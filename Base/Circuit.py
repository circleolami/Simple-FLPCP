from __future__ import annotations

from abc import *
from typing import List

from Base.GGate import GGate
from Base.Gate import Add, CMul
from Unit import Integer
from Unit.Integer import Integer as Int
from Unit.Operand import Operand
from Unit.Polynomial import Polynomial
from Unit.Query import Query
from Unit.Proof import Proof


class Circuit(metaclass=ABCMeta):
    """
    Base circuit class. You can inherit from this class to implement your own circuit.
    """

    def __init__(self, add: List[Add], cmul: List[CMul], g_gates: List[GGate]):
        assert len(g_gates) > 0  # Must exist at least one G-gate

        for i in range(len(g_gates)):
            if type(g_gates[0]) is not type(g_gates[i]):
                assert False

        self.add = add
        self.cmul = cmul
        self.g_gates = g_gates

    @abstractmethod
    def __call__(self, input: List[Operand]):
        pass

    def make_proof(self, input: List[Integer]) -> Proof:
        assert len(input) > 0

        self(input)

        randoms: List[Integer] = []

        g_gate_input: List[Integer][Integer] = [[Int(0) for _ in range(len(self.g_gates) + 1)] for _ in range(self.g_gates[0].get_input_size())]
        for i in range(self.g_gates[0].get_input_size()):
            g_gate_input[i][0] = Int.get_random()
            randoms.append(g_gate_input[i][0])
            for j in range(len(self.g_gates)):
                g_gate_input[i][j + 1] = self.g_gates[j].last_input[i]

        interpolated = [Polynomial.interpolate(g_gate_input[i]) for i in range(len(g_gate_input))]
        g_gate_poly: Polynomial = self.g_gates[0].compute(interpolated)

        res = []
        res.extend(input)
        res.extend(randoms)
        res.extend(g_gate_poly.coefficients)

        return Proof(res)

    def make_queries(self, input_size: int, proof_size: int, r: Integer) -> List[Query]:
        g_gate_input_size = self.g_gates[0].get_input_size()
        coefficient_size = proof_size - input_size - g_gate_input_size

        queries = [Query([Int(0) for _ in range(proof_size)]) for _ in range(input_size)]
        for i in range(input_size):
            queries[i].query[i] = Int(1)

        Query.g_gate_ref = self.g_gates
        Query.coefficient_size = coefficient_size
        self(queries)

        res = []
        for i in range(g_gate_input_size):
            g_gate_input = [Query([Int(1) if k == input_size + i else Int(0) for k in range(proof_size)])]
            for j in range(len(self.g_gates)):
                g_gate_input.append(self.g_gates[j].last_input[i])
            res.append(Query.interpolate(g_gate_input, r))

        p_r_query = [Int(0) for _ in range(proof_size)]
        a = Int(1)
        for i in range(coefficient_size):
            p_r_query[input_size + g_gate_input_size + i] = a
            a *= r
        res.append(Query(p_r_query))

        p_m_query = [Int(0) for _ in range(proof_size)]
        a = Int(1)
        for i in range(coefficient_size):
            p_m_query[input_size + g_gate_input_size + i] = a
            a *= Int(len(self.g_gates))
        res.append(Query(p_m_query))

        return res

    def get_g_gate_count(self):
        return len(self.g_gates)
