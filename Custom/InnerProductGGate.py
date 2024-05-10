from typing import List

from Base import Gate
from Base.GGate import GGate
from Unit.Operand import Operand


class InnerProductGGate(GGate):
    """
    Perform inner product of two n-dim vector
    """

    def __init__(self, dim: int):
        assert dim > 1

        super().__init__([Gate.Add() for _ in range(dim - 1)], [], [Gate.Mul() for _ in range(dim)])

        self.dim = dim

    def compute(self, input: List[Operand]):
        vec0 = input[:len(input) // 2]
        vec1 = input[len(input) // 2:]

        mid = []

        for i in range(self.dim):
            mid.append(self.mul[i](vec0[i], vec1[i]))

        res = mid[0]
        for i in range(self.dim - 1):
            res = self.add[i](res, mid[i + 1])

        return res

    def get_input_size(self):
        return self.dim * 2