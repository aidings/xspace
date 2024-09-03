import sys
from typing import TYPE_CHECKING

from xspace.core import LazyImporter
from xspace._version import __version__


_import_structure = {
    "png_hide": ["PNGHide", "PNGMode"],
    "zips": ["zip_files", "unzip_files"],
    "utils": ["module_from_string", "object_from_config"],
    "object_from_config": ["ObjectFromConfig"],
    "xnote": ["XNote"],
    "model_tools": ["ModelTools", "ModelSaver", "ModelTyper"],
    "color_print": ["info", "debug", "error", "print_rainbow", "print_table", "color_print"],
    "timer": ["Timer", "timer"],
    "trainslate": ["Translater", "Language", "ContentLanguage"],
    "markdown": ["Markdown"],
    "config_dict": ["ConfigDict", "UserDict"],
    "csv_evalue_dataset": ["CSVEvalueDataset"],
    "image_tools": ["ImageTypeReader", "ImageFolderReader", "to_pil", "to_npy"],
    "file_dirs": ["FileRoot", "RankFileWriter"],
    "state_dict": ["StateDict"],
    'check_types': ['check_function_input_types'],
    'timeout': ['Timeout'],
    'class_wargs': ['get_class_defaults'],
    'reloader': ['Reloader']
}

__all__ = [
    'PNGHide', 'PNGMode',
    'zip_files', 'unzip_files',
    'module_from_string', 'object_from_config',
    'ObjectFromConfig',
    'info', 'debug', 'error', 'print_rainbow', 'print_table', 'color_print',
    'Timer', 'timer',
    'Markdown',
    'ConfigDict', 'UserDict',
    'ImageTypeReader', 'ImageFolderReader', 'to_pil', 'to_npy',
    'FileRoot', 'RankFileWriter',
    'StateDict',
    'check_function_input_types',
    'Timeout',
    'get_class_defaults',
    'Reloader'
]

# Direct imports for type-checking
if TYPE_CHECKING:
    from .hpng import PNGHide, PNGMode
    from .zips import zip_files, unzip_files
    from .utils import module_from_string, object_from_config
    from .object_from_config import ObjectFromConfig
    from .color_print import info, debug, error, print_rainbow, print_table, color_print
    from .timer import Timer, timer
    from .markdown import Markdown
    from .config import ConfigDict, UserDict
    from .image_tools import ImageTypeReader, ImageFolderReader, to_pil, to_npy
    from .file_dirs import FileRoot, RankFileWriter
    from .state_dict import StateDict
    from .check_types import check_function_input_types
    from .timeout import Timeout
    from .class_wargs import get_class_defaults
    from .reloader import Reloader
else:
    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        _import_structure,
        extra_objects={"__version__": __version__},
    )
