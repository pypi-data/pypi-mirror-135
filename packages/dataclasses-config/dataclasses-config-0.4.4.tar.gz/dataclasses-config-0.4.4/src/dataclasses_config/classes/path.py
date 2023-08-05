import os

from ..decorations import *

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
    A method `dataclasses_config.classes.path.RelPath.apply()` converts this this object to the `dataclasses_config.classes.path.Path` with the given root.
    
    It is a subclass of `str`, and thus any string operations and methods are available here.
    Useful while reading configuration.
    Automatically converted to the absolute path when used inside `dataclasses_config.config.Config`.
    """
    
    def apply(self, root: Path, **kwargs) -> Path:
        r"""
        Converts this this object to the `dataclasses_config.classes.path.Path` with the given root.
        
        Args:
            root: `dataclasses_config.classes.path.Path`.
            **kwargs: Optional.
                If presented, then the resulting Path is then formatted using the `str.format_map()` method.
        
        Returns:
            `dataclasses_config.classes.path.Path`
        
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
        return p
    
    @property
    def as_path(self) -> Path:
        """
        Transforms the `RelPath` object to the absolute `dataclasses_config.classes.path.Path`.
        Returns:
            `dataclasses_config.classes.path.Path`
        """
        
        return Path(self)

__all__ = \
[
    'Path',
    'RelPath',
]
