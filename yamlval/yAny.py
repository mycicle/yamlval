from typing import Any, Tuple, List, Optional

from .BaseType import BaseType

class yAny(BaseType):
    __children__ = None
    __type__ = None
    def __init__(self):
        self.__type__ = self._get_type()

    def _get_type(self) -> Tuple[Any]:
        output = [int, float, str, list, dict]
        return tuple(output)

    def matches(self, inp: Any) -> Tuple[bool, Optional[List[str]]]:
        match: bool = True
        err: List[str] = []

        if inp is None:
            match = False
            err += [f"Input {inp} is type {type(inp)}, expected type {self.__type__}"]
        
        return (match, err if not match else None)

        