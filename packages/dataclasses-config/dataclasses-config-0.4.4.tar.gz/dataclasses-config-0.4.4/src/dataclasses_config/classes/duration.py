from datetime import timedelta
from typing import *

from pytimeparse2 import parse as timeparse

from ..decorations import *

@deserialize_with(ConstructorDataType.String)
class Duration(timedelta):
    """
    A helper class which represents any duration.
    This class is a subclass of standard timedelta.
    
    This class' constructor accepts either:
      
      - Single `int` or `float`: Counts this argument as the seconds
      - Single `str`: Uses the special library `pytimeparse` to parse the duration
      - Normal timedelta arguments (positional or keyword)
    
    Examples:
        ```python
        Duration(1000).total_seconds()              #   1000.0
        Duration('100ms').total_seconds()           #      0.1
        Duration('4 days 5 hours').total_seconds()  # 363600.0
        Duration('2:53').total_seconds()            #    173.0
        ```
    
    WARNING:
        
        1. This module PATCHES the `pytimeparse` library to support milliseconds,
        so it works correctly only with the version 1.1.18
        and only if no other module does so.
        This will be disabled as soon as the
        [Feature Request #22](https://github.com/wroberts/pytimeparse/issues/22) becomes closed.
        
        2. The `pytimeparse` library of version 1.1.8 DO NOT support
        large intervals, such as YEARS and MONTHS.
        This is the subject to to change.
        See [Feature Request #7](https://github.com/wroberts/pytimeparse/issues/7) for details.
    """
    
    @overload
    def __new__(cls: Type['Duration'], arg: str):
        pass
    @overload
    def __new__(cls: Type['Duration'], arg: timedelta):
        pass
    @overload
    def __new__(cls: Type['Duration'], arg: Union[int, float]):
        pass
    @overload
    def __new__(cls: Type['Duration'], *args, **kwargs):
        pass
    
    def __new__(cls: Type['Duration'], *args, **kwargs):
        if (len(args) == 1 and not kwargs):
            arg = args[0]
            
            if (isinstance(arg, timedelta)):
                return super().__new__(cls, seconds=arg.total_seconds())
            elif (isinstance(arg, str)):
                return super().__new__(cls, seconds=timeparse(arg))
            elif (isinstance(arg, (int, float))):
                return super().__new__(cls, seconds=arg)
        
        return super().__new__(cls, *args, **kwargs)

__all__ = \
[
    'Duration',
]
