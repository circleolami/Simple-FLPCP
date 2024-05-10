from __future__ import annotations

import copy
from typing import List, Union

from gmpy2 import mpfr, mpz

from Unit.Integer import Integer
from Unit.Operand import Operand
from Utils.Constant import base


class Query(Operand):

    def __init__(self, query: List[Integer]):
        self.query = query

    def __add__(self, other: Query) -> Query:
        assert len(self.query) == len(other.query)

        res = self.query[:]
        for i in range(len(self.query)):
            res[i] += other.query[i]

        return Query(res)

    def __mul__(self, other: Union[Integer, mpfr, Query]) -> Query:
        if isinstance(other, Integer):
            res = self.query[:]
            for i in range(len(self.query)):
                res[i] *= other

            return Query(res)
        elif isinstance(other, mpfr):
            res = self.query[:]
            for i in range(len(self.query)):
                res[i] *= other

            return Query(res)
        elif isinstance(other, Query):
            return Query(self.query[:])
        else:
            assert False

    @staticmethod
    def interpolate(points: List[Query], r: Integer) -> Query:
        assert r.n >= mpz(len(points)) and len(points) > 0  # For HVZK

        result = Query([Integer(0) for _ in range(points[0].get_size())])
        for i in range(len(points)):
            term: Query = copy.deepcopy(points[i])
            for j in range(len(points)):
                if i != j:
                    term = term * (mpfr((r + Integer(-j)).n, base) / mpfr(i - j, base))
            result = result + term

        return result

    def get_size(self):
        return len(self.query)