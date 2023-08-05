"""
.. include:: ../../README.md
"""

from collections import namedtuple

__title__ = 'dataclasses-config'
__author__ = 'Peter Zaitcev / USSX Hares'
__license__ = 'BSD 2-clause'
__copyright__ = 'Copyright 2020-2022 Peter Zaitcev'
__version__ = '0.4.4'

VersionInfo = namedtuple('VersionInfo', 'major minor micro releaselevel serial')
version_info = VersionInfo(*__version__.split('.'), releaselevel='alpha', serial=0)

from .classes import *
from .config import *
from .decorations import *
from .settings import *

__all__ =  \
[
    'version_info',
    '__title__',
    '__author__',
    '__license__',
    '__copyright__',
    '__version__',
]
__pdoc__ = { }
__pdoc_extras__ = [ ]

submodules = \
[
    classes,
    config,
    decorations,
    settings,
]

for _m in submodules: __all__.extend(_m.__all__)
from ._helpers import create_documentation_index
create_documentation_index(submodules, __name__, __pdoc__, __pdoc_extras__)
del create_documentation_index, submodules
