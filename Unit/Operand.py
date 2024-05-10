from abc import *


class Operand(metaclass=ABCMeta):

    @abstractmethod
    def __add__(self, other):
        pass

    @abstractmethod
    def __mul__(self, other):
        pass
