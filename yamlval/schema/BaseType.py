from abc import ABCMeta, abstractmethod

class BaseType:
    def __init__(self):
        pass

    @abstractmethod
    def matches(self) -> bool:
        pass