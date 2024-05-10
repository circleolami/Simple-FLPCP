from typing import List

from gmpy2 import mpfr, mpz, round_away

from Unit.Integer import Integer
from Unit.Query import Query
from Utils.Constant import base


class Proof:

    def __init__(self, proof: List):
        self.proof = proof

    def __repr__(self) -> str:
        return str(self.proof)

    def __mul__(self, other: Query) -> Integer:
        assert len(self.proof) == len(other.query)

        res = mpfr(0.0, base)
        for i in range(len(self.proof)):
            res += self.proof[i] * other.query[i]

        return Integer(mpz(round_away(res)))

    def get_length(self) -> int:
        return len(self.proof)
