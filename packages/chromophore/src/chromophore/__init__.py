"""
chromophore — cross-framework colourmap toolkit.

Load colourmaps from any source, convert between frameworks,
preview natively in Jupyter.

Usage
-----
    from chromophore import Colormap

    # from hex stops
    cm = Colormap.from_hex(["#2D5016", "#7A9E5A", "#D4AF37"], name="forest", discrete=True)
    cm          # gradient or swatch preview in Jupyter

    # wrap an existing matplotlib cmap
    cm = Colormap.from_matplotlib("viridis")
    cm.to_plotly()   # → [[0.0, '#...'], ..., [1.0, '#...']]

    # register with matplotlib
    cm.register()
    import matplotlib.pyplot as plt
    plt.imshow(data, cmap="forest")
"""
from __future__ import annotations

from chromophore._colormap import Colormap

__version__ = "0.1.0"
__all__ = ["Colormap"]
