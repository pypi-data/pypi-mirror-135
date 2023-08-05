"""
A major part of this code is translated from https://github.com/microsoft/Swin-Transformer
"""

import jax.numpy as jnp
import flax.linen as nn

from ..layers import PatchEmbed, TransformerMLP, DropPath, AdaptiveAveragePool1D

from typing import Iterable, Optional

__all__ = [
    "SwinTransformer",
    "SwinTiny224",
    "SwinSmall224",
    "SwinBase224",
    "SwinBase384",
    "SwinLarge224",
    "SwinLarge384",
]


def window_partition(x, window_size):
    batch, height, width, channels = x.shape
    x = jnp.reshape(
        x,
        (
            batch,
            height // window_size,
            window_size,
            width // window_size,
            window_size,
            channels,
        ),
    )
    windows = jnp.reshape(
        jnp.transpose(x, (0, 1, 3, 2, 4, 5)), (-1, window_size, window_size, channels)
    )
    return windows


def window_reverse(windows, window_size, height, width):
    batch = int(windows.shape[0] / (height * width / window_size / window_size))
    x = jnp.reshape(
        windows,
        (
            batch,
            height // window_size,
            width // window_size,
            window_size,
            window_size,
            -1,
        ),
    )
    x = jnp.reshape(jnp.transpose(x, (0, 1, 3, 2, 4, 5)), (batch, height, width, -1))
    return x


class WindowAttention(nn.Module):
    dim: int
    num_heads: int
    window_size: Iterable[int]
    use_bias: bool = True
    att_drop: float = 0.0
    proj_drop: float = 0.0
    deterministic: Optional[bool] = None

    def get_rel_pos_index(self):
        h_indices = jnp.arange(0, self.window_size[0])
        w_indices = jnp.arange(0, self.window_size[1])
        indices = jnp.stack(jnp.meshgrid(h_indices, w_indices))
        flatten_indices = jnp.reshape(indices, (2, -1))
        relative_indices = flatten_indices[:, :, None] - flatten_indices[:, None, :]
        relative_indices = jnp.transpose(relative_indices, (1, 2, 0))

        relative_indices.at[:, :, 0].add(self.window_size[0] - 1)
        relative_indices.at[:, :, 1].add(self.window_size[1] - 1)
        relative_indices.at[:, :, 0].mul(2 * self.window_size[1] - 1)
        relative_pos_index = jnp.sum(relative_indices, -1)
        return relative_pos_index

    @nn.compact
    def __call__(self, inputs, mask=None, deterministic=None):

        deterministic = nn.merge_param(
            "deterministic", self.deterministic, deterministic
        )

        rpbt = self.param(
            "rel_pos_bias_table",
            nn.initializers.normal(0.02),
            (
                (2 * self.window_size[0] - 1) * (2 * self.window_size[1] - 1),
                self.num_heads,
            ),
        )

        relative_pos_index = self.variable(
            "rel_pos_index", "rel_pos_index", self.get_rel_pos_index
        )

        batch, n, channels = inputs.shape
        qkv = nn.Dense(self.dim * 3, use_bias=self.use_bias)(inputs)
        qkv = qkv.reshape(batch, n, 3, self.num_heads, channels // self.num_heads)
        qkv = jnp.transpose(qkv, (2, 0, 3, 1, 4))
        q, k, v = qkv[0], qkv[1], qkv[2]

        q = q * ((self.dim // self.num_heads) ** -0.5)
        att = q @ jnp.swapaxes(k, -2, -1)

        rel_pos_bias = jnp.reshape(
            rpbt[jnp.reshape(relative_pos_index.value, (-1))],
            (
                self.window_size[0] * self.window_size[1],
                self.window_size[0] * self.window_size[1],
                -1,
            ),
        )
        rel_pos_bias = jnp.transpose(rel_pos_bias, (2, 0, 1))
        att += jnp.expand_dims(rel_pos_bias, 0)

        if mask is not None:
            att = jnp.reshape(
                att, (batch // mask.shape[0], mask.shape[0], self.num_heads, n, n)
            )
            att = att + jnp.expand_dims(jnp.expand_dims(mask, 1), 0)
            att = jnp.reshape(att, (-1, self.num_heads, n, n))
            att = nn.softmax(att)

        else:
            att = nn.softmax(att)

        att = nn.Dropout(self.att_drop)(att, deterministic)

        x = jnp.reshape(jnp.swapaxes(att @ v, 1, 2), (batch, n, channels))
        x = nn.Dense(self.dim)(x)
        x = nn.Dropout(self.proj_drop)(x, deterministic)
        return x


class SwinBlock(nn.Module):
    dim: int
    inp_hw: Iterable[int]
    num_heads: int
    window_size: int = 7
    shift_size: int = 0
    mlp_ratio: int = 4
    use_att_bias: bool = True
    dropout: float = 0.0
    att_dropout: float = 0.0
    drop_path: float = 0.0
    deterministic: Optional[bool] = None

    def get_att_mask(self, shift_size, window_size, height, width):
        if shift_size > 0:
            mask = jnp.zeros([1, height, width, 1])
            h_slices = (
                slice(0, -window_size),
                slice(-window_size, -shift_size),
                slice(-shift_size, None),
            )
            w_slices = (
                slice(0, -window_size),
                slice(-window_size, -shift_size),
                slice(-shift_size, None),
            )

            count = 0
            for h in h_slices:
                for w in w_slices:
                    mask.at[:, h, w, :].set(count)
                    count += 1

            mask_windows = window_partition(mask, window_size)
            mask_windows = jnp.reshape(mask_windows, (-1, window_size * window_size))
            att_mask = jnp.expand_dims(mask_windows, 1) - jnp.expand_dims(
                mask_windows, 2
            )
            att_mask = jnp.where(att_mask != 0, att_mask, float(-100.0))
            att_mask = jnp.where(att_mask == 0, att_mask, float(0.0))

        else:
            att_mask = None
            return att_mask

    @nn.compact
    def __call__(self, inputs, deterministic=None):

        deterministic = nn.merge_param(
            "deterministic", self.deterministic, deterministic
        )

        height, width = self.inp_hw[0], self.inp_hw[1]

        input_resolution = min(height, width)
        if input_resolution <= self.window_size:
            shift_size = 0
            window_size = input_resolution
        else:
            shift_size = self.shift_size
            window_size = self.window_size

        att_mask = self.variable(
            "attention_mask",
            "mask",
            self.get_att_mask,
            shift_size,
            window_size,
            height,
            width,
        )

        batch, length, channels = inputs.shape
        height, width = self.inp_hw[0], self.inp_hw[1]
        assert length == height * width

        residual = inputs
        x = nn.LayerNorm()(inputs)
        x = jnp.reshape(x, (batch, height, width, channels))

        if shift_size > 0:
            shifted_x = jnp.roll(x, (-shift_size, -shift_size), axis=(1, 2))
        else:
            shifted_x = x

        x_windows = window_partition(shifted_x, window_size)
        x_windows = jnp.reshape(x_windows, (-1, window_size * window_size, channels))

        att_windows = WindowAttention(
            self.dim,
            self.num_heads,
            (window_size, window_size),
            self.use_att_bias,
            self.att_dropout,
            self.dropout,
        )(x_windows, att_mask.value, deterministic)

        att_windows = jnp.reshape(att_windows, (-1, window_size, window_size, channels))
        shifted_x = window_reverse(att_windows, window_size, height, width)

        if shift_size > 0:
            x = jnp.roll(shifted_x, (shift_size, shift_size), axis=(1, 2))
        else:
            x = shifted_x

        x = jnp.reshape(x, (batch, height * width, channels))

        x = residual + DropPath(self.drop_path)(x, deterministic)
        x = nn.LayerNorm()(x)
        mlp = TransformerMLP(self.dim * self.mlp_ratio, self.dim)(x, deterministic)
        x = x + DropPath(self.drop_path)(mlp, deterministic)

        return x


class PatchMerging(nn.Module):
    inp_res: Iterable[int]
    dim: int

    @nn.compact
    def __call__(self, inputs):
        batch, n, channels = inputs.shape
        height, width = self.inp_res[0], self.inp_res[1]
        x = jnp.reshape(inputs, (batch, height, width, channels))

        x0 = x[:, 0::2, 0::2, :]
        x1 = x[:, 1::2, 0::2, :]
        x2 = x[:, 0::2, 1::2, :]
        x3 = x[:, 1::2, 1::2, :]

        x = jnp.concatenate([x0, x1, x2, x3], axis=-1)
        x = jnp.reshape(x, (batch, -1, 4 * channels))
        x = nn.LayerNorm()(x)
        x = nn.Dense(2 * self.dim, use_bias=False)(x)
        return x


class SwinLayer(nn.Module):
    inp_res: Iterable[int]
    dim: int
    num_heads: int
    window_size: int
    mlp_ratio: int
    use_att_bias: bool
    dropout: float
    att_dropout: float
    drop_path: float
    depth: int
    downsample: Optional[bool] = False
    deterministic: Optional[bool] = None

    @nn.compact
    def __call__(self, x, deterministic=None):

        deterministic = nn.merge_param(
            "deterministic", self.deterministic, deterministic
        )

        for i in range(self.depth):
            x = SwinBlock(
                self.dim,
                self.inp_res,
                self.num_heads,
                self.window_size,
                0 if (i % 2 == 0) else self.window_size // 2,
                self.mlp_ratio,
                self.use_att_bias,
                self.dropout,
                self.att_dropout,
                self.drop_path[i]
                if isinstance(self.drop_path, (list, tuple))
                else self.drop_path,
            )(x, deterministic)

        if self.downsample:
            x = PatchMerging(self.inp_res, self.dim)(x)

        return x


class SwinTransformer(nn.Module):
    patch_size: int = 4
    emb_dim: int = 96
    depths: Iterable[int] = (2, 2, 6, 2)
    num_heads: Iterable[int] = (3, 6, 12, 24)
    window_size: int = 7
    mlp_ratio: int = 4
    use_att_bias: bool = True
    dropout: float = 0.0
    att_dropout: float = 0.0
    drop_path: float = 0.1
    use_abs_pos_emb: bool = False
    attach_head: bool = True
    num_classes: Optional[int] = 1000
    deterministic: Optional[bool] = None

    @nn.compact
    def __call__(self, inputs, deterministic=None):

        deterministic = nn.merge_param(
            "deterministic", self.deterministic, deterministic
        )

        x = PatchEmbed(self.patch_size, self.emb_dim, use_norm=True)(inputs)
        num_patches = x.shape[1]
        patch_grid = (
            inputs.shape[1] // self.patch_size,
            inputs.shape[2] // self.patch_size,
        )

        if self.use_abs_pos_emb:
            abs_pos_emb = self.param(
                "abs_pos_emb",
                nn.initializers.normal(0.02),
                (1, num_patches, self.emb_dim),
            )
            x = x + abs_pos_emb

        x = nn.Dropout(self.dropout)(x, deterministic)

        dpr = [x.item() for x in jnp.linspace(0, self.drop_path, sum(self.depths))]

        layers = []
        for i in range(len(self.depths)):
            x = SwinLayer(
                (patch_grid[0] // (2 ** i), patch_grid[1] // (2 ** i)),
                int(self.emb_dim * 2 ** i),
                self.num_heads[i],
                self.window_size,
                self.mlp_ratio,
                self.use_att_bias,
                self.dropout,
                self.att_dropout,
                self.drop_path,
                self.depths[i],
                True if i < (len(self.depths) - 1) else False,
            )(x, deterministic)
        x = nn.LayerNorm()(x)
        x = AdaptiveAveragePool1D(1)(x)
        x = jnp.reshape(x, (1, -1))

        if self.attach_head:
            x = nn.Dense(self.num_classes)(x)
            x = nn.softmax(x)

        return x


def SwinTiny224(attach_head=True, num_classes=1000, dropout=0.0):
    return SwinTransformer(
        patch_size=4,
        emb_dim=96,
        depths=(2, 2, 6, 2),
        num_heads=(3, 6, 12, 24),
        window_size=7,
        mlp_ratio=4,
        use_att_bias=True,
        dropout=dropout,
        att_dropout=0.0,
        drop_path=0.1,
        use_abs_pos_emb=False,
        attach_head=attach_head,
        num_classes=num_classes,
    )


def SwinSmall224(attach_head=True, num_classes=1000, dropout=0.0):
    return SwinTransformer(
        patch_size=4,
        emb_dim=96,
        depths=(2, 2, 18, 2),
        num_heads=(3, 6, 12, 24),
        window_size=7,
        mlp_ratio=4,
        use_att_bias=True,
        dropout=dropout,
        att_dropout=0.0,
        drop_path=0.1,
        use_abs_pos_emb=False,
        attach_head=attach_head,
        num_classes=num_classes,
    )


def SwinBase224(attach_head=True, num_classes=1000, dropout=0.0):
    return SwinTransformer(
        patch_size=4,
        emb_dim=128,
        depths=(2, 2, 18, 2),
        num_heads=(4, 8, 16, 32),
        window_size=7,
        mlp_ratio=4,
        use_att_bias=True,
        dropout=dropout,
        att_dropout=0.0,
        drop_path=0.1,
        use_abs_pos_emb=False,
        attach_head=attach_head,
        num_classes=num_classes,
    )


def SwinLarge224(attach_head=True, num_classes=1000, dropout=0.0):
    return SwinTransformer(
        patch_size=4,
        emb_dim=192,
        depths=(2, 2, 18, 2),
        num_heads=(6, 12, 24, 48),
        window_size=7,
        mlp_ratio=4,
        use_att_bias=True,
        dropout=dropout,
        att_dropout=0.0,
        drop_path=0.1,
        use_abs_pos_emb=False,
        attach_head=attach_head,
        num_classes=num_classes,
    )


def SwinBase384(attach_head=True, num_classes=1000, dropout=0.0):
    return SwinTransformer(
        patch_size=4,
        emb_dim=128,
        depths=(2, 2, 18, 2),
        num_heads=(4, 8, 16, 32),
        window_size=12,
        mlp_ratio=4,
        use_att_bias=True,
        dropout=dropout,
        att_dropout=0.0,
        drop_path=0.1,
        use_abs_pos_emb=False,
        attach_head=attach_head,
        num_classes=num_classes,
    )


def SwinLarge384(attach_head=True, num_classes=1000, dropout=0.0):
    return SwinTransformer(
        patch_size=4,
        emb_dim=192,
        depths=(2, 2, 18, 2),
        num_heads=(6, 12, 24, 48),
        window_size=12,
        mlp_ratio=4,
        use_att_bias=True,
        dropout=dropout,
        att_dropout=0.0,
        drop_path=0.1,
        use_abs_pos_emb=False,
        attach_head=attach_head,
        num_classes=num_classes,
    )
