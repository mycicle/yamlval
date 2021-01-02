from abc import ABCMeta, abstractmethod

from typing import Any, Tuple, List, Optional

class BaseType(metaclass=ABCMeta):
    """
    In retrospect this class may not even be necesarry, but 
    I will leave it in case there is a use for it
    """
    def __init__(self):
        pass

    @abstractmethod
    def matches(self, inp: Any) -> Tuple[bool, Optional[List[str]]]:
        pass

    @property
    @abstractmethod
    def __type__(self):
        pass

    @property
    @abstractmethod
    def __children__(self):
        pass