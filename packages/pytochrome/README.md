# p(h)ytochrome

Scientific visualization style system — dark and light themes for matplotlib and Plotly.

```
χρῶμα (chrōma) — Greek for colour
φυτόν (phytón) — plant
Py             — Python
```

Named after the plant photoreceptor that switches between two stable light states
(Pr ↔ Pfr). The `h` is silent in the import; loud in the docs.

```python
import pytochrome as pc

pc.dark(fig)     # bind dark style  — Pfr state
pc.light(fig)    # bind light style — Pr  state
pc.toggle(fig)   # switch states
pc.save(fig, "output")  # SVG + PNG, transparent background

# Aliases for those who know the reference
pc.Pfr(fig)   # dark  — far-red absorbing, active state
pc.Pr(fig)    # light — red absorbing, resting state
```

Works with **matplotlib** (2D + 3D) and **Plotly** out of the box.
New backends register via `BackendRegistry`.

## Design

p(h)ytochrome acts as a **ligand** on figure objects: it binds, changes their
visual conformation, and can dissociate. The data is never touched.
Two token sets — `DARK` (Pfr) and `LIGHT` (Pr) — drive all colour, font,
and transparency decisions. All figures export with transparent backgrounds,
optimised for dark or light host backgrounds independently.
