import sys
from typing import TYPE_CHECKING

from xspace.core import LazyImporter
from xspace._version import __version__


_import_structure = {
    "index_wraper": ["DatasetIndexWrapper"],
    "evalue_dataset": ["EvalueDataset"]
}

__all__ = [
    "DatasetIndexWrapper",
    "EvalueDataset"
]

# Direct imports for type-checking
if TYPE_CHECKING:
    from .index_wraper import DatasetIndexWrapper
    from .evalue_dataset import EvalueDataset
else:
    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        _import_structure,
        extra_objects={"__version__": __version__},
    )
