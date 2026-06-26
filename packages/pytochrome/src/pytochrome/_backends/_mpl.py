"""Matplotlib backend — handles Figure objects (2D and 3D axes)."""
from __future__ import annotations

from typing import Any

import matplotlib
import matplotlib.pyplot as plt

from pytochrome._backends._base import BackendRegistry, StyleBackend
from pytochrome._tokens import AesTokens, ThemeTokens
from pytochrome._tokens import _resolve_cmap

# ---------------------------------------------------------------------------
# Font stacks
# ---------------------------------------------------------------------------

_FONT_STACK       = ["Space Grotesk", "Helvetica Neue", "Arial", "sans-serif"]
# "Space Grotesk Medium" is registered as a separate family on macOS.
# Use it as the first choice for titles to get medium weight without
# triggering a numeric-weight lookup warning.
_FONT_TITLE_STACK = ["Space Grotesk Medium", "Space Grotesk", "Helvetica Neue", "Arial", "sans-serif"]
_MONO_STACK       = ["SF Mono", "Fira Mono", "DejaVu Sans Mono", "Courier New"]


def _rgba_to_mpl(rgba: str) -> tuple[float, float, float, float]:
    """Parse 'rgba(r,g,b,a)' into a matplotlib RGBA tuple (0–1 normalised)."""
    inner = rgba.strip()[5:-1]
    r, g, b, a = [float(x.strip()) for x in inner.split(",")]
    return r / 255, g / 255, b / 255, a


class MatplotlibBackend(StyleBackend):
    """Style backend for matplotlib Figure objects."""

    def can_handle(self, fig: Any) -> bool:
        return isinstance(fig, matplotlib.figure.Figure)

    # ------------------------------------------------------------------
    # GoG: Theme layer — non-data ink
    # ------------------------------------------------------------------

    def apply_theme(self, fig: Any, tokens: ThemeTokens) -> Any:
        """Apply structural non-data ink: axes, grid, fonts, backgrounds."""
        axis_color = _rgba_to_mpl(tokens.axis)
        grid_color = _rgba_to_mpl(tokens.grid)

        # Transparent figure background
        fig.patch.set_facecolor("none")
        fig.patch.set_alpha(0.0)

        for ax in fig.get_axes():
            ax.set_facecolor("none")
            ax.patch.set_alpha(0.0)

            # Spines
            for spine in ax.spines.values():
                spine.set_edgecolor(axis_color)
                spine.set_linewidth(0.8)
            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)

            # Ticks
            ax.tick_params(
                colors=tokens.text_secondary,
                labelcolor=tokens.text_secondary,
                direction="in",
                width=0.6,
                length=4,
                which="major",
            )
            ax.tick_params(length=2, which="minor")

            # Tick label font (data layer — monospace for numeric readability)
            for label in ax.get_xticklabels() + ax.get_yticklabels():
                label.set_color(tokens.text_secondary)
                label.set_fontfamily(_MONO_STACK)
                label.set_fontsize(10)

            # Axis labels (descriptive / prose layer)
            for lbl in (ax.xaxis.label, ax.yaxis.label):
                lbl.set_color(tokens.text_primary)
                lbl.set_fontfamily(_FONT_STACK)
                lbl.set_fontsize(11)

            # Title — Medium weight via family name, not numeric fontweight
            ax.title.set_color(tokens.text_primary)
            ax.title.set_fontfamily(_FONT_TITLE_STACK)
            ax.title.set_fontsize(14)

            # Grid
            ax.grid(True, axis="y", color=grid_color, linewidth=0.6, zorder=0)
            ax.grid(False, axis="x")

            # Legend
            if ax.get_legend() is not None:
                leg = ax.get_legend()
                leg.get_frame().set_facecolor("none")
                leg.get_frame().set_edgecolor("none")
                for text in leg.get_texts():
                    text.set_color(tokens.text_primary)
                    text.set_fontfamily(_FONT_STACK)
                    text.set_fontsize(10)

            # 3D axes
            try:
                from mpl_toolkits.mplot3d import Axes3D as _Axes3D  # noqa: PLC0415
                if isinstance(ax, _Axes3D):
                    ax.set_facecolor("none")
                    for pane in (ax.xaxis.pane, ax.yaxis.pane, ax.zaxis.pane):
                        pane.fill = False
                        pane.set_edgecolor(axis_color)
            except ImportError:
                pass

        # Figure suptitle
        if fig._suptitle is not None:  # noqa: SLF001
            fig._suptitle.set_color(tokens.text_primary)        # noqa: SLF001
            fig._suptitle.set_fontfamily(_FONT_TITLE_STACK)     # noqa: SLF001

        # rcParams — structural defaults for axes/artists added after apply_theme
        plt.rcParams.update({
            "font.family":     "sans-serif",
            "font.sans-serif": _FONT_STACK,
            "font.monospace":  _MONO_STACK,
            "font.size":       11,
            "text.color":      tokens.text_primary,
            "axes.facecolor":  "none",
            "axes.edgecolor":  axis_color,
            "axes.labelcolor": tokens.text_primary,
            "axes.labelsize":  11,
            "axes.titlecolor": tokens.text_primary,
            "axes.titlesize":  14,
            "axes.spines.top":   False,
            "axes.spines.right": False,
            "xtick.color":      tokens.text_secondary,
            "ytick.color":      tokens.text_secondary,
            "xtick.labelcolor": tokens.text_secondary,
            "ytick.labelcolor": tokens.text_secondary,
            "xtick.labelsize":  10,
            "ytick.labelsize":  10,
            "xtick.direction":  "in",
            "ytick.direction":  "in",
            "xtick.major.width": 0.6,
            "ytick.major.width": 0.6,
            "xtick.major.size":  4.0,
            "ytick.major.size":  4.0,
            "xtick.minor.size":  2.0,
            "ytick.minor.size":  2.0,
            "axes.grid":        True,
            "axes.grid.axis":   "y",
            "grid.color":       grid_color,
            "grid.linewidth":   0.6,
            "grid.linestyle":   "-",
            "grid.alpha":       1.0,
            "legend.facecolor":   "none",
            "legend.edgecolor":   (0, 0, 0, 0),
            "legend.labelcolor":  tokens.text_primary,
            "legend.fontsize":    10,
            "legend.frameon":     False,
            "legend.framealpha":  0.0,
            "figure.dpi":        150,
            "figure.facecolor":  "none",
            "figure.edgecolor":  "none",
            "savefig.facecolor": "none",
            "savefig.edgecolor": "none",
            "savefig.transparent": True,
        })

        return fig

    # ------------------------------------------------------------------
    # GoG: Aesthetics layer — data ink
    # ------------------------------------------------------------------

    def apply_aes(self, fig: Any, tokens: AesTokens) -> Any:
        """Apply data-ink colour encodings: qualitative cycle and default cmap."""
        plt.rcParams["axes.prop_cycle"] = plt.cycler(color=list(tokens.cycle))
        plt.rcParams["image.cmap"]      = _resolve_cmap(tokens.cmap_sequential)
        return fig

    # ------------------------------------------------------------------
    # Mode tracking
    # ------------------------------------------------------------------

    def get_mode(self, fig: Any) -> str | None:
        return BackendRegistry.read_tag(fig)


# Register at import time
BackendRegistry.register(MatplotlibBackend())
