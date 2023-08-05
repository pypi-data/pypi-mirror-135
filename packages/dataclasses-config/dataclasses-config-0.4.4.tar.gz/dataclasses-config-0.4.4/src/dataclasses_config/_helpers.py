from typing import *

from typing_inspect import is_generic_type, get_origin, is_optional_type, get_args

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
del T

def create_documentation_index(submodules: list, __name__: str, __pdoc__: Dict[str, Union[str, bool]], __pdoc_extras__: List[str]):
    for submodule in submodules:
        submodule_name = submodule.__name__.partition(f'{__name__}.')[-1]
        __pdoc__[submodule_name] = True
        submodule_extras = getattr(submodule, '__pdoc_extras__', list())
        for _element in submodule.__all__:
            __pdoc__[_element] = _element in submodule_extras
        __pdoc_extras__.extend(submodule_extras)


__all__ = \
[
    'create_documentation_index',
    'extract_generic',
    'extract_optional',
]
