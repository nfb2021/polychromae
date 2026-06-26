"""Tests for chromophore.Colormap."""
import pytest

from chromophore import Colormap

_HEX5 = ["#2D5016", "#7A9E5A", "#5C4033", "#B8C5A0", "#D4AF37"]


def test_from_hex_continuous() -> None:
    cm = Colormap.from_hex(_HEX5, name="forest")
    assert cm.name == "forest"
    assert cm.colors == _HEX5
    assert not cm.discrete


def test_from_hex_discrete() -> None:
    cm = Colormap.from_hex(_HEX5, name="forest", discrete=True)
    assert cm.discrete


def test_to_matplotlib_continuous() -> None:
    import matplotlib.colors as mcolors

    cm = Colormap.from_hex(_HEX5, name="forest_cont")
    mpl_cm = cm.to_matplotlib()
    assert isinstance(mpl_cm, mcolors.LinearSegmentedColormap)


def test_to_matplotlib_discrete() -> None:
    import matplotlib.colors as mcolors

    cm = Colormap.from_hex(_HEX5, name="forest_disc", discrete=True)
    mpl_cm = cm.to_matplotlib()
    assert isinstance(mpl_cm, mcolors.ListedColormap)


def test_to_plotly_positions() -> None:
    cm = Colormap.from_hex(_HEX5, name="forest")
    scale = cm.to_plotly()
    assert scale[0][0] == 0.0
    assert scale[-1][0] == 1.0
    assert len(scale) == len(_HEX5)


def test_register_with_matplotlib() -> None:
    import matplotlib as mpl

    cm = Colormap.from_hex(_HEX5, name="forest_reg")
    cm.register()
    assert "forest_reg" in mpl.colormaps
    assert "forest_reg_r" in mpl.colormaps


def test_from_matplotlib_roundtrip() -> None:
    cm = Colormap.from_matplotlib("viridis")
    assert cm.name == "viridis"
    assert len(cm.colors) == 256


def test_repr() -> None:
    cm = Colormap.from_hex(_HEX5, name="forest")
    assert "forest" in repr(cm)
    assert "5 stops" in repr(cm)


def test_repr_html_gradient() -> None:
    cm = Colormap.from_hex(_HEX5, name="forest")
    html = cm._repr_html_()
    assert "linear-gradient" in html
    assert "forest" in html


def test_repr_html_swatch() -> None:
    cm = Colormap.from_hex(_HEX5, name="forest", discrete=True)
    html = cm._repr_html_()
    assert "#2D5016" in html
    assert "forest" in html
