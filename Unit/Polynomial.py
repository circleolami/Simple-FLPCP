from __future__ import annotations

from typing import List, Union

from gmpy2 import mpfr, cmp

from Unit.Integer import Integer
from Unit.Operand import Operand
from Utils.Constant import base


class Polynomial(Operand):
    def __init__(self, coefficients: List[mpfr]):
        assert len(coefficients) > 0

        self.coefficients = coefficients

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
            if cmp(res[i], mpfr(0.0, base)) == 0:
                res.pop(i)
            else:
                break

        return Polynomial(res)

    def __mul__(self, other: Union[Polynomial, Integer]) -> Polynomial:
        if isinstance(other, Integer):
            res = self.coefficients[:]

            for i in range(len(self.coefficients)):
                res[i] *= mpfr(other.n, base)

            for i in range(len(self.coefficients) - 1, -1, -1):
                if cmp(res[i], mpfr(0.0, base)) == 0:
                    res.pop(i)
                else:
                    break

            return Polynomial(res)
        elif isinstance(other, Polynomial):
            deg = self.get_degree() + other.get_degree()

            assert deg >= 0

            res = [mpfr(0.0, base) for _ in range(deg + 1)]
            for i in range(len(self.coefficients)):
                for j in range(len(other.coefficients)):
                    res[i + j] += self.coefficients[i] * other.coefficients[j]

            return Polynomial(res)
        else:
            assert False

    @staticmethod
    def interpolate(points: List[Integer]) -> Polynomial:
        deg = len(points) - 1

        assert deg >= 0

        coefficient = [mpfr(points[i].n, base) for i in range(deg + 1)]
        for i in range(1, deg + 1):
            for j in range(deg, i - 1, -1):
                coefficient[j] = (coefficient[j] - coefficient[j - 1]) / mpfr(i, base)

        return Polynomial(coefficient)

    def get_degree(self) -> int:
        return len(self.coefficients) - 1
