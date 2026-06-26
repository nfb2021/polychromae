# Scientific Visualization Style System

## Design Specification & Planning Document

> Working document for a custom matplotlib + Plotly style system.
> Status: **Planning** — not yet implemented.

---

## 1. Purpose & Scope

A unified, opinionated style system for scientific Python figures that is:

- **Screen-first** — RGB color space only, no CMYK considerations
- **Dual-mode** — light and dark variants from a single coherent palette
- **Publication-ready** — SVG/PNG export at correct sizes and DPI
- **Colorblind-safe** — every color decision verifiable under all CVD types
- **Branded but functional** — connects visually to the canVODpy Nordic Green identity without sacrificing data legibility

Covers two backends:

1. **Matplotlib** — `.mplstyle` files, applied via `plt.style.use()`
2. **Plotly / Plotly Express** — registered `pio.templates`, applied via `template=` or `px.defaults`

---

## 2. Literature Basis

Key sources informing every decision in this document:

| Source | Key takeaway |
| --- | --- |
| Rougier, Droettboom & Bourne (2014), *PLOS Comp. Bio.* | Every element must earn its place. Reduce ticks, remove chartjunk, adapt to medium |
| Kelleher & Wagener (2011), *Env. Modelling & Software* | Cognitive load from decoration reduces communication |
| Bang Wong (2010–2012), *Nature Methods* — "Points of View" (29 columns) | Practical guidance on color, typography, negative space, axes, layout |
| Okabe & Ito (2008), *Color Universal Design* | Gold-standard 8-color qualitative palette; explicitly endorsed by Nature Methods |
| Fabio Crameri — *Scientific Colour Maps* (v8, 2023) | Perceptually uniform, CVD-safe, citeable sequential and diverging colormaps |
| Thyng et al. (2016), *Oceanography* — cmocean | Physically intuitive colormaps for earth/ocean science variables |
| Nature Research figure specifications (2025) | Font: Arial/Helvetica; RGB; vector preferred; 5–7pt body, 8pt panel labels |

### Core principles extracted

1. **Remove to improve** — default software outputs are overloaded; strip spines, ticks, grids aggressively
2. **Color carries meaning** — sequential for ordered data, diverging for data with a meaningful midpoint, qualitative for categories; never use rainbow/jet
3. **Colorblind safety is mandatory** — 8% of men have red-green CVD; design around it from the start
4. **Medium determines design** — screen figures can use color more freely than print; exploit this
5. **Captions explain; figures show** — don't label the obvious
6. **Maximum 6–8 categories** — beyond 8 distinct colors readers cannot reliably distinguish them

---

## 3. Visual Identity Reference

### canVODpy CSS: "Nordic Green" palette

Exact values from `docs/assets/canvod-nordic.css` in the canVODpy repository.
This is the ground truth — five greens only, no blues.

| Token | Hex | Role |
| --- | --- | --- |
| `--g1` | `#E1E6B9` | Lightest — light mode background, dark mode text/cream |
| `--g2` | `#C4D7A4` | Light sage — light mode surface, dark mode muted text |
| `--g3` | `#ABC8A4` | Mid sage — dark mode links, muted elements |
| `--g4` | `#375D3B` | Deep forest green — primary links, header bg, active elements |
| `--g5` | `#183128` | Darkest — body text on light, deepest shadows |

#### Light mode token mapping

| Token | Value | Notes |
| --- | --- | --- |
| `--bg` | `#E1E6B9` (g1) | Warm lime-sage — site background (not used for plot area) |
| `--surface` | `#C4D7A4` (g2) | Cards, panels |
| `--text` | `#183128` (g5) | Body text |
| `--muted` | `#375D3B` (g4) | Secondary text |
| `--link` | `#375D3B` (g4) | Links, accents |
| `--border` | `#5D7D5B` | Passes WCAG non-text contrast on g1 |

#### Dark mode token mapping

| Token | Value | Notes |
| --- | --- | --- |
| `--bg` | `#0d0d0d` | Near-black (not blue-dark) |
| `--surface` | `#2a2a2a` | Card surfaces |
| `--surface-2` | `#1a1a1a` | Deeper surface |
| `--text` | `#E1E6B9` (g1) | Warm cream — not pure white |
| `--muted` | `#C4D7A4` (g2) | Secondary text |
| `--link` | `#ABC8A4` (g3) | Links in dark mode |
| `--border` | `#555555` | Borders |

### Brand anchor colors for visualization

The site background (`#E1E6B9`) is too warm/lime for plot backgrounds — it would clash with data colors. Plots use neutral white/near-black backgrounds. The green palette is brought in through:

- **House accent (light mode)**: `#375D3B` (g4) — callout markers, highlights, annotation arrows
- **House accent (dark mode)**: `#ABC8A4` (g3) — lighter green, readable on near-black

---

## 4. Font System

### Brand fonts (from CSS)

```css
@import url("https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300..700&family=Fira+Code:wght@300..700&display=swap");
```

The site uses exactly two fonts:

- **Space Grotesk** — geometric display sans-serif; all body, headings, UI
- **Fira Code** — proportional monospace with ligatures; all code blocks

### The contrast problem and its solution

Space Grotesk has strong personality: wide proportions, distinctive terminals, confident optical weight. Using it everywhere in the site and then also for tick labels and axis numbers in figures produces visual monotony — the data layer blends into the editorial layer.

**Solution: use Fira Code for all numeric/data-layer text in figures.**

This is elegant because:

- Fira Code is already a brand font — no third font needed
- Monospace numbers have equal character widths — tick labels align perfectly in columns
- The visual contrast between Space Grotesk (prose/titles) and Fira Code (numbers/data) is immediate and intentional
- It creates a clear "data layer" identity without introducing Inter or Arial

### Two-font hierarchy for figures

| Element | Font | Weight | Size | Rationale |
| --- | --- | --- | --- | --- |
| Figure title | Space Grotesk | Medium (500) | 14 pt | Brand identity; connects figure to site context |
| Axis labels (x/y) | Space Grotesk | Regular (400) | 11 pt | Descriptive — prose-adjacent |
| Tick labels / numbers | Fira Code | Regular (400) | 10 pt | Data layer; monospace alignment; clear contrast |
| Legend text (series names) | Space Grotesk | Regular (400) | 10 pt | Descriptive labels — prose-adjacent |
| Panel labels (a, b, c) | Space Grotesk | Bold (700) | 12 pt | Structural anchors; bridge brand and data |
| Inline annotations | Fira Code | Regular (400) | 9 pt | Numeric values = data layer |
| Text annotations | Space Grotesk | Regular (400) | 9 pt | Explanatory text = prose layer |

### Matplotlib config

```python
# Register fonts (on first use, skill downloads them if not present)
from matplotlib import font_manager
font_manager.fontManager.addfont("SpaceGrotesk-Medium.ttf")
font_manager.fontManager.addfont("FiraCode-Regular.ttf")

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Space Grotesk", "Arial", "Helvetica Neue", "sans-serif"]
plt.rcParams["font.monospace"] = ["Fira Code", "JetBrains Mono", "Consolas", "monospace"]

# Tick labels use monospace
plt.rcParams["xtick.labelsize"] = 10
plt.rcParams["ytick.labelsize"] = 10
# Override tick font per-axis: ax.set_xticklabels(ax.get_xticklabels(), fontfamily="Fira Code")
```

### Plotly config

```python
fig.update_layout(
    title_font=dict(family="Space Grotesk, sans-serif", size=14, weight=500),
    font=dict(family="Space Grotesk, sans-serif", size=11),  # axis labels, legend
    # Tick labels: no direct family override in plotly — handled via global font or per-axis
)
```

---

## 5. Color System

### 5.1 Philosophy

The palette is **Manim-modernised**: the Manim community palette provides a beautiful 5-step tint system (E=darkest → A=lightest) per hue that gives visual coherence. We take the hue families from Manim but:

- Replace the flat `#333333` background with the brand near-black (`#0d0d0d`) for dark mode
- Use neutral white/off-white for light mode plot area (not the site's lime bg)
- Replace the qualitative cycle with Okabe-Ito hue-matched to Manim families for CVD safety
- Remove pure yellow (`#FFFF00`) from cycles; use gold instead
- Add the brand green (`#375D3B` / `#ABC8A4`) as a house accent separate from the data cycle

### 5.2 Transparency principle

**All figures have transparent backgrounds.** Neither the figure frame nor the axes area has a fill color. This makes every figure a portable asset that adapts to whatever background it is placed on — dark page, light page, slide, or PDF.

The two style variants ("dark" and "light") define only **foreground element colors**: text, axis lines, ticks, grid lines, and markers. They are optimised to read clearly against dark or light host backgrounds respectively, and will still be legible against slightly-off backgrounds (deep navy, warm cream, mid-grey) without any change.

```ini
# matplotlib: always set these
figure.facecolor  : none
axes.facecolor    : none
savefig.facecolor : none
savefig.transparent : True
```

```python
# plotly: always set these
fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
)
```

### 5.3 Dark style — foreground elements (for dark host backgrounds)

| Role | Hex | Notes |
| --- | --- | --- |
| Primary text | `#E1E6B9` | Brand g1 cream — warm near-white |
| Secondary text (ticks, minor labels) | `#9aaa8a` | Desaturated g2-adjacent; softer |
| Axis lines / spines | `rgba(255,255,255,0.25)` | Semi-transparent white; adapts to any dark bg |
| Grid lines | `rgba(255,255,255,0.07)` | Very faint; visible on dark, invisible on light |

### 5.4 Light style — foreground elements (for light host backgrounds)

| Role | Hex | Notes |
| --- | --- | --- |
| Primary text | `#183128` | Brand g5 — deep forest |
| Secondary text (ticks, minor labels) | `#5D7D5B` | Brand border color |
| Axis lines / spines | `rgba(0,0,0,0.30)` | Semi-transparent dark; adapts to any light bg |
| Grid lines | `rgba(0,0,0,0.07)` | Very faint; visible on light, invisible on dark |

### 5.4 Qualitative color cycle (data series)

Based on Okabe-Ito (Nature Methods gold standard), reordered to lead with Manim-adjacent teal/blue, adapted per mode.

#### Full Okabe-Ito reference

| Color | Hex | RGB |
| --- | --- | --- |
| Orange | `#E69F00` | 230, 159, 0 |
| Sky Blue | `#56B4E9` | 86, 180, 233 |
| Bluish Green | `#009E73` | 0, 158, 115 |
| Yellow | `#F0E442` | 240, 228, 66 |
| Blue | `#0072B2` | 0, 114, 178 |
| Vermillion | `#D55E00` | 213, 94, 0 |
| Reddish Purple | `#CC79A7` | 204, 121, 167 |
| Black | `#000000` | — |

#### Dark mode cycle (Manim C-variants, Okabe-Ito-safe ordering)

```python
DARK_CYCLE = [
    "#58C4DD",  # 1. Manim BLUE_C      — sky blue, Manim signature
    "#E69F00",  # 2. Okabe-Ito Orange  — warm gold, replaces harsh yellow
    "#5CD0B3",  # 3. Manim TEAL_C      — teal
    "#FC6255",  # 4. Manim RED_C       — coral red (not pure red)
    "#9A72AC",  # 5. Manim PURPLE_C    — soft purple
    "#83C167",  # 6. Manim GREEN_C     — muted green
    "#F0AC5F",  # 7. Manim GOLD_C      — warm amber
    "#CC79A7",  # 8. Okabe-Ito Reddish Purple
]
```

#### Light mode cycle (Manim D/E-variants — darker, readable on white)

```python
LIGHT_CYCLE = [
    "#29ABCA",  # 1. Manim BLUE_D
    "#C78D46",  # 2. Manim GOLD_E      — darker gold
    "#55C1A7",  # 3. Manim TEAL_D
    "#E65A4C",  # 4. Manim RED_D
    "#715582",  # 5. Manim PURPLE_D
    "#77B05D",  # 6. Manim GREEN_D
    "#E1A158",  # 7. Manim GOLD_D
    "#CC79A7",  # 8. Okabe-Ito Reddish Purple (works on both modes)
]
```

**Rules:**

- Never pair colors 4 (red) and 6 (green) directly on the same figure without a shape/dash distinction
- Yellow (`#F0E442`) is excluded from both cycles — fails contrast on white and reads poorly at small marker sizes; substitute gold
- Keep the brand green (`#375D3B` / `#ABC8A4`) reserved for the house accent, not the cycle

### 5.5 House accent (brand green)

Not part of the data cycle. Used for callouts, selected elements, highlights, annotation arrows.

| Mode | Hex | Use |
| --- | --- | --- |
| Dark | `#ABC8A4` (g3) | Highlight bars, annotation arrows, selected points |
| Light | `#375D3B` (g4) | Same |

### 5.6 Full Manim tint ramp (available for manual use)

The full Manim palette provides a 5-step tint per hue (E=darkest, A=lightest), useful for confidence bands, secondary series, or stepped heatmap levels.

| Family | E | D | C | B | A |
| --- | --- | --- | --- | --- | --- |
| Blue | `#1C758A` | `#29ABCA` | `#58C4DD` | `#9CDCEB` | `#C7E9F1` |
| Teal | `#49A88F` | `#55C1A7` | `#5CD0B3` | `#76DDC0` | `#ACEAD7` |
| Green | `#699C52` | `#77B05D` | `#83C167` | `#A6CF8C` | `#C9E2AE` |
| Gold | `#C78D46` | `#E1A158` | `#F0AC5F` | `#F9B775` | `#F7C797` |
| Red | `#CF5044` | `#E65A4C` | `#FC6255` | `#FF8080` | `#F7A1A3` |
| Maroon | `#94424F` | `#A24D61` | `#C55F73` | `#EC92AB` | `#ECABC1` |
| Purple | `#644172` | `#715582` | `#9A72AC` | `#B189C6` | `#CAA3E8` |
| Grey | `#222222` | `#444444` | `#888888` | `#BBBBBB` | `#DDDDDD` |

*Yellow-C (`#FFFF00`) excluded from cycles; use Gold-C (`#F0AC5F`) instead.*

---

## 6. Colormaps

### 6.1 Continuous sequential

For data varying from low to high. Avoid `jet` and `rainbow` — not perceptually uniform, create false boundaries.

#### Primary: Fabio Crameri (via `cmcrameri` or `palettable.scientific`)

All are perceptually uniform, CVD-safe, and citable (Zenodo DOI).

| Name | Character | Best for |
| --- | --- | --- |
| **`batlow`** | Dark blue → green → yellow → orange | General-purpose; the "scientific rainbow"; replaces jet |
| **`oslo`** | Black → blue → white | Temperature, elevation (cold→hot feel) |
| `davos` | Dark blue → white → light yellow | Snow, ice, cold processes |
| `hawaii` | Deep blue → teal → yellow → orange | Multi-variable maps |
| `lapaz` | Dark indigo → teal → cream | Oceanographic depth |
| `nuuk` | Dark teal → light cream | Arctic / polar data |
| `tokyo` | Dark purple → orange → yellow | Urban heat, general purpose |
| `turku` | Dark brown → cream | Soil, sediment |
| `imola` | Dark navy → light yellow | High-contrast mapping |
| `acton` | Light lavender → dark purple | Astrophysics, spectral data |
| `bilbao` | Light pink → dark orange-red | Heat, fire, radiation intensity |
| `lajolla` | White → yellow → dark red | Anomalies on white background |

#### Physical variable colormaps: cmocean (via `cmocean` or `palettable.cmocean`)

Each map is physically intuitive for its named variable.

| Name | Physical variable | Type |
| --- | --- | --- |
| `thermal` | Sea surface temperature | Sequential |
| `haline` | Salinity | Sequential |
| `solar` | Solar irradiance | Sequential |
| `ice` | Sea ice concentration | Sequential |
| `deep` | Ocean depth (shallow→deep) | Sequential |
| `dense` | Water density | Sequential |
| `algae` | Chlorophyll / algae concentration | Sequential |
| `matter` | Particulate matter | Sequential |
| `turbid` | Turbidity | Sequential |
| `speed` | Flow speed | Sequential |
| `amp` | Amplitude / magnitude (always positive) | Sequential |
| `tempo` | Rate / temporal change | Sequential |
| `rain` | Precipitation | Sequential |
| `gray` | Grayscale (overlays) | Sequential |
| `oxy` | Dissolved oxygen (hybrid) | Sequential |
| `topo` | Topography (land + ocean) | Diverging |
| `balance` | Balanced diverging | Diverging |
| `delta` | Diverging (river delta) | Diverging |
| `curl` | Vorticity / curl | Diverging |
| `diff` | Difference maps | Diverging |
| `tarn` | Diverging with white center | Diverging |
| `phase` | Phase / cyclic data (0–2π) | Cyclic |

### 6.2 Continuous diverging

For data with a meaningful midpoint (zero, a reference value, a mean).

| Name | Character | Best for |
| --- | --- | --- |
| **`vik`** (Crameri) | Blue ↔ red, white center | Temperature anomalies, standard deviation |
| **`berlin`** (Crameri) | Dark blue ↔ dark red, white center | Strong divergence, high contrast |
| `roma` (Crameri) | Blue ↔ orange, white center | Asymmetric divergence |
| `cork` (Crameri) | Green ↔ purple, white center | Correlation, wind |
| `broc` (Crameri) | Blue ↔ brown | Soil moisture, ocean–land |
| `lisbon` (Crameri) | Teal ↔ gold | Balanced |
| `tofino` (Crameri) | Blue ↔ green, white center | Sea/land temperature |
| `balance` (cmocean) | Blue ↔ red | Sea level anomaly |
| `RdBu_r` (matplotlib) | Blue ↔ red, white center | Widely recognized fallback |

**Recommended default:** `vik` for general diverging; `berlin` for high-contrast.

**Rule:** Always center diverging colormaps at the actual midpoint (`vmin=-x, vmax=x`). Never let the white center float.

### 6.3 Qualitative

See §5.4. For more than 8 categories use Paul Tol's `muted` (9 colors) or `vibrant` (7 colors).

Paul Tol `vibrant` hex:

```text
#CC6677, #332288, #DDCC77, #117733, #88CCEE, #882255, #44AA99
```

### 6.4 Colorblind safety rules

- Never rely on red+green alone to convey a distinction
- Yellow (`#F0E442`) fails contrast on white — replace with gold
- Verify with a CVD simulator before submission (`colorspacious` or similar)
- Okabe-Ito cycle is safe for protanopia, deuteranopia, and tritanopia
- `batlow` and `vik`/`berlin` are CVD-safe continuous colormaps

---

## 7. Axes, Grid & Layout

### Axis styling

```
spines:          bottom + left only  (top=hidden, right=hidden)
axis line width: 0.8 pt
ticks:           inward
tick width:      0.6 pt
tick length:     4 pt (major), 2 pt (minor)
tick count:      4–5 per axis (AutoLocator with nbins=5)
zero line:       dashed 0.6 pt — only when data crosses zero
```

### Grid

```ini
show:            horizontal gridlines only (no vertical)
linewidth:       0.6 pt
linestyle:       solid
color (dark):    rgba(255,255,255,0.07)  — faint white; invisible on light backgrounds
color (light):   rgba(0,0,0,0.07)       — faint black; invisible on dark backgrounds
z-order:         behind data
```

No box frame. No background color fill — see §5.2.

### Lines & markers

```ini
default line width:         1.5 pt
secondary / reference:      0.8 pt, dashed
confidence band / fill:     same hue A-variant, alpha=0.25
markers:                    size 6 pt, filled, no edge stroke
error bars:                 cap width=3 pt, linewidth=1.0 pt
```

### Subplot spacing

```ini
vertical_spacing:   0.06 (fraction of total height)
horizontal_spacing: 0.08
```

---

## 8. Figure Sizes & Export

### Standard sizes (screen / web)

| Layout | Width | Height | Notes |
| --- | --- | --- | --- |
| Single panel | 700 px | 500 px | Standard result figure |
| Wide timeseries | 1050 px | 380 px | Long x-axis |
| 2-panel horizontal | 1000 px | 450 px | Side-by-side comparison |
| 2-panel vertical | 600 px | 800 px | Stacked panels |
| 4-panel 2×2 | 900 px | 650 px | Multi-variable overview |

In inches for matplotlib (at 100 DPI screen reference): divide px by 100.

### Export formats

| Format | When | Settings |
| --- | --- | --- |
| **SVG** | Always — primary lossless format | `bbox_inches="tight"` |
| **PNG** | Web embedding, slide thumbnails | 150 DPI web / 300 DPI for paper inclusion |
| **PDF** | LaTeX inclusion, submission | Vector; embed fonts |

### Matplotlib export helper (planned)

```python
style.save(fig, "figure_name", formats=["svg", "png"], dpi=150)
# Saves: figure_name.svg + figure_name.png
# Applies tight_layout automatically
# Strips metadata for clean anonymous submission
```

---

## 9. Skill Structure (planned)

```text
science-style/
├── SKILL.md                    # Trigger rules, description, usage
├── __init__.py                 # Public API
├── styles/
│   ├── mpl_light.mplstyle      # Matplotlib light mode
│   └── mpl_dark.mplstyle       # Matplotlib dark mode
├── plotly_templates.py         # Registers pio.templates["science_light"] + ["science_dark"]
├── fonts/
│   └── README.md               # Instructions for Space Grotesk + Fira Code
└── colormaps.py                # References to batlow, vik, Okabe-Ito cycle, etc.
```

### Public API

```python
import science_style as ss

# Apply globally (sets both matplotlib rcParams and plotly pio.templates.default)
ss.apply_dark()
ss.apply_light()

# Individual backends
ss.mpl.apply_dark()
ss.plotly.apply_dark()

# Color access
ss.colors.dark.cycle          # list of 8 hex strings
ss.colors.light.cycle         # list of 8 hex strings
ss.colors.blue.C              # "#58C4DD" — Manim BLUE_C
ss.colors.brand.dark          # "#ABC8A4" — house accent, dark mode (brand g3)
ss.colors.brand.light         # "#375D3B" — house accent, light mode (brand g4)

# Colormaps
ss.cmap.sequential            # "batlow"
ss.cmap.diverging             # "vik"
ss.cmap.qualitative           # returns the 8-color list

# Export
ss.save(fig, "name")                                         # SVG + PNG @ 150 DPI
ss.save(fig, "name", dpi=300, formats=["svg", "png", "pdf"])
```

---

## 10. Open Questions

| # | Question | Options | Status |
| --- | --- | --- | --- |
| 1 | **Skill name** | `science-style`, `rosalia-style`, custom | ❓ open |
| 2 | **Tint ramp API** | A: simple 8-color cycle only / B: full `colors.blue.C` ramp | ❓ open |
| 3 | **Font download** | Download Space Grotesk + Fira Code on first use vs. user installs | ❓ open |
| 4 | **Plotly Express defaults** | Set `px.defaults` automatically on `apply()`? | ❓ open |
| 5 | **cmocean dependency** | Hard dep vs. optional extra (`pip install science-style[cmocean]`) | ❓ open |
| 6 | **Default colormap** | `batlow` (Crameri, needs `cmcrameri`) vs `cividis` (matplotlib built-in, zero deps) | ❓ open |

---

## 11. Decision Log

| Date | Decision | Rationale |
| --- | --- | --- |
| 2026-06-24 | Screen-only, no CMYK | User explicitly stated no print use |
| 2026-06-24 | Manim palette as tint ramp base | "Sleek but dated" — modernise rather than replace |
| 2026-06-24 | Qualitative cycle = Okabe-Ito reordered | Nature Methods gold standard; colorblind-safe |
| 2026-06-24 | Space Grotesk for titles + axis labels | Brand continuity; descriptive text stays in brand font |
| 2026-06-24 | Fira Code for tick labels and numeric annotations | Monospace numbers align cleanly; distinct "data layer" vs. prose layer; already a brand font |
| 2026-06-24 | Transparent figure and axes backgrounds | Figures are portable assets — foreground colors are optimized per mode, but the figure adapts to any host background automatically |
| 2026-06-24 | Grid/axis lines use `rgba()` not opaque hex | Semi-transparent foreground lines work on any dark or light background without hardcoding a specific bg color |
| 2026-06-24 | Dark text = `#E1E6B9` (brand g1 cream) | Matches actual CSS; warm cream instead of pure white |
| 2026-06-24 | `batlow` as default sequential cmap | Perceptually uniform, CVD-safe, the "scientific rainbow" |
| 2026-06-24 | `vik` as default diverging cmap | Blue↔red, white center; clean and well-tested |
| 2026-06-24 | Brand accent = g4 (light) / g3 (dark) | Extracted from CSS; not in data cycle |

---

## 12. Sources & References

- [Ten Simple Rules for Better Figures — Rougier et al., PLOS Comp. Bio. 2014](https://journals.plos.org/ploscompbiol/article?id=10.1371%2Fjournal.pcbi.1003833)
- [Ten Guidelines for Effective Data Visualization — Kelleher & Wagener, 2011](https://www.sciencedirect.com/science/article/abs/pii/S1364815210003270)
- [Points of View columns — Bang Wong / Nature Methods](https://mk.bcgsc.ca/pointsofview/history.mhtml)
- [Okabe-Ito colorblind-safe palette](https://conceptviz.app/blog/okabe-ito-palette-hex-codes-complete-reference)
- [Paul Tol's Color Schemes (SRON)](https://personal.sron.nl/~pault/)
- [Fabio Crameri — Scientific Colour Maps (Zenodo)](https://zenodo.org/records/8409685)
- [cmocean — Beautiful colormaps for oceanography](https://matplotlib.org/cmocean/)
- [palettable — Color palettes for Python](https://jiffyclub.github.io/palettable/)
- [Nature Research Figure Specifications](https://research-figure-guide.nature.com/figures/preparing-figures-our-specifications/)
- [Manim Community color reference](https://docs.manim.community/en/stable/reference/manim.utils.color.manim_colors.html)
- [3b1b/manim default\_config.yml](https://github.com/3b1b/manim/blob/master/manimlib/default_config.yml)
- [canVODpy CSS — Nordic Green palette](https://github.com/nfb2021/canvodpy/blob/main/docs/assets/canvod-nordic.css)
- [Space Grotesk typeface](https://fonts.floriankarsten.com/space-grotesk)
- [Fira Code typeface](https://github.com/tonsky/FiraCode)
