from abc import abstractmethod
from typing import Any, Optional, Tuple

from .BaseType import BaseType
from .BoundedType import BoundedType
from .yAny import yAny

class MultiType(BoundedType):
    __children__: Optional[Tuple[Any]] = None
    __anyType__: Optional[bool] = False
    def __init__(self, *children, **bounds):
        super().__init__(**bounds)
        self.__children__ = children
        if yAny in self.__children__:
            self.__anyType__ = True