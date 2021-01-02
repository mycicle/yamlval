from loguru import logger
from typing import List, Any, Tuple, Optional, Dict

from schema.base_classes.MultiType import MultiType
from schema.yEnum import yEnum
class yDict(MultiType):
    __type__ = dict
    def __init__(self, *children, **bounds):
        super().__init__(*children, **bounds)
    
    def inbounds(self, inp: Any) -> bool:
        inBounds: bool = True
        if self.lower is not None:
            if len(inp.keys()) < self.lower:
                inBounds = False

        if self.upper is not None:
            if len(inp.keys()) > self.upper:
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
            err += [f"Input dict <{inp}> has length out of bounds:\n \
                lower: {self.lower if self.lower is not None else 'no lower bound'}\n \
                upper: {self.upper if self.upper is not None else 'no upper bound'}\n \
                received: {len(inp.keys())}"]

        # check internal consistency of children
        # children are the object defining the restrictions placed upon each item 
        # of input

        # yDict(
        #   (key, valuetypes)
        #   (yInt(), yString(), yList(...))
        #   (yEnum(), yList(...), yString(), yInt())
        # )
        # check out the keys
        for key, value in inp.items():
            acceptableKeyTypes: List[Any] = []
            foundProperKeyChild: bool = False

            acceptableValueTypes: List[Any] = []
            foundProperValueChild: bool = False
            for child in self.__children__:
                try:
                    child_key = child[0]
                except TypeError as te:
                    raise ValueError(f"{type(child)} does not support indexing, make sure that the key-value arguments to yDict are wrapped in a tuple!")
                
                if isinstance(child_key, yEnum):
                    raise TypeError(f"Enums within yDict keys are not currently supported. I suggest adding the types expected within the enum as valid key types for the yDict and then checking validity later on.")

                child_values = tuple(child[1:])
                for val in child_values:
                    if isinstance(val, yEnum):
                        raise TypeError(f"Enums within yDict values are not currently supported. I suggest adding the types expected within the enum as valid value types for the yDict and then checking validity later on.")

                child_values_types = tuple([typ.__type__ for typ in child_values])
                acceptableKeyTypes.append(child_key.__type__)
                acceptableValueTypes.append(child_values_types)

                if isinstance(key, child_key.__type__):
                    foundProperKeyChild = True
                    matches_child, error = child_key.matches(key)
                    if not matches_child:
                        match = False
                        err += error
                
                if isinstance(value, child_values_types):
                    try:
                        matching_child_value = child_values[child_values_types.index(type(value))]
                    except Exception as exc:
                        raise ValueError(f"{exc}\nEnums within yDict values are not currently supported. I suggest adding the types expected within the enum as valid value types for the yDict and then checking validity later on.")
                    foundProperValueChild = True
                    matches_child, error = matching_child_value.matches(value)
                    if not matches_child:
                        match = False
                        err += error
                
            if not foundProperKeyChild:
                match = False
                err += [f"Improper key type for kv pair <{key} : {value}>. Expected key-value types <{acceptableKeyTypes} : {acceptableValueTypes}>. Recieved kv types <{type(key)} : {type(value)}>"]
            
            if not foundProperValueChild:
                match = False
                err += [f"Improper value type for kv pair <{key} : {value}>. Expected key-value types <{acceptableKeyTypes} : {acceptableValueTypes}>. Recieved kv types <{type(key)} : {type(value)}>"]

        return (match, err if not match else None)