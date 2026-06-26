"""Tests for GoG-informed design token integrity."""
import re

import pytest

from pytochrome._tokens import DARK, LIGHT, AesTokens, ThemeTokens, _resolve_cmap

_HEX  = re.compile(r"^#[0-9A-Fa-f]{6}([0-9A-Fa-f]{2})?$")
_RGBA = re.compile(r"^rgba\(\d{1,3},\d{1,3},\d{1,3},(0|1|0\.\d+)\)$")


def _is_hex(s: str) -> bool:
    return bool(_HEX.match(s))


def _is_rgba(s: str) -> bool:
    return bool(_RGBA.match(s.replace(" ", "")))


@pytest.mark.parametrize("mode", [DARK, LIGHT])
def test_cycle_length(mode: object) -> None:
    assert len(mode.aes.cycle) == 8


@pytest.mark.parametrize("mode", [DARK, LIGHT])
def test_cycle_valid_hex(mode: object) -> None:
    for color in mode.aes.cycle:
        assert _is_hex(color), f"Invalid hex in cycle: {color!r}"


@pytest.mark.parametrize("mode", [DARK, LIGHT])
def test_text_colors_valid_hex(mode: object) -> None:
    assert _is_hex(mode.theme.text_primary),   f"text_primary: {mode.theme.text_primary!r}"
    assert _is_hex(mode.theme.text_secondary), f"text_secondary: {mode.theme.text_secondary!r}"
    assert _is_hex(mode.theme.accent),         f"accent: {mode.theme.accent!r}"


@pytest.mark.parametrize("mode", [DARK, LIGHT])
def test_rgba_tokens_valid(mode: object) -> None:
    assert _is_rgba(mode.theme.axis), f"axis: {mode.theme.axis!r}"
    assert _is_rgba(mode.theme.grid), f"grid: {mode.theme.grid!r}"


def test_dark_light_cycles_differ() -> None:
    assert set(DARK.aes.cycle) != set(LIGHT.aes.cycle)


def test_mode_tokens_composed() -> None:
    """ModeTokens must be composed of ThemeTokens + AesTokens."""
    assert isinstance(DARK.theme, ThemeTokens)
    assert isinstance(DARK.aes, AesTokens)
    assert isinstance(LIGHT.theme, ThemeTokens)
    assert isinstance(LIGHT.aes, AesTokens)


def test_resolve_cmap_fallback(monkeypatch: pytest.MonkeyPatch) -> None:
    import builtins
    real_import = builtins.__import__

    def mock_import(name: str, *args: object, **kwargs: object) -> object:
        if name == "cmcrameri.cm":
            raise ImportError("no cmcrameri")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", mock_import)
    assert _resolve_cmap("batlow")  == "viridis"   # LIGHT sequential fallback
    assert _resolve_cmap("lajolla") == "plasma"    # DARK sequential fallback
    assert _resolve_cmap("vik")     == "RdYlBu_r"  # DARK diverging fallback
    assert _resolve_cmap("cork")    == "RdBu_r"    # LIGHT diverging fallback
    assert _resolve_cmap("viridis") == "viridis"   # non-Crameri: pass-through
