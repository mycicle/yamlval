from .BoundedMultiType import BoundedMultiType

from .yEnum import yEnum
from .yAny import yAny
from loguru import logger
from typing import Any, List

class yList(BoundedMultiType):
    __type__: list = list

    def __init__(self, *types, **bounds):
        super().__init__(*types, **bounds)
        
        self.anyInput: bool = False
        for child in self.children:
            if isinstance(child, yAny):
                self.anyInput = True

    def inbounds(self, inp: List[Any]) -> bool:
        inBounds: bool = True
        if self.lower is not None:
            if len(inp) < self.lower:
                inBounds = False

        if self.upper is not None:
            if len(inp) > self.upper:
                inBounds = False
        
        return inBounds
    
    def _check_internal_types(self, inp: Any) -> bool:
        pass

    def matches(self, inp: Any) -> bool:

        if not isinstance(inp, list):
            logger.error(f"\n \
                Input <{inp}> is type <{type(inp)}>, expected type {list}\n \
                see traceback below")
        
        if self.anyInput:
            matchingInternalTypes: bool = True
        else:
            matchingInternalTypes: bool = self._check_internal_types(inp)
    
        if not self.inbounds(inp):
            logger.error(f"\n \
                Input list <{inp}> length is out of bounds:\n \
                lower: {self.lower if self.lower is not None else 'no lower bound'}\n \
                upper: {self.upper if self.upper is not None else 'no upper bound'}\n \
                received length: {len(inp)}\n \
                see traceback below")
        
        return isinstance(inp, list) and self.inbounds(inp) and matchingInternalTypes