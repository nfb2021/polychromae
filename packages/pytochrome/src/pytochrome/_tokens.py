"""GoG-informed design tokens for pytochrome.

Two orthogonal layers (Wilkinson 2005):

  ThemeTokens  — non-data ink: axes, grid, text, backgrounds
                 (GoG: Coordinates + Guide/Annotation layer)

  AesTokens    — data ink: colour cycle and colourmap names
                 (GoG: Aesthetics layer)

  ModeTokens   — composed from both; one instance per display mode.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ThemeTokens:
    """Non-data ink — structural elements around the data."""

    text_primary: str = ""  # axis labels, title, legend text
    text_secondary: str = ""  # tick labels, minor annotations
    axis: str = ""  # rgba() — spines and axis lines
    grid: str = ""  # rgba() — grid lines, very faint
    accent: str = ""  # brand highlight; not a data encoding


@dataclass(frozen=True)
class AesTokens:
    """Data ink — colour encodings (GoG: Aesthetics layer)."""

    cycle: tuple[str, ...] = field(default_factory=tuple)
    # DARK  → Manim C-level: bright/luminous, pops on dark backgrounds
    # LIGHT → Manim E-level: dark/saturated, high contrast on light backgrounds

    cmap_sequential: str = "viridis"  # monotone continuous; fallback always available
    cmap_diverging: str = "RdBu_r"  # symmetric-around-zero; fallback always available


@dataclass(frozen=True)
class ModeTokens:
    """Complete display mode: theme (structural) + aes (data-ink)."""

    theme: ThemeTokens = field(default_factory=ThemeTokens)
    aes: AesTokens = field(default_factory=AesTokens)


# ---------------------------------------------------------------------------
# DARK mode  — Pfr state (far-red absorbing, active)
# ---------------------------------------------------------------------------

DARK = ModeTokens(
    theme=ThemeTokens(
        text_primary="#E1E6B9",  # canvod-nordic g1 — warm cream
        text_secondary="#C4D4BC",  # light sage — readable on dark
        axis="rgba(255,255,255,0.25)",  # semi-transparent white spine
        grid="rgba(255,255,255,0.07)",  # barely-there white grid
        accent="#ABC8A4",  # canvod-nordic g3
    ),
    aes=AesTokens(
        # Cyber/nordic palette — luminous on dark backgrounds (L=0.77, WCAG 7.7–9.8:1).
        # Two hue sets: DARK uses cool-dominant hues (blues, teals, magenta) with warm
        # accents; LIGHT uses earthy/botanical hues — palettes feel distinct, not just
        # L-shifted versions of each other.
        # CVD note: blues/purples are safe for deuteranopes; ≤2 warm hues (amber, vermilion)
        # distinguish by hue-shift direction under simulation.  Yellow (L=0.82, not 0.77)
        # intentional: yellow needs extra lightness to stay vivid in OKLCH.
        cycle=(
            "#30c8e6",  # sky-blue  H=215°  L=0.77
            "#f99c2a",  # amber     H= 65°  L=0.77
            "#31cfb4",  # teal      H=178°  L=0.77
            "#d596fa",  # magenta   H=312°  L=0.77
            "#7ab9fa",  # indigo    H=250°  L=0.77
            "#fb928f",  # vermilion H= 22°  L=0.77
            "#fb89c2",  # rose      H=350°  L=0.77
            "#e4c22f",  # yellow    H= 95°  L=0.82
        ),
        cmap_sequential="lajolla",  # Crameri cream→brown; pops on dark — falls back to plasma
        cmap_diverging="vik",  # Crameri blue–white–red          — falls back to RdYlBu_r
    ),
)

# ---------------------------------------------------------------------------
# LIGHT mode — Pr state (red absorbing, resting)
# ---------------------------------------------------------------------------

LIGHT = ModeTokens(
    theme=ThemeTokens(
        text_primary="#183128",  # canvod-nordic g5 — deep forest
        text_secondary="#2A3828",  # near-black forest — clearly darker than dark mode
        axis="rgba(0,0,0,0.30)",  # semi-transparent dark spine
        grid="rgba(0,0,0,0.07)",  # barely-there dark grid
        accent="#375D3B",  # canvod-nordic g4
    ),
    aes=AesTokens(
        # Botanical/paper palette — earthy, saturated, high contrast on white (L=0.50,
        # WCAG 5.7–6.7:1).  DIFFERENT hue set from DARK: ocean, crimson, forest, violet,
        # ochre, navy, wine, sage — reads like a scientific journal figure.
        # CVD note: forest+sage both shift to olive under deuteranopia; separated by
        # 38° and use in non-adjacent slots — same trade-off as Paul Tol's Muted N=8.
        cycle=(
            "#167173",  # ocean   H=198°  L=0.50
            "#b3194f",  # crimson H=  8°  L=0.50
            "#167645",  # forest  H=155°  L=0.50
            "#4f49d3",  # violet  H=278°  L=0.50
            "#944e12",  # ochre   H= 55°  L=0.50
            "#156c8e",  # navy    H=230°  L=0.50
            "#9c219c",  # wine    H=328°  L=0.50
            "#5f6b13",  # sage    H=117°  L=0.50
        ),
        cmap_sequential="batlow",  # Crameri dark-blue→peach; reads on white — falls back to viridis
        cmap_diverging="cork",  # Crameri blue–grey–green; balanced     — falls back to RdBu_r
    ),
)

TOKENS: dict[str, ModeTokens] = {"dark": DARK, "light": LIGHT}


def _resolve_cmap(name: str) -> str:
    """Return the colourmap name, falling back if cmcrameri is not installed."""
    _CRAMERI = {
        "batlow",
        "vik",
        "berlin",
        "roma",
        "cork",
        "oslo",
        "davos",
        "hawaii",
        "lapaz",
        "nuuk",
        "tokyo",
        "turku",
        "imola",
        "acton",
        "bilbao",
        "lajolla",
        "broc",
        "lisbon",
        "tofino",
    }
    if name in _CRAMERI:
        try:
            import cmcrameri.cm  # noqa: F401  # ty: ignore[unresolved-import]
        except ImportError:
            fallbacks = {
                "batlow": "viridis",  # LIGHT sequential
                "lajolla": "plasma",  # DARK sequential — cream→brown analogue
                "vik": "RdYlBu_r",  # DARK diverging
                "cork": "RdBu_r",  # LIGHT diverging
            }
            return fallbacks.get(name, "viridis")
    return name
