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
        output = True
        valtypes = [valtype.__type__ for valtype in type_pair]
        properValueTypes = type(value) in valtypes[1:] # don't include the key
        properIndex = valtypes.index(type(value))
        if not properValueTypes:
            output = False
        else:
            if not type_pair[properIndex].matches(value):
                output = False

        if not properValueTypes:
            logger.error(f"\n \
                The type of value <{value}> in kv pair <{key}:{value}> is {type(value)}, expected type <{[val.__type__ for val in type_pair[1:] for type_pair in self.types]}>")
    
        return output
        
    def _check_internal_types(self, inp: Any) -> bool:
        output: bool = True
        properKeyTypes: bool = False
        skipValueCheck: bool = False
        for key, value in inp.items():
            for type_pair in self.types:
                properKeyTypes = True if isinstance(type_pair[0], yAny) else type(key) == type_pair[0].__type__
                if not properKeyTypes:
                    continue
                else:
                    if not isinstance(type_pair[0], yAny):
                        if not type_pair[0].matches(key):
                            output = False
                    else:
                        for member in type_pair[1:]:
                            if isinstance(member, yAny):
                                skipValueCheck = True
                        if not skipValueCheck:
                            output = self._check_values(key, value, type_pair)
                    break
            
            if not properKeyTypes:
                logger.error(f"\n \
                    The type of key <{key}> in kv pair <{key} : {value}> is {type(key)}, expected type <{[type_pair[0].__type__ for type_pair in self.types]}>")

        return output

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