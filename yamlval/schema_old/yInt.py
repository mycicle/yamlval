from .BoundedType import BoundedType

from loguru import logger
from typing import Any

class yInt(BoundedType):
    __type__: int = int
    __has_children: bool = False
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def inbounds(self, inp: int) -> bool:
        inBounds: bool = True
        if self.lower is not None:
            if inp < self.lower:
                inBounds = False

        if self.upper is not None:
            if inp > self.upper:
                inBounds = False
        
        return inBounds

    def matches(self, inp: Any) -> bool:
        if not isinstance(inp, int):
            logger.error(f"\n \
                Input <{inp}> is type <{type(inp)}>, expected type {int}\n \
                see traceback below")
        if not self.inbounds(inp):
            logger.error(f"\n \
                Input int <{inp}> is out of bounds:\n \
                lower: {self.lower if self.lower is not None else 'no lower bound'}\n \
                upper: {self.upper if self.upper is not None else 'no upper bound'}\n \
                received: {inp}\n \
                see traceback below")
        return isinstance(inp, int) and self.inbounds(inp)