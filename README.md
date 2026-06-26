# polychromae

*of many colours* — a monorepo of composable Python packages for scientific visualisation colour.

[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## Packages

| Package | Description | Install |
|---|---|---|
| **pytochrome** | GoG-informed dark/light style system for matplotlib and Plotly | `uv add pytochrome` |
| **chromophore** | Cross-framework colourmap container — load, convert, preview | `uv add chromophore` |

---

## pytochrome

Named after the plant photoreceptor that switches between two stable states (Pr ↔ Pfr).
Applies style in two orthogonal Grammar of Graphics layers:

- **theme** — non-data ink: axes, grid, fonts, backgrounds
- **aes** — data ink: colour cycle and colourmap defaults

```python
import matplotlib.pyplot as plt
import pytochrome as pc

fig, ax = plt.subplots()
ax.plot([1, 2, 3])

pc.dark(fig)     # full dark style  — Pfr state
pc.light(fig)    # full light style — Pr  state
pc.toggle(fig)   # switch between states

# GoG-separated
pc.theme(fig, "dark")   # structural chrome only
pc.aes(fig, "light")    # colour encodings only

pc.save(fig, "out")     # SVG + PNG, transparent background
```

Access tokens directly:

```python
pc.DARK.aes.cycle            # 8-colour hex tuple
pc.DARK.theme.text_primary   # structural text colour
pc.cmap.dark.sequential      # resolved sequential cmap name
```

Works with **matplotlib** (2D + 3D) and **Plotly**. New backends register via `BackendRegistry`.

---

## chromophore

A single `Colormap` dataclass that converts between frameworks on demand.

```python
from chromophore import Colormap

# From hex — discrete qualitative palette
cm = Colormap.from_hex(
    ["#2D5016", "#7A9E5A", "#D4AF37"], name="forest", discrete=True
)
cm                      # swatch preview in Jupyter
cm.to_matplotlib()      # ListedColormap
cm.to_plotly()          # [[0.0, '#2d5016'], ..., [1.0, '#d4af37']]

# Wrap an existing matplotlib colormap
cm = Colormap.from_matplotlib("viridis")
cm.to_plotly()

# Sample a Plotly colorscale  (requires chromophore[plotly])
cm = Colormap.from_plotly("Plasma", n=11)
cm.to_matplotlib()

# Register with matplotlib (+ reversed _r variant)
cm.register()
```

Optional extras: `chromophore[plotly]`, `chromophore[crameri]`, `chromophore[cmasher]`,
`chromophore[colorcet]`, `chromophore[all]`.

---

## Development

```bash
git clone https://github.com/nfb2021/polychromae
cd polychromae
uv sync
just test        # run all tests
just check       # ruff + ty + tests
just docs        # serve docs locally
```

> Requires [`uv`](https://docs.astral.sh/uv/) and [`just`](https://github.com/casey/just).
