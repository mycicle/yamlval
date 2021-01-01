from schema.base_classes.BoundedType import BoundedType

from typing import Any, Tuple, List, Optional
class yInt(BoundedType):
    __children__ = None
    __type__ = int
    def __init__(self, **bounds):
        super().__init__(**bounds)
    
    def inbounds(self, inp: Any) -> bool:
        inBounds: bool = True
        if self.lower is not None:
            if inp < self.lower:
                inBounds = False

        if self.upper is not None:
            if inp > self.upper:
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