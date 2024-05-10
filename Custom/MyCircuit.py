from typing import List

from Circuit.Circuit import Circuit
from Custom.MyGGate import MyGGate
from Unit.Operand import Operand


class MyCircuit(Circuit):

    def __init__(self, dim: int):
        super().__init__([], [], [MyGGate(dim)])

    def __call__(self, input: List[Operand]):
        assert len(input) > 1 and len(input) % 2 == 0
        return self.g_gates[0](input)
