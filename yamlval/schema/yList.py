from loguru import logger
from typing import List, Any, Tuple, Optional

from schema.base_classes.MultiType import MultiType

class yList(MultiType):
    __type__ = list
    def __init__(self, *children, **bounds):
        super().__init__(*children, **bounds)

    def inbounds(self, inp: Any) -> bool:
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
            err += [f"Input list <{inp}> has length out of bounds:\n \
                lower: {self.lower if self.lower is not None else 'no lower bound'}\n \
                upper: {self.upper if self.upper is not None else 'no upper bound'}\n \
                received: {len(inp)}"]
        
        # check internal consistency of children
        # children are the object defining the restrictions placed upon each item 
        # of input

        # yList(yList(...), yString(), yInt, yDict(...))
        for item in inp:
            acceptableTypes: List[Any] = []
            foundProperChild: bool = False
            for child in self.__children__:
                acceptableTypes.append(child.__type__)
                if isinstance(item, child.__type__):
                    foundProperChild = True
                    matches_child, error = child.matches(item)
                    if not matches_child:
                        match = False
                        err += error

            if not foundProperChild:
                match = False
                err += [f"Improper type for item <{item}>. Expected type {acceptableTypes}. Recieved type {type(item)}"]
        
        return (match, err if not match else None)