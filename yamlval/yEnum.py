from enum import EnumMeta
from loguru import logger
from typing import List, Any, Set, Tuple, Optional

from .BaseType import BaseType

class yEnum(BaseType):
    __type__ = None
    __children__ = None
    def __init__(self, obj: EnumMeta):
        """
        Initialze the enum for type checking use
        This will serve as the range of values the field can be
        """
        self.obj: EnumMeta = obj
        if not isinstance(self.obj, EnumMeta):
            raise TypeError(f"Object {self.obj.__name__} is not type {EnumMeta}")

        self.values: List[Any] = []
        for field in self.obj:
            self.values.append(field.value)
        
        self.__type__ = self._get_type()

    def _get_type(self) -> List[Any]:
        output: List[Any] = []
        for val in self.values:
            output.append(type(val))
        return tuple(output)
        
    def get_values(self) -> Set[Any]:
        """
        Return a list of the values stored within the enum
        """
        return set(self.values)

    def matches(self, inp: Any) -> Tuple[bool, Optional[List[str]]]:  
        """
        return true if the input is within the enum given at initialization
        else return false
        """
        match: bool = True
        err: List[str] = []
        # check type of inp
        if not isinstance(inp, self.__type__):
            match = False
            err += [f"Input {inp} is type {type(inp)}, expected type {self.__type__}"]
        
        # check that input is within the enum
        if inp not in self.values:
            match = False
            err += [f"Input <{inp}> not in <{[var for var in self.get_values()]}>\n \
                see traceback below"]

        return (match, err if not match else None)