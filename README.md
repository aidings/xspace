# xspace

## lazy import
```python
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
```

## create or update a new version
1. use `xproj -u` to update or create a new version
2. use `git add . && git commit -m "message"` to commit changes
3. use `git push origin master` to push changes to remote repository