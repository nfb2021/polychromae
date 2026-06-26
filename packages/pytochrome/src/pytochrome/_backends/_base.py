"""Abstract base class and registry for pytochrome style backends."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from pytochrome._tokens import AesTokens, ModeTokens, ThemeTokens


class StyleBackend(ABC):
    """
    Contract for a pytochrome plotting backend.

    GoG separation — two distinct methods per layer:
      apply_theme  — non-data ink: axes, grid, fonts, backgrounds
      apply_aes    — data ink:    colour cycle and colourmap defaults

    The concrete apply() calls both; backends implement only the two
    abstract methods.  Backends register themselves with BackendRegistry
    at import time; users never call backends directly.
    """

    @abstractmethod
    def apply_theme(self, fig: Any, tokens: ThemeTokens) -> Any:
        """
        Apply structural non-data ink to *fig* (GoG: theme layer).

        Sets axes colours, grid, fonts, backgrounds.  Returns *fig*.
        """

    @abstractmethod
    def apply_aes(self, fig: Any, tokens: AesTokens) -> Any:
        """
        Apply data-ink colour encodings to *fig* (GoG: aesthetics layer).

        Sets the qualitative colour cycle and default colourmap.  Returns *fig*.
        """

    def apply(self, fig: Any, tokens: ModeTokens) -> Any:
        """
        Apply a complete mode: theme + aesthetics.  Returns *fig*.

        This is the convenience entry-point called by pc.dark() / pc.light().
        """
        self.apply_theme(fig, tokens.theme)
        self.apply_aes(fig, tokens.aes)
        from pytochrome._tokens import DARK  # noqa: PLC0415
        BackendRegistry.tag(fig, "dark" if tokens is DARK else "light")
        return fig

    @abstractmethod
    def can_handle(self, fig: Any) -> bool:
        """Return True if this backend can style *fig*."""

    @abstractmethod
    def get_mode(self, fig: Any) -> str | None:
        """Return the mode currently applied to *fig* ('dark', 'light', or None)."""


class BackendRegistry:
    """
    Global registry of StyleBackend instances.

    Backends are checked in registration order; first match wins.
    """

    _backends: list[StyleBackend] = []
    _TAG = "__pytochrome_mode__"

    @classmethod
    def register(cls, backend: StyleBackend) -> None:
        cls._backends.append(backend)

    @classmethod
    def find(cls, fig: Any) -> StyleBackend:
        for backend in cls._backends:
            if backend.can_handle(fig):
                return backend
        raise TypeError(
            f"No pytochrome backend registered for {type(fig).__qualname__}. "
            "Register one with BackendRegistry.register()."
        )

    @classmethod
    def tag(cls, fig: Any, mode: str) -> None:
        try:
            object.__setattr__(fig, cls._TAG, mode)
        except (AttributeError, TypeError):
            fig.__dict__[cls._TAG] = mode

    @classmethod
    def read_tag(cls, fig: Any) -> str | None:
        return getattr(fig, cls._TAG, None) or fig.__dict__.get(cls._TAG)
