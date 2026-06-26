# chromophore

Cross-framework colourmap container — load from any source, convert between frameworks,
preview natively in Jupyter.

---

## Design

A single `Colormap` dataclass holds an ordered list of hex stops and a `discrete` flag.
Framework-specific objects are produced on demand — nothing is converted until you ask for it.

```
Colormap(name, colors, discrete)
    ├── .to_matplotlib()   → LinearSegmentedColormap or ListedColormap
    ├── .to_plotly()       → [[position, colour], ...]
    ├── .register()        → registers with mpl.colormaps (+ _r reversed)
    └── ._repr_html_()     → gradient strip or swatch grid in Jupyter
```

---

## Usage

```python
from chromophore import Colormap

# From hex stops — continuous gradient
cm = Colormap.from_hex(["#2D5016", "#7A9E5A", "#D4AF37"], name="forest")
cm.to_matplotlib()     # LinearSegmentedColormap (256 samples)
cm.to_plotly()         # [[0.0, '#2D5016'], [0.5, '#7A9E5A'], [1.0, '#D4AF37']]

# Discrete qualitative palette
cm = Colormap.from_hex(["#2D5016", "#7A9E5A", "#D4AF37"], name="forest", discrete=True)
cm.to_matplotlib()     # ListedColormap

# Wrap an existing matplotlib colormap
cm = Colormap.from_matplotlib("viridis")
cm.to_plotly()

# Sample a Plotly colorscale  (requires chromophore[plotly])
cm = Colormap.from_plotly("Plasma", n=11)
cm.to_matplotlib()

# Register with matplotlib
cm.register()          # available as plt.get_cmap("forest") and "forest_r"
```

## Optional dependencies

| Extra | Unlocks |
|---|---|
| `chromophore[plotly]` | `Colormap.from_plotly()` |
| `chromophore[crameri]` | Crameri scientific colourmaps via `from_matplotlib` |
| `chromophore[cmasher]` | CMasher colourmaps |
| `chromophore[colorcet]` | Colorcet colourmaps |
| `chromophore[all]` | All of the above |

```bash
uv add "chromophore[all]"
```
