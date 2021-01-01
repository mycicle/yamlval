from abc import abstractmethod
from typing import Any, Optional

from .BaseType import BaseType

class BoundedType(BaseType):

    def __init__(self, lower: Optional[float] = None, upper: Optional[float] = None):
        self.lower = lower
        self.upper = upper
    
    @abstractmethod
    def inbounds(self) -> bool:
        pass