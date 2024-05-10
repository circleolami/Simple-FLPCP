from typing import List

from Base.Circuit import Circuit
from Base.Gate import Add, CMul
from Custom.InnerProductGGate import InnerProductGGate
from Unit.Integer import Integer
from Unit.Operand import Operand


class ComplexCircuit(Circuit):
    """
    Consist of many inner product G-gate
    """

    def __init__(self, dim: int):
        super().__init__(
            [Add() for _ in range(4 * dim * dim)],
            [CMul(Integer(i)) for i in range(4 * dim * dim)],
            [InnerProductGGate(dim) for _ in range(2 * dim + 1)]
        )
        self.dim = dim

    def __call__(self, input: List[Operand]):
        assert len(input) == 8 * self.dim * self.dim

        mid0 = []
        for i in range(4 * self.dim):
            vec = []
            for j in range(self.dim):
                vec.append(self.add[self.dim * i + j](input[2 * self.dim * i + j], input[2 * self.dim * i + self.dim + j]))
            for j in range(self.dim):
                vec[j] = self.cmul[self.dim * i + j](vec[j])
            mid0.extend(vec)

        mid1 = []
        for i in range(2 * self.dim):
            mid1.append(self.g_gates[i](mid0[self.dim * i * 2:self.dim * (i * 2 + 2)]))

        return self.g_gates[-1](mid1)
