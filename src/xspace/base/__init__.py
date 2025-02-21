import sys
from typing import TYPE_CHECKING

from xspace.core import LazyImporter
from xspace._version import __version__


_import_structure = {
    "hpng": ["PNGHide", "PNGMode"],
    "zips": ["zip_files", "unzip_files", "ZipFileReader"],
    "utils": ["module_from_string", "object_from_config"],
    "object_from_config": ["ObjectFromConfig"],
    "color_print": ["info", "debug", "error", "print_rainbow", "print_table", "color_print"],
    "timer": ["Timer", "timer"],
    "markdown": ["Markdown"],
    "config": ["ConfigDict", "UserDict", 'xconfig'],
    "image_tools": ["ImageTypeReader", "ImageFolderReader", "to_pil", "to_npy", "image2bytes", "ImageMasker", "ImagePaster", "ImageWithMask"],
    "file_dirs": ["FileRoot", "RankFileWriter"],
    "state_dict": ["StateDict"],
    'check_types': ['check_function_input_types'],
    'timeout': ['Timeout'],
    'class_wargs': ['get_class_defaults', 'XKwargs', 'Input2Wargs', 'DefineInputs'],
    'reloader': ['Reloader'],
    'dstruct': ['StrEnum'],
    'dict2attr': ['Dict2Attr'],
    'xnote': ['XNote', 'Image', 'XNoteRow', 'XNoteCol'],
    'product_parameter': ['ProductParameter'],
    'extract_bracket': ['ExtractBrackets'],
    'returns': ['Returns'],
    'list_dict': ['ListDict'],
    'colors': ['Color64', 'COLOR_64']
}

__all__ = [
    'PNGHide', 'PNGMode',
    'zip_files', 'unzip_files', 'ZipFileReader',
    'module_from_string', 'object_from_config',
    'ObjectFromConfig',
    'info', 'debug', 'error', 'print_rainbow', 'print_table', 'color_print',
    'Timer', 'timer',
    'Markdown',
    'ConfigDict', 'UserDict', 'xconfig',
    'ImageTypeReader', 'ImageFolderReader', 'to_pil', 'to_npy', 'image2bytes', 'ImageMasker', 'ImagePaster', 'ImageWithMask',
    'FileRoot', 'RankFileWriter',
    'StateDict',
    'check_function_input_types',
    'Timeout',
    'get_class_defaults', 'XKwargs', 'Input2Wargs', 'DefineInputs',
    'Reloader',
    'StrEnum',
    'Dict2Attr',
    'XNote', 'Image', 'XNoteRow', 'XNoteCol',
    'ProductParameter',
    'ExtractBrackets',
    'Returns',
    'ListDict',
    'Color64', 'COLOR_64'
]

# Direct imports for type-checking
if TYPE_CHECKING:
    from .hpng import PNGHide, PNGMode
    from .zips import zip_files, unzip_files, ZipFileReader
    from .utils import module_from_string, object_from_config
    from .object_from_config import ObjectFromConfig
    from .color_print import info, debug, error, print_rainbow, print_table, color_print
    from .timer import Timer, timer
    from .markdown import Markdown
    from .config import ConfigDict, UserDict, xconfig
    from .image_tools import ImageTypeReader, ImageFolderReader, to_pil, to_npy, image2bytes, ImageMasker, ImagePaster, ImageWithMask
    from .file_dirs import FileRoot, RankFileWriter
    from .state_dict import StateDict
    from .check_types import check_function_input_types
    from .timeout import Timeout
    from .class_wargs import get_class_defaults, XKwargs, Input2Wargs, DefineInputs
    from .reloader import Reloader
    from .dstruct import StrEnum
    from .dict2attr import Dict2Attr
    from .xnote import XNote, Image, XNoteRow, XNoteCol
    from .product_parameter import ProductParameter
    from .extract_bracket import ExtractBrackets
    from .returns import Returns
    from .list_dict import ListDict
    from .colors import Color64, COLOR_64
else:
    sys.modules[__name__] = LazyImporter(
        __name__,
        globals()["__file__"],
        _import_structure,
        extra_objects={"__version__": __version__},
    )
