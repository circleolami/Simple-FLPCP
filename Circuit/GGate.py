from abc import *
from typing import List

from Circuit.Gate import Mul, CMul, Add
from Unit.Operand import Operand


class GGate(metaclass=ABCMeta):

    def __init__(self, add: List[Add], cmul: List[CMul], mul: List[Mul]):
        assert len(add) + len(cmul) + len(mul) > 0

        self.add = add
        self.cmul = cmul
        self.mul = mul
        self.last_input: List[Operand] = []

    def __call__(self, input: List[Operand]):
        assert len(input) == self.get_input_size()

        self.last_input = input[:]
        return self.compute(input)

    @abstractmethod
    def compute(self, input: List[Operand]):
        pass

    @abstractmethod
    def get_input_size(self):
        pass
