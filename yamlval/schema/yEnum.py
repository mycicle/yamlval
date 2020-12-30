from enum import EnumMeta

from typing import Set, Any

class yEnum:
    def __init__(self, obj: EnumMeta):
        self.obj = obj
        print(type(self.obj))
        if not isinstance(self.obj, EnumMeta):
            raise TypeError(f"Object {self.obj.__name__} is not type Enum")
    
    def has_value(self, value: str) -> bool:
        """
        Return true / false for whether the input is stored as a value in the enum
        """
        return value in self.obj.__members__

    def get_values(self) -> Set[Any]:
        """
        Return a list of the values stored within the enum
        """
        return set(item.value for item in self.obj)

    def matches(self, obj: Any):
        if not isinstance(obj, self.__type__):
            return False
            # raise TypeError(f"Object {obj.__name__} is type {type(obj)}, expected type {self.__type__}")
        return True


    def __type__(self) -> type:
        return type(self.obj)