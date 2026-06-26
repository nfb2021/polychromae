"""p(h)ytochrome — GoG-informed scientific visualization style system.

Named after the plant photoreceptor that switches between two stable
light states (Pr ↔ Pfr).  The 'h' is silent in the import; loud in
the docs.

  χρῶμα (chrōma) — Greek for colour.
  φυτόν (phytón) — Greek for plant.
  Py             — Python.

Two GoG layers (Wilkinson 2005):
  theme()  — non-data ink: axes, grid, fonts, backgrounds
  aes()    — data ink:    colour cycle and colourmap defaults

Usage
-----
    import pytochrome as pc

    pc.dark(fig)     # full dark style  — Pfr state (theme + aes)
    pc.light(fig)    # full light style — Pr  state (theme + aes)
    pc.toggle(fig)   # switch states

    # GoG-separated
    pc.theme(fig, "dark")   # structural non-data ink only
    pc.aes(fig, "light")    # data-ink colour encodings only

    pc.save(fig, "output")           # SVG + PNG at 150 DPI, transparent bg
    pc.save(fig, "output", dpi=300)  # higher resolution

    # Token access
    pc.DARK.aes.cycle          # tuple of 8 hex strings
    pc.DARK.theme.text_primary # structural text colour
    pc.colors.dark.cycle       # same as above
    pc.cmap.dark.sequential    # resolved sequential cmap name
    pc.cmap.light.diverging    # resolved diverging cmap name

Aliases for those who know the reference:
    pc.Pr(fig)   # light state — resting
    pc.Pfr(fig)  # dark state  — active
"""

from __future__ import annotations

from typing import Any

# Register natural colormaps and backends
import pytochrome._cmaps as _cmaps_mod

_cmaps_mod.register()

import pytochrome._backends  # noqa: F401
from pytochrome._backends._base import BackendRegistry
from pytochrome._tokens import (
    DARK,
    LIGHT,
    TOKENS,
    AesTokens,
    ModeTokens,
    ThemeTokens,
    _resolve_cmap,
)

__version__ = "0.1.0"
__all__ = [
    "DARK",
    "LIGHT",
    "TOKENS",
    "AesTokens",
    "ModeTokens",
    "Pfr",
    "Pr",
    "ThemeTokens",
    "aes",
    "cmap",
    "colors",
    "dark",
    "light",
    "natural_cmaps",
    "save",
    "theme",
    "toggle",
]


# ---------------------------------------------------------------------------
# Full-mode convenience functions (theme + aes)
# ---------------------------------------------------------------------------


def dark(fig: Any) -> Any:
    """Apply full dark style to *fig* (Pfr state). Returns *fig*."""
    return BackendRegistry.find(fig).apply(fig, DARK)


def light(fig: Any) -> Any:
    """Apply full light style to *fig* (Pr state). Returns *fig*."""
    return BackendRegistry.find(fig).apply(fig, LIGHT)


def toggle(fig: Any) -> Any:
    """Switch *fig* between dark and light states. Returns *fig*."""
    backend = BackendRegistry.find(fig)
    current = backend.get_mode(fig)
    return backend.apply(fig, LIGHT if current == "dark" else DARK)


# Phytochrome state aliases
Pfr = dark  # far-red absorbing — the active dark state
Pr = light  # red absorbing     — the resting light state


# ---------------------------------------------------------------------------
# GoG-separated functions
# ---------------------------------------------------------------------------


def theme(fig: Any, mode: str = "dark") -> Any:
    """Apply structural non-data ink only (GoG: theme layer).

    Sets axes, grid, fonts, and backgrounds without touching the
    colour cycle or colourmap.  Returns *fig*.
    """
    tokens = DARK if mode == "dark" else LIGHT
    return BackendRegistry.find(fig).apply_theme(fig, tokens.theme)


def aes(fig: Any, mode: str = "dark") -> Any:
    """Apply data-ink colour encodings only (GoG: aesthetics layer).

    Sets the qualitative colour cycle and default colourmap without
    touching structural elements.  Returns *fig*.
    """
    tokens = DARK if mode == "dark" else LIGHT
    return BackendRegistry.find(fig).apply_aes(fig, tokens.aes)


# ---------------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------------


def save(
    fig: Any,
    path: str,
    formats: tuple[str, ...] = ("svg", "png"),
    dpi: int = 150,
) -> None:
    """Save *fig* to *path* in one or more formats with transparent background.

    Parameters
    ----------
    fig:
        A matplotlib or Plotly figure.
    path:
        Output path without extension (e.g. ``"figures/timeseries"``).
    formats:
        Tuple of format strings: ``"svg"``, ``"png"``, ``"pdf"``.
    dpi:
        Resolution for raster formats. 150 for web, 300 for print.

    """
    from pathlib import Path

    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)

    try:
        import matplotlib.figure as _mf

        if isinstance(fig, _mf.Figure):
            for fmt in formats:
                fig.savefig(
                    out.with_suffix(f".{fmt}"),
                    dpi=dpi,
                    bbox_inches="tight",
                    transparent=True,
                    metadata={},
                )
            return
    except ImportError:
        pass

    try:
        import plotly.graph_objects as go

        if isinstance(fig, go.Figure):
            for fmt in formats:
                if fmt == "html":
                    fig.write_html(out.with_suffix(".html"))
                else:
                    fig.write_image(str(out.with_suffix(f".{fmt}")), scale=dpi / 72)
            return
    except ImportError:
        pass

    raise TypeError(f"Cannot save figure of type {type(fig).__qualname__}")


# ---------------------------------------------------------------------------
# Colour / cmap accessors
# ---------------------------------------------------------------------------


class _ColorsNamespace:
    """Access colour tokens by mode.

    ``pc.colors.dark``  → DARK.aes  (AesTokens: .cycle, .cmap_sequential …)
    ``pc.colors.light`` → LIGHT.aes
    """

    dark = DARK.aes
    light = LIGHT.aes

    def __repr__(self) -> str:
        return "pytochrome.colors  (.dark / .light  → AesTokens)"


class _CmapNamespace:
    """Access resolved colourmap names by mode.

    ``pc.cmap.dark.sequential``  → e.g. 'plasma'
    ``pc.cmap.light.diverging``  → e.g. 'RdBu_r'
    """

    class _Mode:
        def __init__(self, aes: AesTokens) -> None:
            self._aes = aes

        @property
        def sequential(self) -> str:
            return _resolve_cmap(self._aes.cmap_sequential)

        @property
        def diverging(self) -> str:
            return _resolve_cmap(self._aes.cmap_diverging)

        def __repr__(self) -> str:
            return (
                f"pytochrome.cmap.<mode>  "
                f"(.sequential='{self.sequential}', .diverging='{self.diverging}')"
            )

    dark = _Mode(DARK.aes)
    light = _Mode(LIGHT.aes)

    def __repr__(self) -> str:
        return "pytochrome.cmap  (.dark / .light  → .sequential / .diverging)"


colors = _ColorsNamespace()
cmap = _CmapNamespace()


class _NaturalCmapsNamespace:
    """Named colormaps from natural landscape palettes.

    Each attribute is the registered matplotlib colormap name (also accepted by
    ``pc.cmap`` accessors and Plotly via the pytochrome backend).  Append ``_r``
    for the reversed variant.

    Usage
    -----
        fig, ax = plt.subplots()
        ax.imshow(data, cmap=pc.natural_cmaps.forest_canopy)

        # or pass the name directly to AesTokens
        tokens = pc.DARK.aes._replace(cmap_sequential=pc.natural_cmaps.desert_sunset)
    """

    forest_canopy = "pytochrome_forest_canopy"
    desert_sunset = "pytochrome_desert_sunset"
    woodland_trail = "pytochrome_woodland_trail"
    coastal_morning = "pytochrome_coastal_morning"
    sunset_glow = "pytochrome_sunset_glow"
    canyon_sunset = "pytochrome_canyon_sunset"

    all: tuple[str, ...] = (
        "pytochrome_forest_canopy",
        "pytochrome_desert_sunset",
        "pytochrome_woodland_trail",
        "pytochrome_coastal_morning",
        "pytochrome_sunset_glow",
        "pytochrome_canyon_sunset",
    )

    def __repr__(self) -> str:
        names = ", ".join(
            f".{k}"
            for k in (
                "forest_canopy",
                "desert_sunset",
                "woodland_trail",
                "coastal_morning",
                "sunset_glow",
                "canyon_sunset",
            )
        )
        return f"pytochrome.natural_cmaps  ({names})"


natural_cmaps = _NaturalCmapsNamespace()


# ---------------------------------------------------------------------------
# Import-time defaults
# ---------------------------------------------------------------------------
# Set the pytochrome DARK colour cycle and image cmap as matplotlib defaults
# so any ax.plot() / ax.scatter() / ax.imshow() call uses them without
# needing an explicit pc.dark(fig) / pc.aes(fig) call.


def _install_defaults() -> None:
    try:
        import matplotlib.pyplot as _plt

        _plt.rcParams["axes.prop_cycle"] = _plt.cycler(color=list(DARK.aes.cycle))
        _plt.rcParams["image.cmap"] = _resolve_cmap(DARK.aes.cmap_sequential)
    except Exception:
        pass


_install_defaults()
del _install_defaults
