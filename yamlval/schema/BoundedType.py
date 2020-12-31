from abc import abstractmethod

from .BaseType import BaseType

from typing import Any, Optional

class BoundedType(BaseType):
    lower: Optional[float] = None
    upper: Optional[float] = None
    
    def __init__(self, lower: Optional[float] = None, upper: Optional[float] = None):
        self.lower = lower
        self.upper = upper
    
    @abstractmethod
    def inbounds(self) -> bool:
        pass