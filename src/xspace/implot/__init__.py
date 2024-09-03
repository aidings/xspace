"""
IPyPlot package gives you a fast and easy way of displaying images in python notebooks environment.
It leverages HTML and IPython package under the hood which makes it very fast and efficient in displaying images.
It works best for images as string URLs to local/external files but it can also be used with numpy.ndarray or PIL.Image image formats as well.
To use it, you just need to add `import ipyplot` to your code and use one of the public functions available from top level module.
Example:
```
import ipyplot

ipyplot.plot_images(images=images, labels=labels, ..)
```
"""  # NOQA E501

import sys as _sys

if 'google.colab' in _sys.modules:  # pragma: no cover
    print(
        """
        WARNING! Google Colab Environment detected!
        You might encounter issues while running in Google Colab environment.
        If images are not displaying properly please try setting `force_b64` param to `True`.
        """  # NOQA E501
    )

import sys
from typing import TYPE_CHECKING

from xspace.core import LazyImporter
from xspace._version import __version__


_import_structure = {
    "_plotting": ["plot_images", "plot_class_tabs", "plot_class_representations", "rgb_to_hex"],
}

__all__ = [
    "plot_images",
    "plot_class_tabs",
    "plot_class_representations",
    "rgb_to_hex",
]

# Direct imports for type-checking
if TYPE_CHECKING:
    from ._plotting import plot_images, plot_class_tabs, plot_class_representations, rgb_to_hex
else:
    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        _import_structure,
        extra_objects={"__version__": __version__},
    )