from abc import ABCMeta, abstractmethod

from typing import Any
class BaseType:
    def __init__(self):
        pass

    @abstractmethod
    def matches(self, inp: Any) -> bool:
        pass

    @property
    @abstractmethod
    def __type__(self):
        pass

    @property
    @abstractmethod
    def __has_children__(self):
        pass