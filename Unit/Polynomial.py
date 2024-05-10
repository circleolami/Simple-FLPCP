from __future__ import annotations

import copy
from typing import List, Union

from gmpy2 import invert

from Unit.Integer import Integer
from Unit.Operand import Operand
from Unit.Query import Query


class Polynomial(Operand):
    def __init__(self, coefficients: List[Integer]):
        assert len(coefficients) > 0

        self.coefficients = coefficients

    def __repr__(self):
        return str(self.coefficients)

    def __add__(self, other: Polynomial) -> Polynomial:
        if len(self.coefficients) > len(other.coefficients):
            res = self.coefficients[:]
            for i in range(len(other.coefficients)):
                res[i] += other.coefficients[i]
        else:
            res = other.coefficients[:]
            for i in range(len(self.coefficients)):
                res[i] += self.coefficients[i]

        length = len(res)
        for i in range(length - 1, -1, -1):
            if res[i] == Integer(0):
                res.pop(i)
            else:
                break

        return Polynomial(res)

    def __mul__(self, other: Union[Polynomial, Integer, Query]) -> Union[Polynomial, Integer]:
        if isinstance(other, Integer):
            res = self.coefficients[:]

            for i in range(len(self.coefficients)):
                res[i] *= other

            for i in range(len(self.coefficients) - 1, -1, -1):
                if res[i] == Integer(0):
                    res.pop(i)
                else:
                    break

            return Polynomial(res)
        elif isinstance(other, Polynomial):
            deg = self.get_degree() + other.get_degree()

            assert deg >= 0

            res = [Integer(0) for _ in range(deg + 1)]
            for i in range(len(self.coefficients)):
                for j in range(len(other.coefficients)):
                    res[i + j] += self.coefficients[i] * other.coefficients[j]

            return Polynomial(res)
        elif isinstance(other, Query):
            assert self.get_degree() + 1 == other.get_size()

            res = Integer(0)
            for i in range(len(self.coefficients)):
                res += self.coefficients[i] * other.query[i]

            return res
        else:
            assert False

    @staticmethod
    def interpolate(points: List[Integer]) -> Polynomial:
        n = len(points)

        assert n >= 1

        A = [[Integer(idx ** i) for i in range(n)] for idx in range(len(points))]
        b = points[:]

        # Solve Ax = b
        coefficients = Polynomial.gauss_elimination(A, b)

        return Polynomial(coefficients)

    def get_degree(self) -> int:
        return len(self.coefficients) - 1

    @staticmethod
    def gauss_elimination(A, b):
        n = len(A)

        # Forward elimination
        for i in range(n):
            for j in range(i + 1, n):
                factor = A[j][i] * A[i][i].invert()
                for k in range(i, n):
                    A[j][k] -= factor * A[i][k]
                b[j] -= factor * b[i]

        # Back substitution
        x = [0] * n
        for i in range(n - 1, -1, -1):
            x[i] = b[i] * A[i][i].invert()
            for j in range(i):
                b[j] -= A[j][i] * x[i]

        return x