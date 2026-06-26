---
title: polychromae
description: Colour tools for Python — pytochrome and chromophore
---

<div class="hero" markdown>

# polychromae

**Colour tools for Python**

A monorepo of composable packages for scientific visualisation colour:
style systems, colourmap conversion, and cross-framework preview.

[pytochrome :fontawesome-solid-arrow-right:](packages/pytochrome.md){ .md-button .md-button--primary }
[chromophore :fontawesome-solid-arrow-right:](packages/chromophore.md){ .md-button }

</div>

---

## Packages

<div class="grid cards" markdown>

-   :fontawesome-solid-palette: &nbsp; **pytochrome**

    ---

    GoG-informed dark/light style system for matplotlib and Plotly.
    Applies theme (non-data ink) and aesthetics (data ink) independently,
    following Wilkinson's Grammar of Graphics.

    [:octicons-arrow-right-24: Overview](packages/pytochrome.md)

-   :fontawesome-solid-droplet: &nbsp; **chromophore**

    ---

    Cross-framework colourmap container. Load from hex, matplotlib, or
    Plotly; convert in either direction; preview natively in Jupyter.

    [:octicons-arrow-right-24: Overview](packages/chromophore.md)

</div>

---

## Quick start

```bash
uv add pytochrome
uv add chromophore
```

```python
import matplotlib.pyplot as plt
import pytochrome as pc

fig, ax = plt.subplots()
ax.plot([1, 2, 3])
pc.dark(fig)          # apply full dark style
pc.save(fig, "out")   # SVG + PNG, transparent background
```

```python
from chromophore import Colormap

cm = Colormap.from_hex(["#2D5016", "#7A9E5A", "#D4AF37"], name="forest", discrete=True)
cm                    # swatch preview in Jupyter
cm.to_matplotlib()    # ListedColormap
cm.to_plotly()        # [[0.0, '#...'], ..., [1.0, '#...']]
```
