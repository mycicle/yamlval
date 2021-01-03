from typing import Any, Tuple, List, Optional

from .BaseType import BaseType

class yNone(BaseType):
    __children__ = None
    __type__ = type(None)
    def __init__(self):
        pass

    def matches(self, inp: Any) -> Tuple[bool, Optional[List[str]]]:
        match: bool = True
        err: List[str] = []

        if inp is not None:
            match = False
            err += [f"Input {inp} is type {type(inp)}, expected type {self.__type__}"]
        
        return (match, err if not match else None)
        
        