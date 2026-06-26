"""Plotly backend — handles go.Figure objects (2D and 3D traces)."""

from __future__ import annotations

from typing import Any

from pytochrome._backends._base import BackendRegistry, StyleBackend
from pytochrome._cmaps import as_plotly_colorscale, is_natural
from pytochrome._tokens import AesTokens, ThemeTokens, _resolve_cmap

_FONT = "Space Grotesk, sans-serif"


# ---------------------------------------------------------------------------
# Template builders — one per GoG layer
# ---------------------------------------------------------------------------


def _axis_defaults(tokens: ThemeTokens, showgrid: bool) -> dict:
    return {
        "color": tokens.text_secondary,
        "gridcolor": tokens.grid,
        "gridwidth": 0.6,
        "linecolor": tokens.axis,
        "linewidth": 0.8,
        "tickcolor": tokens.axis,
        "tickwidth": 0.6,
        "tickfont": {"family": _FONT, "size": 10, "color": tokens.text_secondary},
        "title": {"font": {"family": _FONT, "size": 11, "color": tokens.text_primary}},
        "showgrid": showgrid,
        "zeroline": False,
        "zerolinecolor": tokens.axis,
        "zerolinewidth": 0.6,
        "mirror": False,
    }


def _scene_axis(tokens: ThemeTokens) -> dict:
    return {
        "backgroundcolor": "rgba(0,0,0,0)",
        "color": tokens.text_secondary,
        "gridcolor": tokens.grid,
        "gridwidth": 0.6,
        "linecolor": tokens.axis,
        "linewidth": 0.8,
        "tickcolor": tokens.axis,
        "tickwidth": 0.6,
        "zerolinecolor": tokens.axis,
        "zerolinewidth": 0.6,
        "spikecolor": tokens.text_secondary,
    }


def _build_theme_template(tokens: ThemeTokens) -> dict:
    """Layout keys for structural non-data ink (GoG: theme layer)."""
    return {
        "layout": {
            "paper_bgcolor": "rgba(0,0,0,0)",
            "plot_bgcolor": "rgba(0,0,0,0)",
            "font": {
                "family": _FONT,
                "color": tokens.text_primary,
                "size": 11,
                "weight": 400,
            },
            "title": {
                "font": {
                    "family": _FONT,
                    "color": tokens.text_primary,
                    "size": 14,
                    "weight": 500,
                },
                "pad": {"t": 8, "b": 4},
            },
            "xaxis": _axis_defaults(tokens, showgrid=False),
            "yaxis": _axis_defaults(tokens, showgrid=True),
            "scene": {
                "bgcolor": "rgba(0,0,0,0)",
                "xaxis": _scene_axis(tokens),
                "yaxis": _scene_axis(tokens),
                "zaxis": _scene_axis(tokens),
            },
            "legend": {
                "bgcolor": "rgba(0,0,0,0)",
                "bordercolor": "rgba(0,0,0,0)",
                "borderwidth": 0,
                "font": {"family": _FONT, "size": 10, "color": tokens.text_primary},
            },
            "hoverlabel": {
                "bgcolor": tokens.text_primary,
                "bordercolor": tokens.accent,
                "font": {"family": _FONT, "size": 11, "color": tokens.text_secondary},
                "align": "left",
            },
            "modebar": {
                "bgcolor": "rgba(0,0,0,0)",
                "color": tokens.text_secondary,
                "activecolor": tokens.accent,
            },
        }
    }


def _plotly_colorscale(name: str):
    """Return a Plotly colorscale: list for pytochrome naturals, str otherwise."""
    resolved = _resolve_cmap(name)
    return as_plotly_colorscale(resolved) if is_natural(resolved) else resolved


def _build_aes_template(tokens: AesTokens) -> dict:
    """Layout keys for data-ink colour encodings (GoG: aesthetics layer)."""
    return {
        "layout": {
            "colorway": list(tokens.cycle),
            "colorscale": {
                "sequential": _plotly_colorscale(tokens.cmap_sequential),
                "sequentialminus": _plotly_colorscale(tokens.cmap_sequential),
                "diverging": _plotly_colorscale(tokens.cmap_diverging),
            },
        }
    }


# ---------------------------------------------------------------------------
# Backend
# ---------------------------------------------------------------------------


class PlotlyBackend(StyleBackend):
    """Style backend for Plotly go.Figure objects."""

    def can_handle(self, fig: Any) -> bool:
        try:
            import plotly.graph_objects as go

            return isinstance(fig, go.Figure)
        except ImportError:
            return False

    # ------------------------------------------------------------------
    # GoG: Theme layer — non-data ink
    # ------------------------------------------------------------------

    def apply_theme(self, fig: Any, tokens: ThemeTokens) -> Any:
        """Apply structural layout template (axes, grid, fonts, backgrounds)."""
        import plotly.graph_objects as go
        import plotly.io as pio

        mode = BackendRegistry.read_tag(fig) or "dark"
        name = f"pytochrome_{mode}_theme"
        pio.templates[name] = go.layout.Template(_build_theme_template(tokens))
        fig.update_layout(
            template=name,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )
        return fig

    # ------------------------------------------------------------------
    # GoG: Aesthetics layer — data ink
    # ------------------------------------------------------------------

    def apply_aes(self, fig: Any, tokens: AesTokens) -> Any:
        """Apply colour-encoding template (colorway, colorscale)."""
        import plotly.graph_objects as go
        import plotly.io as pio

        mode = BackendRegistry.read_tag(fig) or "dark"
        name = f"pytochrome_{mode}_aes"
        pio.templates[name] = go.layout.Template(_build_aes_template(tokens))
        fig.update_layout(template=name)
        return fig

    # ------------------------------------------------------------------
    # apply() override — register a single combined template for cleanliness
    # ------------------------------------------------------------------

    def apply(self, fig: Any, tokens: Any) -> Any:
        """Apply complete mode: theme + aes as a single merged template."""
        import plotly.graph_objects as go
        import plotly.io as pio

        from pytochrome._tokens import DARK

        mode = "dark" if tokens is DARK else "light"
        name = f"pytochrome_{mode}"

        # Merge theme + aes into one template so update_layout is called once
        combined = _build_theme_template(tokens.theme)
        aes_part = _build_aes_template(tokens.aes)["layout"]
        combined["layout"].update(aes_part)

        pio.templates[name] = go.layout.Template(combined)
        fig.update_layout(
            template=name,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )
        BackendRegistry.tag(fig, mode)
        return fig

    def get_mode(self, fig: Any) -> str | None:
        return BackendRegistry.read_tag(fig)


# Register at import time
BackendRegistry.register(PlotlyBackend())
