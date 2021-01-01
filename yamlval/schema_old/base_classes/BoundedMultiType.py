from abc import abstractmethod
from .BoundedType import BoundedType

from typing import List, Any

class BoundedMultiType(BoundedType):
    def __init__(self, *children, **bounds):
        super().__init__(**bounds)
        
        self.children: List[Any] = []
        for child in children:
            self.children.append(child)

        if self.children is not []:
            self.__has_children__ = True
        else:
            self.__has_children__ = False
    
    @abstractmethod
    def _check_internal_types(self, inp: Any) -> bool:
        pass