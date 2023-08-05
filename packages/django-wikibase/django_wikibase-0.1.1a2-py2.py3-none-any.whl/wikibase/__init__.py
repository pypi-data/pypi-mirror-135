from .version import get_version

VERSION = (0, 1, 1, 'alpha', 2)

__version__ = get_version(VERSION)

from . import expressions  # NOQA
