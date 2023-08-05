"""
.. include:: ../../README.md
"""

from collections import namedtuple

__title__ = 'dataclasses-config'
__author__ = 'Peter Zaitcev / USSX Hares'
__license__ = 'BSD 2-clause'
__copyright__ = 'Copyright 2020-2022 Peter Zaitcev'
__version__ = '0.4.3'

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

_submodules = \
[
    classes,
    config,
    decorations,
    settings,
]

__pdoc__ = { }
for _submodule in _submodules:
    _submodule_name = _submodule.__name__.partition(f'{__name__}.')[-1]
    __all__.extend(_submodule.__all__)
    __pdoc__[_submodule_name] = True
    _submodule.__pdoc__ = getattr(_submodule, '__pdoc__', dict())
    _extras = getattr(_submodule, '__pdoc_extras__', list())
    for _element in _submodule.__all__:
        __pdoc__[_element] = _element in _extras
