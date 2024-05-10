from abc import *

from Unit.Integer import Integer
from Unit.Operand import Operand


class Gate(metaclass=ABCMeta):
    """
    Base class for all gates.
    """

    @abstractmethod
    def __call__(self, *args, **kwargs):
        pass


class Add(Gate):

    def __call__(self, op0: Operand, op1: Operand) -> Operand:
        return op0 + op1


class CMul(Gate):

    def __init__(self, const: Integer):
        self.const = const

    def __call__(self, op0: Operand) -> Operand:
        return op0 * self.const


class Mul(Gate):

    def __call__(self, op0: Operand, op1: Operand) -> Operand:
        return op0 * op1
