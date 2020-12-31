from .BaseType import BaseType

from typing import Any

class yAny(BaseType):
    __type__: Any = any
    def __init__(self):
        pass
    def matches(self, inp: Any):
        return True