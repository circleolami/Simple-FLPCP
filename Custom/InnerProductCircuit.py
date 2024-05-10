from typing import List

from Base.Circuit import Circuit
from Custom.InnerProductGGate import InnerProductGGate
from Unit.Operand import Operand


class InnerProductCircuit(Circuit):
    """
    Consist of one inner product G-gate
    """

    def __init__(self, dim: int):
        super().__init__([], [], [InnerProductGGate(dim)])

    def __call__(self, input: List[Operand]):
        assert len(input) > 1 and len(input) % 2 == 0
        return self.g_gates[0](input)
