"""Named colormaps derived from natural landscape palettes."""
from __future__ import annotations

NATURAL_PALETTES: dict[str, tuple[str, ...]] = {
    "forest_canopy":   ("#2D5016", "#7A9E5A", "#5C4033", "#B8C5A0", "#D4AF37"),
    "desert_sunset":   ("#CC5500", "#E2725B", "#F4A460", "#C08081", "#5D3A6D"),
    "woodland_trail":  ("#01796F", "#8B4513", "#4F7942", "#EAE0C8", "#F5DEB3"),
    "coastal_morning": ("#9DC3E6", "#93E9BE", "#B5A192", "#FFF5EE", "#4682B4"),
    "sunset_glow":     ("#FF4500", "#FF69B4", "#967BB6", "#FFD700", "#8B008B"),
    "canyon_sunset":   ("#C04000", "#D2691E", "#C2B280", "#8A9A5B", "#4B5F78"),
}

PREFIX = "pytochrome_"


def as_plotly_colorscale(name: str) -> list[list]:
    """Return a Plotly-compatible [[position, colour], ...] list."""
    key = name.removeprefix(PREFIX)
    stops = NATURAL_PALETTES[key]
    n = len(stops) - 1
    return [[round(i / n, 4), c] for i, c in enumerate(stops)]


def is_natural(name: str) -> bool:
    """True if *name* refers to one of the pytochrome natural palettes."""
    return name.startswith(PREFIX) and name.removeprefix(PREFIX).removesuffix("_r") in NATURAL_PALETTES


def register() -> None:
    """Register all natural palettes as named matplotlib ListedColormaps."""
    try:
        import matplotlib as mpl
        import matplotlib.colors as mcolors
    except ImportError:
        return

    for name, stops in NATURAL_PALETTES.items():
        full = f"{PREFIX}{name}"
        cmap = mcolors.ListedColormap(list(stops), name=full)
        mpl.colormaps.register(cmap, name=full, force=True)
        mpl.colormaps.register(cmap.reversed(), name=f"{full}_r", force=True)
