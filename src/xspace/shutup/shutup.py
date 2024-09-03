import warnings as _warnings
from tqdm import TqdmWarning
from PIL.Image import DecompressionBombWarning

_warnings.filterwarnings('ignore', category=FutureWarning)
_warnings.filterwarnings('ignore', category=TqdmWarning)
_warnings.filterwarnings('ignore', category=DecompressionBombWarning)
_warnings.filterwarnings('ignore', category=UserWarning, message='TypedStorage is deprecated')