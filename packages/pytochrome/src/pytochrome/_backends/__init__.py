"""Backend sub-package.

Importing this package registers all built-in backends with BackendRegistry.
The order of imports determines priority: matplotlib is checked before plotly.
"""
from pytochrome._backends._base import BackendRegistry, StyleBackend
from pytochrome._backends._mpl import MatplotlibBackend
from pytochrome._backends._plotly import PlotlyBackend

__all__ = ["BackendRegistry", "MatplotlibBackend", "PlotlyBackend", "StyleBackend"]
