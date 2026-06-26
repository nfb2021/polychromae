"""Named natural landscape palettes as ready-to-use Colormap instances."""

from __future__ import annotations

from chromophore._colormap import Colormap

palettes: dict[str, Colormap] = {
    "forest_canopy": Colormap.from_hex(
        ["#2D5016", "#7A9E5A", "#5C4033", "#B8C5A0", "#D4AF37"],
        name="forest_canopy",
        discrete=True,
    ),
    "desert_sunset": Colormap.from_hex(
        ["#CC5500", "#E2725B", "#F4A460", "#C08081", "#5D3A6D"],
        name="desert_sunset",
        discrete=True,
    ),
    "woodland_trail": Colormap.from_hex(
        ["#01796F", "#8B4513", "#4F7942", "#EAE0C8", "#F5DEB3"],
        name="woodland_trail",
        discrete=True,
    ),
    "coastal_morning": Colormap.from_hex(
        ["#9DC3E6", "#93E9BE", "#B5A192", "#FFF5EE", "#4682B4"],
        name="coastal_morning",
        discrete=True,
    ),
    "sunset_glow": Colormap.from_hex(
        ["#FF4500", "#FF69B4", "#967BB6", "#FFD700", "#8B008B"],
        name="sunset_glow",
        discrete=True,
    ),
    "canyon_sunset": Colormap.from_hex(
        ["#C04000", "#D2691E", "#C2B280", "#8A9A5B", "#4B5F78"],
        name="canyon_sunset",
        discrete=True,
    ),
}
