# pytochrome

GoG-informed dark/light style system for matplotlib and Plotly.

Named after the plant photoreceptor that switches between two stable states (Pr ↔ Pfr).
The `h` is silent in the import; loud in the docs.

```
χρῶμα (chrōma) — Greek for colour
φυτόν (phytón) — plant
Py             — Python
```

---

## Design

pytochrome acts as a **ligand** on figure objects: it binds, changes their visual
conformation, and can dissociate. The data is never touched.

Following Wilkinson's Grammar of Graphics, two orthogonal layers are applied:

| Layer | Function | Controls |
|---|---|---|
| **theme** | `pc.theme(fig)` | axes, grid, fonts, backgrounds — *non-data ink* |
| **aes** | `pc.aes(fig)` | colour cycle, colourmap defaults — *data ink* |
| **combined** | `pc.dark(fig)` / `pc.light(fig)` | both layers at once |

---

## Usage

```python
import matplotlib.pyplot as plt
import pytochrome as pc

fig, ax = plt.subplots()
ax.plot([1, 2, 3])

# Full style — both layers
pc.dark(fig)     # Pfr state — dark background
pc.light(fig)    # Pr  state — light background
pc.toggle(fig)   # switch between states

# GoG-separated
pc.theme(fig, "dark")    # structural ink only — axes, grid, fonts
pc.aes(fig, "light")     # data ink only — cycle and cmap defaults

# Save
pc.save(fig, "output")           # SVG + PNG, transparent background
pc.save(fig, "output", dpi=300)
```

## Token access

```python
pc.DARK.aes.cycle            # 8-colour hex tuple
pc.DARK.theme.text_primary   # structural text colour
pc.colors.dark.cycle         # same, via namespace

pc.cmap.dark.sequential      # resolved sequential cmap name
pc.cmap.light.diverging      # resolved diverging cmap name
```

## Natural colormaps

Six discrete nature-inspired colormaps registered with matplotlib:

```python
ax.imshow(data, cmap=pc.natural_cmaps.forest_canopy)
ax.imshow(data, cmap=pc.natural_cmaps.desert_sunset)
ax.imshow(data, cmap=pc.natural_cmaps.woodland_trail)
ax.imshow(data, cmap=pc.natural_cmaps.coastal_morning)
ax.imshow(data, cmap=pc.natural_cmaps.sunset_glow)
ax.imshow(data, cmap=pc.natural_cmaps.canyon_sunset)
# append _r for reversed variant
```

## Extending with a custom backend

```python
from pytochrome._backends._base import StyleBackend, BackendRegistry
from pytochrome._tokens import ThemeTokens, AesTokens

class MyBackend(StyleBackend):
    @classmethod
    def _TAG(cls): return "mybk"

    def apply_theme(self, fig, tokens: ThemeTokens): ...
    def apply_aes(self, fig, tokens: AesTokens): ...
    def get_mode(self, fig): ...

BackendRegistry.register(MyBackend)
```
