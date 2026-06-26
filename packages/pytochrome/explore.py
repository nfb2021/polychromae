# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo>=0.23",
#     "matplotlib>=3.9",
#     "plotly>=5.24",
#     "numpy>=2.0",
#     "pandas>=2.0",
#     "pytochrome @ file:///Users/work/Developer/pytochrome",
# ]
# ///

import marimo

__generated_with = "0.23.10"
app = marimo.App(width="medium")


@app.cell
def _():
    import importlib

    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    import plotly.graph_objects as go

    import pytochrome._tokens as _tok
    importlib.reload(_tok)
    import pytochrome as _pc
    _pc.DARK = _tok.DARK
    _pc.LIGHT = _tok.LIGHT
    import pytochrome as pc
    DARK, LIGHT = _tok.DARK, _tok.LIGHT

    return DARK, LIGHT, go, mo, np, pc, pd, plt


@app.cell
def _(mo):
    mo.md(r"""
    # p(h)ytochrome · dataset exploration

    **Pr ↔ Pfr** — toggle below to switch light / dark states.
    Matplotlib and Plotly figures both update from the same token set.
    """)
    return


@app.cell
def _(pd):
    penguins = (
        pd.read_csv(
            "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/penguins.csv"
        )
        .dropna()
    )
    return (penguins,)


@app.cell
def _(np, pd):
    _rng = np.random.default_rng(42)
    _years = np.arange(1880, 2025)
    _trend = 0.008 * (_years - 1950) + 0.0003 * (_years - 1950) ** 2
    _cycle = 0.1 * np.sin(2 * np.pi * (_years - 1880) / 11)
    _noise = _rng.normal(0, 0.08, len(_years))
    temp = pd.DataFrame({
        "year": _years,
        "anomaly": _trend + _cycle + _noise - np.mean(_trend),
    })
    return (temp,)


@app.cell
def _(mo):
    mode_switch = mo.ui.switch(label="Light mode", value=False)
    mode_switch
    return (mode_switch,)


@app.cell
def _(DARK, LIGHT, mode_switch, pc, plt):
    tok = LIGHT if mode_switch.value else DARK
    apply_style = pc.light if mode_switch.value else pc.dark

    plt.rcParams["axes.prop_cycle"] = plt.cycler(color=list(tok.aes.cycle))
    plt.rcParams["image.cmap"] = _resolve_cmap(tok.aes.cmap_sequential)
    return apply_style, tok


@app.cell
def _(apply_style, penguins, plt, tok):
    _fig, _ax = plt.subplots(figsize=(6, 4.5))
    for _i, _sp in enumerate(penguins["species"].unique()):
        _d = penguins[penguins["species"] == _sp]
        _ax.scatter(
            _d["flipper_length_mm"],
            _d["body_mass_g"],
            label=_sp,
            color=tok.aes.cycle[_i],
            alpha=0.75,
            s=30,
            linewidths=0,
        )
    _ax.set(
        xlabel="Flipper length (mm)",
        ylabel="Body mass (g)",
        title="Palmer Penguins — flipper vs mass",
    )
    _ax.legend()
    apply_style(_fig)
    _fig
    return


@app.cell
def _(apply_style, plt, temp, tok):
    _fig, _ax = plt.subplots(figsize=(9, 3.5))
    _y = temp["year"].values
    _a = temp["anomaly"].values
    _pos = _a >= 0
    _ax.fill_between(_y, _a, 0, where=_pos, color=tok.aes.cycle[0], alpha=0.45, lw=0)
    _ax.fill_between(_y, _a, 0, where=~_pos, color=tok.aes.cycle[3], alpha=0.45, lw=0)
    _ax.plot(_y, _a, lw=0.8, color=tok.theme.text_secondary)
    _ax.axhline(0, lw=0.6, color=tok.theme.accent)
    _ax.set(
        xlabel="Year",
        ylabel="Anomaly (°C)",
        title="Global temperature anomaly · synthetic",
        xlim=(_y[0], _y[-1]),
    )
    apply_style(_fig)
    _fig
    return


@app.cell
def _(apply_style, np, plt, tok):
    _rng = np.random.default_rng(0)
    _t = np.linspace(0, 4 * np.pi, 300)
    _fig, _ax = plt.subplots(figsize=(8, 3.5))
    for _k in range(len(tok.aes.cycle)):
        _offset = _k * 0.3
        _ax.plot(
            _t,
            np.sin(_t + _offset) + _offset + _rng.normal(0, 0.04, len(_t)),
            lw=1.5,
            label=f"series {_k + 1}",
        )
    _ax.set(xlabel="t", ylabel="amplitude", title="Default colour cycle — 8 series")
    _ax.legend(ncol=4, loc="upper right")
    apply_style(_fig)
    _fig
    return


@app.cell
def _(apply_style, penguins, plt, tok):
    _cols = ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"]
    _corr = penguins[_cols].corr()
    _cmap_div = _resolve_cmap(tok.aes.cmap_diverging)
    _fig, _ax = plt.subplots(figsize=(5, 4.5))
    _im = _ax.imshow(_corr.values, aspect="auto", vmin=-1, vmax=1, cmap=_cmap_div)
    _fig.colorbar(_im, ax=_ax, shrink=0.8)
    _labels = ["bill length", "bill depth", "flipper", "body mass"]
    _ax.set_xticks(range(4))
    _ax.set_xticklabels(_labels, rotation=35, ha="right")
    _ax.set_yticks(range(4))
    _ax.set_yticklabels(_labels)
    _ax.set_title("Penguin correlation — diverging cmap")
    apply_style(_fig)
    _fig
    return


@app.cell
def _(apply_style, go, penguins, tok):
    _fig = go.Figure()
    for _i, _sp in enumerate(penguins["species"].unique()):
        _d = penguins[penguins["species"] == _sp]
        _fig.add_trace(
            go.Scatter(
                x=_d["bill_length_mm"],
                y=_d["bill_depth_mm"],
                mode="markers",
                name=_sp,
                marker=dict(size=7, opacity=0.8, color=tok.aes.cycle[_i]),
            )
        )
    _fig.update_layout(
        title="Palmer Penguins — bill dimensions",
        xaxis_title="Bill length (mm)",
        yaxis_title="Bill depth (mm)",
        height=420,
    )
    apply_style(_fig)
    _fig
    return


@app.cell
def _(apply_style, go, temp, tok):
    _smoothed = temp["anomaly"].rolling(11, center=True).mean()
    _fig = go.Figure(
        [
            go.Scatter(
                x=temp["year"],
                y=temp["anomaly"],
                mode="lines",
                name="Annual",
                line=dict(width=0.8, color=tok.theme.text_secondary),
                opacity=0.5,
            ),
            go.Scatter(
                x=temp["year"],
                y=_smoothed,
                mode="lines",
                name="11-yr mean",
                line=dict(width=2.5, color=tok.aes.cycle[0]),
            ),
        ]
    )
    _fig.update_layout(
        title="Global temperature anomaly · synthetic",
        xaxis_title="Year",
        yaxis_title="Anomaly (°C)",
        height=380,
    )
    apply_style(_fig)
    _fig
    return


@app.cell
def _(apply_style, go, penguins, tok):
    _cmap_seq = _resolve_cmap(tok.aes.cmap_sequential)
    _fig = go.Figure(
        go.Histogram2dContour(
            x=penguins["flipper_length_mm"],
            y=penguins["body_mass_g"],
            colorscale=_cmap_seq,
            contours=dict(coloring="heatmap"),
            showscale=True,
            line=dict(width=0),
            ncontours=20,
        )
    )
    _fig.update_layout(
        title="Penguin density — sequential cmap",
        xaxis_title="Flipper length (mm)",
        yaxis_title="Body mass (g)",
        height=420,
    )
    apply_style(_fig)
    _fig
    return


@app.cell
def _(mo):

    import pathlib as _pl
    _svg = (_pl.Path(__file__).parent / "logo.svg").read_text()
    mo.Html(f'''<div style="background:#12131f;display:inline-block;padding:24px;border-radius:12px">{_svg}</div>''')

    return


@app.cell(hide_code=True)
def _(mo, plt):

    import numpy as _np6
    _rng6   = _np6.random.default_rng(7)
    _t6     = _np6.linspace(0, 4*_np6.pi, 300)
    _dark_cur  = ['#30c8e6', '#f99c2a', '#31cfb4', '#d596fa', '#7ab9fa', '#fb928f', '#fb89c2', '#e4c22f']
    _dark_new  = ['#eebb58', '#8ccc66', '#00c66b', '#00d3ab', '#00d6d2', '#00c2dd', '#25b7ea', '#53b1ff']
    _light_cur = ['#167173', '#b3194f', '#167645', '#4f49d3', '#944e12', '#156c8e', '#9c219c', '#5f6b13']
    _light_new = ['#8b6000', '#316800', '#00610b', '#006142', '#005857', '#00526b', '#004975', '#003d84']
    _names6    = ['sand', 'sage', 'forest', 'moss', 'teal', 'ocean', 'steel', 'navy']

    def _cmp6(cur, new, bg, fg, title):
        _fig, (_l, _r) = plt.subplots(1, 2, figsize=(12, 4.2), facecolor=bg)
        _fig.suptitle(title, color=fg, fontsize=11, fontweight='bold', y=1.01)
        for _ax, _cols, _lbl in [(_l, cur, 'current'), (_r, new, 'natural')]:
            _ax.set_facecolor(bg)
            _ax.set_title(_lbl, color=fg, fontsize=10)
            for _k, _c in enumerate(_cols):
                _ax.plot(_t6,
                         _np6.sin(_t6 + _k*0.4) + _k*0.4 + _rng6.normal(0, 0.04, len(_t6)),
                         lw=2.2, color=_c, label=_names6[_k])
            _ax.legend(fontsize=7.5, ncol=2, loc='upper left',
                       facecolor=bg, labelcolor=fg, edgecolor='none', handlelength=1.2)
            _ax.tick_params(colors=fg, labelsize=8)
            for sp in _ax.spines.values(): sp.set_edgecolor(fg); sp.set_alpha(0.2)
        _fig.tight_layout()
        return _fig

    _fig_dark6  = _cmp6(_dark_cur,  _dark_new,  '#12131f', '#c8c8e0', 'DARK')
    _fig_light6 = _cmp6(_light_cur, _light_new, '#ffffff', '#1a1a2e', 'LIGHT')
    mo.vstack([_fig_dark6, _fig_light6])

    return


@app.cell(hide_code=True)
def _(plt):

    import matplotlib.colors as _mc8
    import matplotlib.patches as _mp8

    _palettes8 = [('Forest Canopy', ('#2D5016', '#7A9E5A', '#5C4033', '#B8C5A0', '#D4AF37')), ('Desert Sunset', ('#CC5500', '#E2725B', '#F4A460', '#C08081', '#5D3A6D')), ('Woodland Trail', ('#01796F', '#8B4513', '#4F7942', '#EAE0C8', '#F5DEB3')), ('Coastal Morning', ('#9DC3E6', '#93E9BE', '#B5A192', '#FFF5EE', '#4682B4')), ('Sunset Glow', ('#FF4500', '#FF69B4', '#967BB6', '#FFD700', '#8B008B')), ('Canyon Sunset', ('#C04000', '#D2691E', '#C2B280', '#8A9A5B', '#4B5F78'))]
    _n8 = len(_palettes8)
    _fig8, _axes8 = plt.subplots(_n8, 1, figsize=(8, _n8 * 1.35), facecolor='#12131f')
    _fig8.subplots_adjust(hspace=0.15)

    for _ax8, (_name8, _stops8) in zip(_axes8, _palettes8):
        _ax8.set_facecolor('#12131f')
        _ax8.set_xlim(0, len(_stops8))
        _ax8.set_ylim(0, 1)
        _ax8.axis('off')

        for _i8, _hex8 in enumerate(_stops8):
            _rect8 = _mp8.FancyBboxPatch(
                (_i8 + 0.06, 0.22), 0.88, 0.66,
                boxstyle='round,pad=0.02',
                facecolor=_hex8, edgecolor='none'
            )
            _ax8.add_patch(_rect8)

            # choose label colour by perceived lightness
            _r8,_g8,_b8 = _mc8.to_rgb(_hex8)
            _lum8 = 0.2126*_r8 + 0.7152*_g8 + 0.0722*_b8
            _lc8 = '#1a1a2e' if _lum8 > 0.35 else '#e8e8f0'

            _ax8.text(_i8 + 0.5, 0.55, _hex8.upper(),
                      ha='center', va='center',
                      fontsize=7.2, fontfamily='monospace',
                      color=_lc8, fontweight='bold')

        _ax8.text(-0.05, 0.55, _name8,
                  ha='right', va='center',
                  fontsize=8.5, color='#c8c8e0',
                  fontfamily='monospace')

    _fig8.suptitle('pytochrome  ·  natural palettes', color='#c8c8e0',
                   fontsize=10, y=0.98, fontfamily='monospace')
    _fig8

    return


if __name__ == "__main__":
    app.run()
