from .BoundedType import BoundedType

from loguru import logger
from typing import Any

class yString(BoundedType):
    __type__: str = str
    __has_children__: bool = False
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
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

    def matches(self, inp: Any) -> bool:
        if not isinstance(inp, str):
            logger.error(f"\n \
                Input <{inp}> is type <{type(inp)}>, expected type {str}\n \
                see traceback below")

        if not self.inbounds(inp):
            logger.error(f"\n \
                Input string <{inp}> length is out of bounds:\n \
                lower: {self.lower if self.lower is not None else 'no lower bound'}\n \
                upper: {self.upper if self.upper is not None else 'no upper bound'}\n \
                received length: {len(inp)}\n \
                see traceback below")
        return isinstance(inp, str) and self.inbounds(inp)