from .BaseType import BaseType

from typing import Any, List
class yAny(BaseType):
    __type__: List[Any] = None
    def __init__(self):
        self.__type__ = self._get_type()

    def matches(self, inp: Any):
        return True

    def _get_type(self) -> List[Any]:
        return [int, float, list, tuple, object]