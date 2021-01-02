from abc import abstractmethod
from typing import Any, Optional, Tuple

from .BaseType import BaseType
from .BoundedType import BoundedType

class MultiType(BoundedType):
    __children__: Optional[Tuple[Any]] = None

    def __init__(self, *children, **bounds):
        super().__init__(**bounds)
        self.__children__ = children