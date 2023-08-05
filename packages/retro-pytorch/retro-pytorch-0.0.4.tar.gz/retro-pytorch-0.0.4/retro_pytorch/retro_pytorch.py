import torch
import torch.nn.functional as F
from torch import nn, einsum

from einops import rearrange, repeat

# helper functions

def exists(val):
    return val is not None

def default(val, d):
    return val if exists(val) else d

def divisible_by(val, divisor):
    return (val / divisor).is_integer()

def cast_tuple(val, num = 1):
    return val if isinstance(val, tuple) else ((val,) * num)

# normalization

class RMSNorm(nn.Module):
    def __init__(
        self,
        dim,
        *,
        eps = 1e-8
    ):
        super().__init__()
        self.eps = eps
        self.scale = dim ** -0.5
        self.gamma = nn.Parameter(torch.ones(dim))

    def forward(self, x):
        norm = x.norm(keepdim = True, dim = -1) * self.scale
        return (x / norm.clamp(min = self.eps)) * self.gamma

# positional embedding

class RotaryEmbedding(nn.Module):
    def __init__(self, dim):
        super().__init__()
        inv_freq = 1. / (10000 ** (torch.arange(0, dim, 2).float() / dim))
        self.register_buffer('inv_freq', inv_freq)

    def forward(self, max_seq_len, device):
        seq = torch.arange(max_seq_len, device = device)
        freqs = einsum('i , j -> i j', seq.type_as(self.inv_freq), self.inv_freq)
        emb = torch.cat((freqs, freqs), dim = -1)
        return rearrange(emb, 'n d -> 1 1 n d')

def rotate_half(x):
    x = rearrange(x, '... (j d) -> ... j d', j = 2)
    x1, x2 = x.unbind(dim = -2)
    return torch.cat((-x2, x1), dim = -1)

def apply_rotary_pos_emb(t, freqs):
    seq_len = t.shape[-2]
    freqs = freqs[:, :, :seq_len]
    return (t * freqs.cos()) + (rotate_half(t) * freqs.sin())

# feedforward

def FeedForward(dim, mult = 4, dropout = 0.):
    inner_dim = int(mult * dim)

    return nn.Sequential(
        RMSNorm(dim),
        nn.Linear(dim, inner_dim),
        nn.GELU(),
        nn.Dropout(dropout),
        nn.Linear(inner_dim, dim)
    )

# attention

class Attention(nn.Module):
    def __init__(
        self,
        dim,
        *,
        dim_head = 64,
        heads = 8,
        causal = False,
        dropout = 0.
    ):
        super().__init__()
        self.heads = heads
        self.scale = dim_head ** -0.5
        self.causal = causal
        inner_dim = dim_head * heads

        self.norm = RMSNorm(dim)
        self.dropout = nn.Dropout(dropout)

        self.to_q = nn.Linear(dim, inner_dim, bias = False)
        self.to_kv = nn.Linear(dim, inner_dim * 2, bias = False)
        self.to_out = nn.Linear(inner_dim, dim)

    def forward(self, x, context = None, pos_emb = None):
        device, h, scale = x.device, self.heads, self.scale
        kv_input = default(context, x)

        x = self.norm(x)

        q = self.to_q(x)
        k, v = self.to_kv(kv_input).chunk(2, dim = -1)

        # split heads

        q, k, v = map(lambda t: rearrange(t, 'b n (h d) -> b h n d', h = h), (q, k, v))

        # scale

        q = q * scale

        # apply relative positional encoding (rotary embeddings)

        if exists(pos_emb):
            q_pos_emb, k_pos_emb = cast_tuple(pos_emb, num = 2)
            q = apply_rotary_pos_emb(q, q_pos_emb)
            k = apply_rotary_pos_emb(k, k_pos_emb)

        # derive query key similarities

        sim = einsum('b h i d, b h j d -> b h i j', q, k)

        # masking

        if self.causal:
            i, j = sim.shape[-2:]
            causal_mask = torch.ones(i, j, device = device, dtype = torch.bool).triu(j - i + 1)
            mask_value = -torch.finfo(sim.dtype).max
            sim = sim.masked_fill(causal_mask, mask_value)

        # attention

        attn = sim.softmax(dim = -1)

        attn = self.dropout(attn)

        # aggregate

        out = einsum('b h i j, b h j d -> b h i d', attn, v)

        # merge heads

        out = rearrange(out, 'b h n d -> b n (h d)')

        # combine heads linear out

        return self.to_out(out)


class ChunkedCrossAttention(nn.Module):
    def __init__(
        self,
        **kwargs
    ):
        super().__init__()
        self.cross_attn = Attention(**kwargs)

    def forward(self, x, *, context, pos_emb = None, **kwargs):
        # derive variables

        b, n, num_chunks, num_retrieved, chunk_size = x.shape[0], x.shape[-2], *context.shape[-4:-1]
        causal_padding = chunk_size - 1

        # causal padding

        x = F.pad(x, (0, 0, -causal_padding, causal_padding), value = 0.)

        # take care of rotary positional embedding
        # make sure queries positions are properly shifted to the future

        q_pos_emb, k_pos_emb = pos_emb
        q_pos_emb = F.pad(q_pos_emb, (0, 0, -causal_padding, causal_padding), value = 0.)
        pos_emb = (q_pos_emb, k_pos_emb)

        # reshape so we have chunk to chunk attention, without breaking causality

        x = rearrange(x, 'b (k n) d -> (b k) n d', k = num_chunks)
        context = rearrange(context, 'b k r n d -> (b k) (r n) d')

        # cross attention

        out = self.cross_attn(x, context = context, pos_emb = pos_emb, **kwargs)

        # reshape back to original sequence

        out = rearrange(out, '(b k) n d -> b (k n) d', k = num_chunks)

        # pad back to original, with 0s at the beginning (which will be added to the residual and be fine)

        out = F.pad(out, (0, 0, causal_padding, -causal_padding), value = 0.)
        return out

# encoder and decoder classes

class Encoder(nn.Module):
    def __init__(
        self,
        dim,
        *,
        depth,
        causal = False,
        heads = 8,
        dim_head = 64,
        attn_dropout = 0.,
        ff_mult = 4,
        ff_dropout = 0.,
        final_norm = True,
        cross_attn_layers = None,
        chunked_cross_attn = False
    ):
        super().__init__()
        self.layers = nn.ModuleList([])

        rotary_emb_dim = max(default(dim_head, dim_head // 2), 32)
        self.rotary_pos_emb = RotaryEmbedding(rotary_emb_dim)

        for layer_num in range(1, depth + 1):
            has_cross_attn = not exists(cross_attn_layers) or layer_num in cross_attn_layers

            self.layers.append(nn.ModuleList([
                Attention(dim = dim, dim_head = dim_head, heads = heads, dropout = attn_dropout, causal = causal),
                Attention(dim = dim, dim_head = dim_head, heads = heads, dropout = attn_dropout) if has_cross_attn else None,
                FeedForward(dim = dim, mult = ff_mult, dropout = ff_dropout),
            ]))

        self.norm_out = RMSNorm(dim) if final_norm else nn.Identity()

    def forward(self, x, *, chunked_seq):
        device, chunk_size, seq_len = x.device, x.shape[-2], chunked_seq.shape[-2]

        q_pos_emb = self.rotary_pos_emb(chunk_size, device = device)
        k_pos_emb = self.rotary_pos_emb(seq_len, device = device)

        for attn, cross_attn, ff in self.layers:
            x = attn(x, pos_emb = q_pos_emb) + x

            if exists(cross_attn):
                x = cross_attn(x, context = chunked_seq, pos_emb = (q_pos_emb, k_pos_emb)) + x

            x = ff(x) + x

        return self.norm_out(x)

class Decoder(nn.Module):
    def __init__(
        self,
        dim,
        *,
        depth,
        heads = 8,
        dim_head = 64,
        attn_dropout = 0.,
        ff_mult = 4,
        ff_dropout = 0.,
        final_norm = True,
        cross_attn_layers = None
    ):
        super().__init__()
        self.layers = nn.ModuleList([])

        rotary_emb_dim = max(default(dim_head, dim_head // 2), 32)
        self.rotary_pos_emb = RotaryEmbedding(rotary_emb_dim)

        for layer_num in range(1, depth + 1):
            has_cross_attn = not exists(cross_attn_layers) or layer_num in cross_attn_layers

            self.layers.append(nn.ModuleList([
                Attention(dim = dim, dim_head = dim_head, heads = heads, dropout = attn_dropout, causal = True),
                ChunkedCrossAttention(dim = dim, dim_head = dim_head, heads = heads, dropout = attn_dropout) if has_cross_attn else None,
                FeedForward(dim = dim, mult = ff_mult, dropout = ff_dropout),
            ]))

        self.norm_out = RMSNorm(dim) if final_norm else nn.Identity()

    def forward(self, x, *, retrieved):
        device, seq_len, num_chunks, num_neighbors, chunk_size = x.device, x.shape[-2], *retrieved.shape[-4:-1]

        self_attn_pos_emb = self.rotary_pos_emb(seq_len, device = device)

        cross_attn_q_pos_emb = self.rotary_pos_emb(seq_len // num_chunks + chunk_size, device = device)  # need to add extra chunk size, since it will be shifted
        cross_attn_k_pos_emb = self.rotary_pos_emb(num_neighbors * chunk_size, device = device)

        cross_attn_pos_emb = (cross_attn_q_pos_emb, cross_attn_k_pos_emb)

        for attn, cross_attn, ff in self.layers:
            x = attn(x, pos_emb = self_attn_pos_emb) + x

            if exists(cross_attn):
                x = cross_attn(x, context = retrieved, pos_emb = cross_attn_pos_emb) + x

            x = ff(x) + x

        return self.norm_out(x)

# main class

class RETRO(nn.Module):
    def __init__(
        self,
        *,
        num_tokens,
        max_seq_len = 2048,
        enc_dim = 896,
        enc_depth = 2,
        enc_cross_attn_layers = None,
        dec_depth = 12,
        dec_cross_attn_layers = (1, 3, 6, 9),
        heads = 8,
        dec_dim = 768,
        dim_head = 64,
        enc_attn_dropout = 0.,
        enc_ff_dropout = 0.,
        dec_attn_dropout = 0.,
        dec_ff_dropout = 0.
    ):
        super().__init__()
        self.token_emb = nn.Embedding(num_tokens, enc_dim)
        self.pos_emb = nn.Embedding(max_seq_len, enc_dim)

        self.to_decoder_model_dim = nn.Linear(enc_dim, dec_dim) if enc_dim != dec_dim else nn.Identity()
        self.encoder_output_to_decoder_dim = nn.Linear(enc_dim, dec_dim) if enc_dim != dec_dim else nn.Identity()

        self.encoder = Encoder(
            dim = enc_dim,
            depth = enc_depth,
            attn_dropout = enc_attn_dropout,
            ff_dropout = enc_ff_dropout,
            cross_attn_layers = enc_cross_attn_layers
        )

        self.decoder = Decoder(
            dim = dec_dim,
            depth = dec_depth,
            attn_dropout = dec_attn_dropout,
            ff_dropout = dec_ff_dropout,
            cross_attn_layers = dec_cross_attn_layers
        )

        self.to_logits = nn.Linear(dec_dim, num_tokens)

    def forward(
        self,
        seq,
        retrieved,
        return_loss = False
    ):
        """
        b - batch
        n - sequence length / chunk length
        k - number of chunks
        d - feature dimension
        r - num retrieved neighbors
        """

        assert not (return_loss and not self.training), 'must be training if returning loss'

        # handle some user inputs

        if retrieved.ndim == 3:
            retrieved = rearrange(retrieved, 'b k n -> b k 1 n') # 1 neighbor retrieved

        # if training, derive labels

        if return_loss:
            seq, labels = seq[:, :-1], seq[:, 1:]

        # variables

        n, num_chunks, num_neighbors, chunk_size, device = seq.shape[-1], *retrieved.shape[-3:], seq.device

        assert divisible_by(n, chunk_size), 'sequence length must be divisible by chunk size'

        # embed both sequence and retrieved chunks

        embed = self.token_emb(seq)
        retrieved = self.token_emb(retrieved)

        # get absolute positional embedding

        pos_emb = self.pos_emb(torch.arange(n, device = device))
        pos_emb = rearrange(pos_emb, 'n d -> 1 n d')
        embed = embed + pos_emb

        # encode

        retrieved = rearrange(retrieved, 'b k r n d -> (b k r) n d', r = num_neighbors)
        embed_as_context = repeat(embed, 'b (k n) d -> (b k r) n d', k = num_chunks, r = num_neighbors)

        retrieved = self.encoder(retrieved, chunked_seq = embed_as_context)
        retrieved = rearrange(retrieved, '(b k r) n d -> b k r n d', k = num_chunks, r = num_neighbors)

        # project both sequence embedding and retrieved embedding to decoder dimension if necessary

        embed = self.to_decoder_model_dim(embed)
        retrieved = self.encoder_output_to_decoder_dim(retrieved)

        # decode

        embed = self.decoder(embed, retrieved = retrieved)

        # project to logits

        logits = self.to_logits(embed)

        if not return_loss:
            return logits

        # cross entropy loss

        loss = F.cross_entropy(rearrange(logits, 'b n c -> b c n'), labels)
        return loss
