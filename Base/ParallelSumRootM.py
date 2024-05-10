import math
from typing import List

from Base.GGate import GGate
from Unit import Integer

from Unit.Operand import Operand
from Unit.Polynomial import Polynomial
from Unit.Proof import Proof
from Unit.Query import Query
from Unit.Integer import Integer as Int


class ParallelSumRootM:
    """
    Parallel-Sum circuit class for root-M method.
    """

    def __init__(self, g_gates: List[GGate]):
        assert len(g_gates) > 1

        self.g_gates: List[GGate] = g_gates

    def __call__(self, input: List[Operand]):
        assert len(input) == len(self.g_gates) * self.g_gates[0].get_input_size()

        sum = self.g_gates[0](input[0:self.g_gates[0].get_input_size()])
        for i in range(1, len(self.g_gates)):
            sum += self.g_gates[i](input[self.g_gates[0].get_input_size() * i:self.g_gates[0].get_input_size() * (i + 1)])

        return sum

    def get_g_gates_count(self):
        return math.floor(math.sqrt(len(self.g_gates)))

    def make_proof(self, input: List) -> Proof:
        assert len(input) > 0

        self(input)

        randoms: List[Integer] = []

        g_gates_count = math.floor(math.sqrt(len(self.g_gates)))
        g_gate_input_size = self.g_gates[0].get_input_size()

        g_gate_input: List[Integer][Integer] = [[Int(0) for _ in range(g_gates_count + 1)] for _ in
                                                range(g_gate_input_size * g_gates_count)]
        for i in range(g_gate_input_size * g_gates_count):
            g_gate_input[i][0] = Int.get_random()
            randoms.append(g_gate_input[i][0])
            for j in range(g_gates_count):
                g_gate_input[i][j + 1] = self.g_gates[(i // g_gate_input_size) + j * g_gates_count].last_input[i % g_gate_input_size]

        interpolated = [Polynomial.interpolate(g_gate_input[i]) for i in range(g_gate_input_size * g_gates_count)]
        g_gate_poly: Polynomial = self.g_gates[0].compute(interpolated[0:g_gate_input_size])
        for j in range(1, g_gates_count):
            g_gate_poly += self.g_gates[j].compute(interpolated[g_gate_input_size * j:g_gate_input_size * (j + 1)])

        res = []
        res.extend(input)
        res.extend(randoms)
        res.extend(g_gate_poly.coefficients)

        return Proof(res)

    def make_queries(self, proof_size: int, r: Integer) -> List[Query]:
        g_gates_count = math.floor(math.sqrt(len(self.g_gates)))
        g_gate_input_size = self.g_gates[0].get_input_size() * g_gates_count
        input_size = g_gate_input_size * g_gates_count
        coefficient_size = proof_size - input_size - g_gate_input_size

        input_queries = [Query([Int(0) for _ in range(proof_size)]) for _ in range(input_size)]
        for i in range(input_size):
            input_queries[i].query[i] = Int(1)

        res = []
        for i in range(g_gate_input_size):
            g_gate_input = [Query([Int(1) if k == input_size + i else Int(0) for k in range(proof_size)])]
            for j in range(g_gates_count):
                g_gate_input.append(input_queries[j * g_gate_input_size + i])
            res.append(Query.interpolate(g_gate_input, r))

        p_r_query = [Int(0) for _ in range(proof_size)]
        a = Int(1)
        for i in range(coefficient_size):
            p_r_query[input_size + g_gate_input_size + i] = a
            a *= r
        res.append(Query(p_r_query))

        result_query = Query([Int(0) for _ in range(proof_size)])
        for i in range(coefficient_size):
            result_query.query[input_size + g_gate_input_size + i] = Int(1)
        for j in range(2, g_gates_count + 1):
            p_m_query = [Int(0) for _ in range(proof_size)]
            a = Int(1)
            for i in range(coefficient_size):
                p_m_query[input_size + g_gate_input_size + i] = a
                a *= Int(j)
            result_query += Query(p_m_query)
        res.append(result_query)

        return res
