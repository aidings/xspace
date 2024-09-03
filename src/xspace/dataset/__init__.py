import sys
from typing import TYPE_CHECKING

from xspace.core import LazyImporter
from xspace._version import __version__


_import_structure = {
    "csv_evalue_dataset": ["CSVEvalueDataset"],
    "index_warper": ["DatasetIndexWarpper"],
}

__all__ = [
    "CSVEvalueDataset",
    "DatasetIndexWarpper",
]

# Direct imports for type-checking
if TYPE_CHECKING:
    from .csv_evalue_dataset import CSVEvalueDataset
    from .index_warper import DatasetIndexWarpper
else:
    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        _import_structure,
        extra_objects={"__version__": __version__},
    )