from abc import abstractmethod
from .BoundedType import BoundedType

from typing import List, Any

class BoundedMultiType(BoundedType):
    def __init__(self, *typs, **bounds):
        super().__init__(**bounds)
        self.types: List[Any] = []
        for typ in typs:
            self.types.append(typ)
    
    @abstractmethod
    def _check_internal_types(self, inp: Any) -> bool:
        pass