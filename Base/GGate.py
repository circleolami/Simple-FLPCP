from abc import *
from typing import List, Union

from Base.Gate import Add, CMul, Mul
from Unit.Integer import Integer
from Unit.Operand import Operand
from Unit.Query import Query


class GGate(metaclass=ABCMeta):
    """
    Base G-gate class. You can inherit from this class to implement your own G-gate.
    """

    def __init__(self, add: List[Add], cmul: List[CMul], mul: List[Mul]):
        assert len(add) + len(cmul) + len(mul) > 0

        self.add = add
        self.cmul = cmul
        self.mul = mul
        self.last_input = []

    def __call__(self, input: List[Union[Operand, Query]]):
        assert len(input) == self.get_input_size()

        self.last_input = input[:]

        if isinstance(input[0], Query):
            for idx, g_gate in enumerate(Query.g_gate_ref):
                if self == g_gate:
                    p_r_query = [Integer(0) for _ in range(input[0].get_size())]
                    a = Integer(1)
                    for i in range(Query.coefficient_size):
                        p_r_query[input[0].get_size() - Query.coefficient_size + i] = a
                        a *= Integer(idx + 1)
                    return Query(p_r_query)
        else:
            return self.compute(input)

    @abstractmethod
    def compute(self, input: List[Operand]):
        pass

    @abstractmethod
    def get_input_size(self):
        pass
