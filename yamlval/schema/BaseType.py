from abc import ABCMeta, abstractmethod

class BaseType:
    def __init__(self):
        pass

    @abstractmethod
    def matches(self) -> bool:
        pass

    @property
    @abstractmethod
    def __type__(self):
        pass