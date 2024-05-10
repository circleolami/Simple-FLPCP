from __future__ import annotations

import copy
from typing import List, TYPE_CHECKING

from operator import add

from Unit.Integer import Integer
from Unit.Operand import Operand

if TYPE_CHECKING:
    from Base.GGate import GGate


class Query(Operand):
    g_gate_ref = []
    coefficient_size = 0

    def __init__(self, query: List[Integer]):
        self.query = query

    def __repr__(self) -> str:
        return f'Query({self.query})'

    def __add__(self, other: Query) -> Query:
        assert len(self.query) == len(other.query)

        res = self.query[:]
        for i in range(len(self.query)):
            res[i] += other.query[i]

        return Query(res)

    def __sub__(self, other: Query) -> Query:
        assert len(self.query) == len(other.query)

        res = self.query[:]
        for i in range(len(self.query)):
            res[i] -= other.query[i]

        return Query(res)

    def __mul__(self, other: Integer) -> Query:
        res = self.query[:]
        for i in range(len(self.query)):
            res[i] *= other

        return Query(res)

    @staticmethod
    def new_interpolate(points: List[Query], r: Integer) -> Query:
        result = [Integer(0) for _ in range(points[0].get_size())]
        for i in range(len(points)):
            term = copy.deepcopy(points[i])
            for j in range(len(points)):
                if i == j:
                    continue
                for k in range(len(term.query)):
                    term.query[k] *= (r + Integer(-j)) * Integer(i - j).invert()
            result = list(map(add, result, term.query))

        return Query(result)

    @staticmethod
    def interpolate(y_values: List[Query], r: Integer):
        n = len(y_values)

        divided_diff = [[Query([Integer(0) for _ in range(y_values[0].get_size())]) for _ in range(n)] for _ in range(n)]
        for i in range(n):
            divided_diff[i][0] = y_values[i]

        for j in range(1, n):
            for i in range(n - j):
                divided_diff[i][j] = (divided_diff[i + 1][j - 1] - divided_diff[i][j - 1]) * Integer(j).invert()

        coefficients = []
        for i in range(n):
            coefficients.append(divided_diff[0][i])

        polynomial_value = Query([Integer(0) for _ in range(y_values[0].get_size())])
        product_term = Integer(1)
        for i in range(n):
            polynomial_value += coefficients[i] * product_term
            product_term *= (r - Integer(i))

        return polynomial_value


    def get_size(self):
        return len(self.query)
