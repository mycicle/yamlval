from .BoundedMultiType import BoundedMultiType

from .yAny import yAny

from loguru import logger
from typing import Any, Dict

class yDict(BoundedMultiType):
    __type__: dict = dict

    def __init__(self, *type_pairs, **bounds):
        super().__init__(*type_pairs, **bounds)

    
    def inbounds(self, inp: Dict[Any, Any]) -> bool:
        inBounds: bool = True
        if self.lower is not None:
            if len(inp) < self.lower:
                inBounds = False

        if self.upper is not None:
            if len(inp) > self.upper:
                inBounds = False
        
        return inBounds

    def _check_values(self, key, value, type_pair) -> bool:
        pass
        
    def _check_internal_types(self, inp: Any) -> bool:
        pass

    def matches(self, inp: Any) -> bool:

        if not isinstance(inp, dict):
            logger.error(f"\n \
                Input <{inp}> is type <{type(inp)}>, expected type {list}\n \
                see traceback below")
        
        matchingInternalTypes: bool = self._check_internal_types(inp)

        if not self.inbounds(inp):
            logger.error(f"\n \
                Input dict <{inp}> length is out of bounds:\n \
                lower: {self.lower if self.lower is not None else 'no lower bound'}\n \
                upper: {self.upper if self.upper is not None else 'no upper bound'}\n \
                received length: {len(inp)}\n \
                see traceback below")
        
        return isinstance(inp, dict) and self.inbounds(inp) and matchingInternalTypes