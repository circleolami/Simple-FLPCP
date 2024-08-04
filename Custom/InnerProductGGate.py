from typing import List
from Base import Gate
from Base.GGate import GGate
from Unit.Operand import Operand

class InnerProductGGate(GGate):
    """
    Compute the inner product of two n-dimensional vectors
    """

    def __init__(self, dim: int, degrees: List[int]):
        assert dim > 1
        self.degrees = degrees  # Store the optimized degrees

        # Initialize with the degrees added to the existing initialization code
        super().__init__([Gate.Add() for _ in range(dim - 1)], [], [Gate.Mul() for _ in range(dim)])

        self.dim = dim

    # Compute the inner product of two vectors
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
    
    # Return the input size of the gate
    def get_input_size(self):
        return self.dim * 2
