from loguru import logger
from typing import Any, Tuple, Optional, List

from .base_classes.BoundedType import BoundedType

class yString(BoundedType):
    __type__ = str
    __children__ = None

    def __init__(self, **bounds):
        super().__init__(**bounds)
        if self.lower is None:
            self.lower = 0
        
    def inbounds(self, inp: str) -> bool:
        inBounds: bool = True
        if self.lower is not None:
            if len(inp) < self.lower:
                inBounds = False

        if self.upper is not None:
            if len(inp) > self.upper:
                inBounds = False
        
        return inBounds

    def matches(self, inp: Any) -> Tuple[bool, Optional[List[str]]]:
        match: bool = True
        err: List[str] = []
        # check type of inp
        if not isinstance(inp, self.__type__):
            match = False
            err += [f"Input {inp} is type {type(inp)}, expected type {self.__type__}"]

        # check bounds of inp
        if not self.inbounds(inp):
            match = False
            err += [f"Input int <{inp}> is out of bounds:\n \
                lower: {self.lower if self.lower is not None else 'no lower bound'}\n \
                upper: {self.upper if self.upper is not None else 'no upper bound'}\n \
                received: {inp}"]

        # return match and the error list if match is false, 
        # return match and None if match is true
        return (match, err if not match else None)