from typing import List
from Base.Circuit import Circuit
from Custom.InnerProductGGate import InnerProductGGate
from Unit.Operand import Operand
from Unit.Integer import Integer

class ComplexCircuit(Circuit):
    """
    Define a circuit composed of multiple inner product G-gates
    """

    def __init__(self, dim: int):
        degrees = compute_degrees(dim)  # Calculate the optimal degrees for the given dimension using dynamic programming
        # Pass the degrees value when creating InnerProductGGate
        super().__init__(
            [], [], [InnerProductGGate(dim, degrees) for _ in range(2 * dim + 1)]
        )
        self.dim = dim

    # Execute the circuit for the input vector
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
