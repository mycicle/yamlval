from .BoundedType import BoundedType

from loguru import logger
from typing import Any

class yFloat(BoundedType):
    __type__: float = float
    __has_children__: bool = False
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def inbounds(self, inp: float) -> bool:
        inBounds: bool = True
        if self.lower is not None:
            if inp < self.lower:
                inBounds = False

        if self.upper is not None:
            if inp > self.upper:
                inBounds = False
        
        return inBounds

    def matches(self, inp: Any) -> bool:
        if not isinstance(inp, float):
            logger.error(f"\n \
                Input <{inp}> is type <{type(inp)}>, expected type {float}\n \
                see traceback below")
        if not self.inbounds(inp):
            logger.error(f"\n \
                Input float <{inp}> is out of bounds:\n \
                lower: {self.lower if self.lower is not None else 'no lower bound'}\n \
                upper: {self.upper if self.upper is not None else 'no upper bound'}\n \
                received: {inp}\n \
                see traceback below")
        return isinstance(inp, float) and self.inbounds(inp)
