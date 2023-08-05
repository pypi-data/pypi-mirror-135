import os
import warnings
from datetime import timedelta
from importlib import import_module
from types import ModuleType
from typing import *

from pytimeparse2 import parse as timeparse
from typing_inspect import is_generic_type, get_origin, is_optional_type, get_args

from .decorations import *

T = TypeVar('T')
def extract_optional(tp: Union[Type[Optional[T]], Type[T]]) -> Tuple[bool, Type[T]]:
    """
    Helper function that checks if the given type is optional,
    and if it is, expands it.
    Correctly handles both `Union[..., None]` and `Optional[...]` cases.
    
    Args:
        tp: `Type[T]` - potentially optional type.
    
    Returns:
        Returns a tuple of 2 values.
        
        - `bool`: **True** if the given type is `Optional`; **False** otherwise.
        - `Type[R]`: The class *T*, if *T* is not optional; and *R* if *T* is `Optional[R]`.
    
    Examples:
        ```python
        extract_optional(dict)                      # => (False, dict)
        extract_optional(Optional[int])             # => (True,  int)
        extract_optional(MyClass[str])              # => (False, MyClass[str])
        extract_optional(Union[MyClass[str], None]) # => (True,  MyClass[str])
        ```
    """
    
    if (is_optional_type(tp)):
        tp = get_args(tp, evaluate=True)[0]
        return True, tp
    else:
        return False, tp

def extract_generic(tp: Type[T]) -> Tuple[bool, Type[T], Tuple[Type, ...]]:
    """
    Helper function that checks if the given type is generic,
    and if it is, expands it.
    
    Args:
        tp: `Type[T]` - potentially generic type.
    
    Returns:
        Returns a tuple of 3 values.
        
        - `bool`: **True** if the given type is `Generic`; **False** otherwise.
        - `Type[R]`: The class *T*, if *T* is not optional; and *R* if *T* is `Optional[R]`.
        - `Tuple[Type, ...]`: The tuple of class parameters used for *T*'s creation; empty tuple if it is not generic.
    
    Examples:
        ```python
        extract_generic(dict)                      # => (False, dict,    ())
        extract_generic(Dict[A, B])                # => (True,  Dict,    (A, B))
        extract_generic(Optional[int])             # => (True,  Union,   (int, None))
        extract_generic(MyClass[str])              # => (True,  MyClass, (str))
        extract_generic(Union[MyClass[str], None]) # => (True,  Union,   (MyClass[str], None))
        ```
    """
    
    if (is_generic_type(tp)):
        base = get_origin(tp)
        return True, base, get_args(tp, evaluate=True)
    else:
        return False, tp, tuple()

@deserialize_with(ConstructorDataType.String, post_init='_check_class')
class DynamicClass(Generic[T]):
    """
    A helper class which accepts a string class path and imports it.
    Stores both class path and the loaded class.
    
    This class is the generic over `T` - super-class.
    If used inside `dataclasses_config.config.Config` class,
    it would also check that the loaded class is the subclass of `T`.
    
    Raises:
        ImportError: Raised in case of missing module or class in that module.
        TypeError: Raised in case of loaded class not matching the super-class.
    
    Warnings:
        ImportWarning: Sent if the inheritance check is called without specifying the base class.
    
    """
    
    class_path: str
    """`str`. Full class path which could be used for import."""
    
    cls: Type[T]
    """`Type[T]`. An imported and loaded class."""
    
    def __init__(self, class_path: str, *, cls: Type[T] = None):
        self.class_path = class_path
        module_name, _sep, class_name = self.class_path.rpartition('.')
        if (not _sep):
            raise ImportError(f"Cannot import class '{self.class_path}'")
        
        if (cls is None):
            mod: ModuleType = import_module(module_name)
            try:
                self.cls = getattr(mod, class_name)
            except AttributeError as e:
                raise ImportError(f"Cannot import name {class_name!r} from {module_name!r} ({mod.__file__})") from e
        else:
            self.cls = cls
    
    @classmethod
    def from_cls(cls, target_cls: Type[T]) -> 'DynamicClass[T]':
        return cls(class_path=f'{target_cls.__module__}.{target_cls.__name__}', cls=target_cls)
    
    def _check_class(self, tp: Type['DynamicClass[T]'], *args, **kwargs):
        
        _, tp = extract_optional(tp)        
        is_generic, base, type_args = extract_generic(tp)
        if (not is_generic):
            warnings.warn(ImportWarning(f"Type {tp} should be parametrized, but it is not."))
            return
        
        expected_parent = type_args[0]
        if (not issubclass(self.cls, expected_parent)):
            raise TypeError(f"{self.cls!r} is not a subclass of {expected_parent!r} (from {tp!r}).")
    
    def __repr__(self):
        return f'{type(self).__name__}({self.cls!r})'
del T

@deserialize_with(ConstructorDataType.String)
class Path(str):
    r"""
    A helper class which converts any string-like path to the absolute path.
    
    It is a subclass of `str`, and thus any string operations and methods are available here.
    Useful while reading configuration.
    Automatically converted to the absolute path when used inside `dataclasses_config.config.Config`.
    
    Examples:
        ```python
        Path('.')               
        # Something like:
        #   '/home/user/project/test'
        #   'C:\\Users\\user\\Projects\\Test'
        
        Path('my_lib', 'mod.py')
        # Something like:
        #   '/home/user/project/test/my_lib/mod.py'
        #   'C:\\Users\\user\\Projects\\Test\\my_lib\\mod.py'
        
        ```
    """
    
    def __new__(cls, *args, **kwargs):
        return os.path.abspath(os.path.join(*args))

@deserialize_with(ConstructorDataType.String)
class RelPath(str):
    """
    A helper class which represents relative path.
    A method `dataclasses_config.classes.RelPath.apply()` converts this this object to the `dataclasses_config.classes.Path` with the given root.
    
    It is a subclass of `str`, and thus any string operations and methods are available here.
    Useful while reading configuration.
    Automatically converted to the absolute path when used inside `dataclasses_config.config.Config`.
    """
    
    def apply(self, root: Path, **kwargs) -> Path:
        r"""
        Converts this this object to the `dataclasses_config.classes.Path` with the given root.
        
        Args:
            root: `dataclasses_config.classes.Path`.
            **kwargs: Optional.
                If presented, then the resulting Path is then formatted using the `str.format_map()` method.
        
        Returns:
            `dataclasses_config.classes.Path`
        
        Examples:
            ```python
            RelPath('mod.py').apply('.')                                     
            # Something like:
            #   '/home/user/project/test/mod.py'
            #   'C:\\Users\\user\\Projects\\Test\\mod.py'
            
            RelPath('{module_name}/mod.py').apply('my_lib')                  
            # Something like:
            #   '/home/user/project/test/my_lib/{module_name}/mod.py'
            #   'C:\\Users\\user\\Projects\\Test\\my_lib\\{module_name}\\mod.py'
            
            RelPath('{module_name}/mod.py').apply('my_lib', module_name=bin) 
            # Something like:
            #   '/home/user/project/test/my_lib/bin/mod.py'
            #   'C:\\Users\\user\\Projects\\Test\\my_lib\\bin\\mod.py'
            ```
        """
        
        p = Path(root, self)
        if (kwargs):
            p = Path(p.format_map(kwargs))
        # noinspection PyTypeChecker
        return p
    
    @property
    def as_path(self) -> Path:
        """
        Transforms the `RelPath` object to the absolute `dataclasses_config.classes.Path`.
        Returns:
            `dataclasses_config.classes.Path`
        """
        
        # noinspection PyTypeChecker
        return Path(self)

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
    'extract_generic',
    'extract_optional',
    
    'Duration',
    'DynamicClass',
    'Path',
    'RelPath',
]
