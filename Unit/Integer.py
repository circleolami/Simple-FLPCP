from __future__ import annotations

import sys
import time
from typing import Union
from gmpy2 import mpz, c_mod, mpz_random, random_state, cmp, next_prime, powmod, invert

from Unit.Operand import Operand


class Integer(Operand):
    __base: mpz = mpz(2)
    __random_state = random_state(int(time.time()))

    @staticmethod
    def set_base(base: Union[mpz, int]):
        assert type(base) is int or type(base) is mpz

        Integer.__base = -mpz(base)

    @staticmethod
    def get_base() -> mpz:
        return -Integer.__base

    @staticmethod
    def get_random(min: mpz = mpz(0)) -> Integer:
        return Integer(mpz_random(Integer.__random_state, Integer.__base - min) + min)

    @staticmethod
    def set_prime(min: mpz):
        Integer.__base = -next_prime(min)

    def __init__(self, n: Union[mpz, int]):
        super().__init__()
        assert type(n) is int or type(n) is mpz

        self.n: mpz = c_mod(n, Integer.__base)

    def invert(self):
        return Integer(invert(self.n, Integer.get_base()))

    def __repr__(self):
        return str(self.n)

    def __add__(self, other: Integer) -> Integer:
        return Integer(c_mod(self.n + other.n, Integer.__base))

    def __sub__(self, other: Integer) -> Integer:
        return Integer(c_mod(self.n - other.n, Integer.__base))

    def __mul__(self, other: Integer) -> Integer:
        return Integer(c_mod(self.n * other.n, Integer.__base))

    def __pow__(self, other: Integer) -> Integer:
        return Integer(powmod(self.n, other.n, Integer.__base))

    def __eq__(self, other: Integer) -> bool:
        return cmp(self.n, other.n) == 0

    def __gt__(self, other):
        return cmp(self.n, other.n) > 0

    def __lt__(self, other):
        return cmp(self.n, other.n) < 0

    def __ge__(self, other):
        return cmp(self.n, other.n) >= 0

    def __le__(self, other):
        return cmp(self.n, other.n) <= 0

    def __ne__(self, other):
        return cmp(self.n, other.n) != 0

    def get_size(self) -> int:
        return sys.getsizeof(self.n)
