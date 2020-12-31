from .BaseType import BaseType
from enum import EnumMeta
from loguru import logger
from typing import Set, Any, List

class yEnum(BaseType):
    __type__: EnumMeta = EnumMeta
    
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

    def get_values(self) -> Set[Any]:
        """
        Return a list of the values stored within the enum
        """
        return set(self.values)

    def matches(self, inp: Any) -> bool:  
        """
        return true if the input is within the enum given at initialization
        else return false
        """
        if inp not in self.values:
            logger.error(f"\n \
                Input <{inp}> not in <{[var for var in self.get_values()]}>\n \
                see traceback below")
        return inp in self.values