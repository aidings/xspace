from pathlib import Path
setup_pfile = Path(__file__).parent / 'data' / 'setup.py'
ignore_pfile = Path(__file__).parent / 'data' / '.gitignore'

from ._version import __version__