"""Core Colormap class — cross-framework colourmap container."""
from __future__ import annotations

import re
from dataclasses import dataclass, field


def _hex_to_rgb01(h: str) -> tuple[float, float, float]:
    h = h.lstrip("#")
    return (int(h[0:2], 16) / 255, int(h[2:4], 16) / 255, int(h[4:6], 16) / 255)


def _rgb01_to_hex(r: float, g: float, b: float) -> str:
    return f"#{int(r * 255):02x}{int(g * 255):02x}{int(b * 255):02x}"


def _rgb_str_to_tuple(s: str) -> tuple[float, float, float]:
    m = re.match(r"rgb\((\d+),?\s*(\d+),?\s*(\d+)\)", s)
    if not m:
        raise ValueError(f"Cannot parse rgb string: {s!r}")
    return tuple(int(x) / 255 for x in m.groups())  # type: ignore[return-value]


@dataclass
class Colormap:
    """A colourmap that converts between matplotlib, Plotly, and raw hex.

    Parameters
    ----------
    name:
        Identifier used when registering with matplotlib.
    colors:
        Ordered list of colours as hex strings (``"#rrggbb"``).
    discrete:
        If True, treated as a qualitative palette (ListedColormap).
        If False, treated as a continuous gradient (LinearSegmentedColormap).

    """

    name: str
    colors: list[str] = field(default_factory=list)
    discrete: bool = False

    # ------------------------------------------------------------------
    # Constructors
    # ------------------------------------------------------------------

    @classmethod
    def from_hex(
        cls,
        colors: list[str],
        name: str = "custom",
        discrete: bool = False,
    ) -> Colormap:
        """Create from an ordered list of hex colour strings."""
        return cls(name=name, colors=list(colors), discrete=discrete)

    @classmethod
    def from_matplotlib(cls, name: str) -> Colormap:
        """Wrap an existing matplotlib colormap by sampling 256 stops."""
        import matplotlib as mpl

        cmap = mpl.colormaps[name]
        n = len(getattr(cmap, "colors", [])) or 256
        discrete = hasattr(cmap, "colors")
        colors = [
            _rgb01_to_hex(*cmap(i / (n - 1))[:3])
            for i in range(n)
        ]
        return cls(name=name, colors=colors, discrete=discrete)

    @classmethod
    def from_plotly(cls, name: str, n: int = 11) -> Colormap:
        """Sample a named Plotly colorscale into *n* hex stops."""
        import plotly.colors as pc

        scale = pc.get_colorscale(name)
        sampled = pc.sample_colorscale(scale, n)
        colors = []
        for c in sampled:
            if c.startswith("rgb"):
                r, g, b = _rgb_str_to_tuple(c)
                colors.append(_rgb01_to_hex(r, g, b))
            else:
                colors.append(c)
        return cls(name=name, colors=colors, discrete=False)

    # ------------------------------------------------------------------
    # Exporters
    # ------------------------------------------------------------------

    def to_matplotlib(self, n: int = 256):
        """Return a matplotlib colormap (Listed or LinearSegmented)."""
        import matplotlib.colors as mcolors

        if self.discrete:
            return mcolors.ListedColormap(self.colors, name=self.name)
        return mcolors.LinearSegmentedColormap.from_list(self.name, self.colors, N=n)

    def to_plotly(self) -> list[list]:
        """Return a Plotly-compatible ``[[position, colour], ...]`` colorscale."""
        n = len(self.colors) - 1
        return [[round(i / n, 6), c] for i, c in enumerate(self.colors)]

    def register(self, force: bool = True) -> None:
        """Register with matplotlib under ``self.name``."""
        import matplotlib as mpl

        cmap = self.to_matplotlib()
        mpl.colormaps.register(cmap, name=self.name, force=force)
        mpl.colormaps.register(cmap.reversed(), name=f"{self.name}_r", force=force)

    # ------------------------------------------------------------------
    # Jupyter preview
    # ------------------------------------------------------------------

    def _repr_html_(self) -> str:
        if self.discrete:
            return self._swatch_html()
        return self._gradient_html()

    def _gradient_html(self) -> str:
        stops = ", ".join(
            f"{c} {round(i / (len(self.colors) - 1) * 100)}%"
            for i, c in enumerate(self.colors)
        )
        return (
            f'<div style="'
            f"display:inline-block;width:320px;height:24px;"
            f"border-radius:4px;overflow:hidden;"
            f"background:linear-gradient(to right,{stops});"
            f'margin:2px 0">'
            f'<span style="display:block;padding:4px 8px;font-size:11px;'
            f'font-family:monospace;color:#fff;text-shadow:0 0 3px #000">'
            f"{self.name}"
            f"</span></div>"
        )

    def _swatch_html(self) -> str:
        swatches = "".join(
            f'<div title="{c}" style="'
            f"display:inline-block;width:{max(20, 240 // len(self.colors))}px;"
            f'height:32px;background:{c}"></div>'
            for c in self.colors
        )
        return (
            f'<div style="display:inline-block">'
            f'<div style="font-size:11px;font-family:monospace;margin-bottom:2px">'
            f"{self.name}</div>"
            f'<div style="border-radius:4px;overflow:hidden">{swatches}</div>'
            f"</div>"
        )

    def __repr__(self) -> str:
        kind = "discrete" if self.discrete else "continuous"
        return f"Colormap({self.name!r}, {len(self.colors)} stops, {kind})"
