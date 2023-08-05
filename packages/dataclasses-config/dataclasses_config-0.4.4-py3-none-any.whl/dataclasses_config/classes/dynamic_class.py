import warnings
from dataclasses import field
from importlib import import_module
from types import ModuleType
from typing import *

from ..decorations import *
from .._helpers import extract_optional, extract_generic

T = TypeVar('T')
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
    
    class_path: str = field()
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

__all__ = \
[
    'DynamicClass',
]
