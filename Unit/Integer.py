from __future__ import annotations

import random
import time
from typing import Union
from gmpy2 import mpz, c_mod, mpz_random, random_state, cmp, next_prime

from Unit.Operand import Operand


class Integer(Operand):
    __base: Union[mpz, int] = mpz(2)

    @staticmethod
    def set_base(base: Union[mpz, int]):
        assert type(base) is int or type(base) is mpz

        Integer.__base = -base

    @staticmethod
    def get_base() -> Union[mpz, int]:
        return Integer.__base

    @staticmethod
    def get_random() -> Integer:
        return Integer(mpz_random(random_state(int(time.time())), Integer.__base))

    @staticmethod
    def set_prime(min: mpz):
        Integer.__base = -next_prime(min)

    def __init__(self, n: Union[mpz, int]):
        super().__init__()
        assert type(n) is int or type(n) is mpz

        self.n: mpz = c_mod(n, Integer.__base)

    def __repr__(self):
        return str(self.n)

    def __add__(self, other: Integer) -> Integer:
        return Integer(c_mod(self.n + other.n, Integer.__base))

    def __mul__(self, other: Integer) -> Integer:
        return Integer(c_mod(self.n * other.n, Integer.__base))

    def __eq__(self, other: Integer) -> bool:
        return cmp(self.n, other.n) == 0
