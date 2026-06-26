"""Pytochrome colormap registration — natural palettes sourced from chromophore."""
from __future__ import annotations

from chromophore import palettes as _palettes

PREFIX = "pytochrome_"


def as_plotly_colorscale(name: str) -> list[list]:
    """Return a Plotly-compatible [[position, colour], ...] list for a natural palette."""
    key = name.removeprefix(PREFIX)
    colors = _palettes[key].colors
    n = len(colors) - 1
    return [[round(i / n, 4), c] for i, c in enumerate(colors)]


def is_natural(name: str) -> bool:
    """True if *name* refers to one of the pytochrome natural palettes."""
    return name.startswith(PREFIX) and name.removeprefix(PREFIX).removesuffix("_r") in _palettes


def register() -> None:
    """Register all natural palettes as named matplotlib ListedColormaps."""
    try:
        import matplotlib as mpl
        import matplotlib.colors as mcolors
    except ImportError:
        return

    for name, cm in _palettes.items():
        full = f"{PREFIX}{name}"
        mpl_cm = mcolors.ListedColormap(cm.colors, name=full)
        mpl.colormaps.register(mpl_cm, name=full, force=True)
        mpl.colormaps.register(mpl_cm.reversed(), name=f"{full}_r", force=True)
