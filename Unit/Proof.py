from typing import List

from Unit.Integer import Integer
from Unit.Query import Query


class Proof:

    def __init__(self, proof: List[Integer]):
        self.proof = proof

    def __repr__(self) -> str:
        return str(self.proof)

    def __mul__(self, other: Query) -> Integer:
        assert len(self.proof) == len(other.query)

        res = Integer(0)
        for i in range(len(self.proof)):
            res += self.proof[i] * other.query[i]

        return res

    def get_size(self) -> int:
        return len(self.proof)

    def get_byte_size(self) -> int:
        total_bytes = 0
        for p in self.proof:
            total_bytes += p.get_size()
        return total_bytes
