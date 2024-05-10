from typing import List

from Base.GGate import GGate
from Unit import Integer

from Unit.Operand import Operand
from Unit.Polynomial import Polynomial
from Unit.Proof import Proof
from Unit.Query import Query
from Unit.Integer import Integer as Int


class ParallelSum:
    """
    Parallel-Sum circuit class for fully linear interactive oracle proof.
    """

    def __init__(self, g_gates: List[GGate]):
        assert len(g_gates) > 0

        self.g_gates: List[GGate] = g_gates
        self.last_input_poly: List[Polynomial] = []
        self.last_round_proof: Proof = Proof([])
        self.current_round: int = 0

    def __call__(self, input: List[Operand]):
        assert len(input) == len(self.g_gates) * self.g_gates[0].get_input_size()

        sum = self.g_gates[0](input[0:self.g_gates[0].get_input_size()])
        for i in range(1, len(self.g_gates)):
            sum += self.g_gates[i](input[self.g_gates[0].get_input_size() * i:self.g_gates[0].get_input_size() * (i + 1)])

        return sum

    def get_max_round(self):
        rounds = 0
        count = len(self.g_gates)
        while count % 2 == 0:
            count = count // 2
            rounds += 1
        return rounds

    def get_g_gate_input_size(self):
        return self.g_gates[0].get_input_size()

    def get_g_gate_count(self):
        return len(self.g_gates)

    def make_first_proof(self, inputs: List, is_final: bool = False) -> Proof:
        assert len(inputs) > 0 and self.get_max_round() != 0

        self(inputs)

        randoms = []

        g_gate_input: List[Integer][Integer] = [
            [Int(0) for _ in range(3)] for _ in range(len(inputs) // 2)
        ]

        g_gates_input_size = self.g_gates[0].get_input_size()

        for j in range(len(inputs) // 2):
            g_gate_input[j][0] = Int.get_random()
            randoms.append(g_gate_input[j][0])
            g_gate_number = j // g_gates_input_size
            input_number_per_g_gate = j % g_gates_input_size
            circuit_count_per_g_gate = len(self.g_gates) // 2
            g_gate_input[j][1] = self.g_gates[g_gate_number].last_input[input_number_per_g_gate]
            g_gate_input[j][2] = self.g_gates[g_gate_number + circuit_count_per_g_gate].last_input[input_number_per_g_gate]

        interpolated = [Polynomial.interpolate(g_gate_input[i]) for i in range(len(inputs) // 2)]
        g_gate_poly: Polynomial = self.g_gates[0].compute(interpolated[0:g_gates_input_size])
        for j in range(1, len(self.g_gates) // 2):
            g_gate_poly += self.g_gates[j].compute(interpolated[g_gates_input_size * j:g_gates_input_size * (j + 1)])

        res = []
        if is_final or self.get_max_round() == 1:
            res.extend(inputs)
            res.extend(randoms)
        res.extend(g_gate_poly.coefficients)

        if is_final or self.get_max_round() == 1:
            self.last_input_poly = []
            self.last_round_proof = Proof([])
            self.current_round = 0
            return Proof(res)
        else:
            self.last_input_poly = interpolated
            self.last_round_proof = Proof(res)
            self.current_round = 1
            return self.last_round_proof

    def make_next_proof(self, prev_random: Integer, is_final: bool = False) -> Proof:
        assert self.last_round_proof.get_size() > 0 and self.current_round < self.get_max_round()

        last_input_query = Query([prev_random ** Int(i) for i in range(len(self.last_input_poly[0].coefficients))])

        inputs = []
        prev_input = []
        for i in self.last_input_poly:
            prev_input.append(i * last_input_query)
        for i in range(2 ** self.current_round):
            inputs.extend(prev_input)

        self(inputs)

        randoms = []

        input_count_per_g_gate = len(inputs) // (2 ** (self.current_round + 1))

        g_gate_input: List[Integer][Integer] = [
            [Int(0) for _ in range(3)] for _ in range(input_count_per_g_gate)
        ]

        g_gates_input_size = self.g_gates[0].get_input_size()

        for j in range(input_count_per_g_gate):
            g_gate_input[j][0] = Int.get_random()
            randoms.append(g_gate_input[j][0])
            g_gate_number = j // g_gates_input_size
            input_number_per_g_gate = j % g_gates_input_size
            circuit_count_per_g_gate = len(self.g_gates) // (2 ** (self.current_round + 1))
            for k in range(2):
                g_gate_input[j][k + 1] = self.g_gates[g_gate_number + k * circuit_count_per_g_gate].last_input[
                    input_number_per_g_gate]

        interpolated = [Polynomial.interpolate(g_gate_input[i]) for i in range(input_count_per_g_gate)]
        g_gate_poly: Polynomial = self.g_gates[0].compute(interpolated[0:g_gates_input_size])
        for j in range(1, len(self.g_gates) // (2 ** (self.current_round + 1))):
            g_gate_poly += self.g_gates[j].compute(interpolated[g_gates_input_size * j:g_gates_input_size * (j + 1)])

        res = []
        if is_final or self.get_max_round() == 1:
            res.extend(prev_input)
            res.extend(randoms)
        res.extend(g_gate_poly.coefficients)

        if is_final or self.get_max_round() == 1:
            self.last_input_poly = []
            self.last_round_proof = Proof([])
            self.current_round = 0
            return Proof(res)
        else:
            self.last_input_poly = interpolated
            self.last_round_proof = Proof(res)
            self.current_round += 1
            return self.last_round_proof

    @staticmethod
    def make_p_query(proof_size: int, r: Integer) -> Query:
        return Query([r ** Int(i) for i in range(proof_size)])

    def make_last_queries(self, proof_size: int, r: Integer) -> List[Query]:
        g_gate_input_size = len(self.g_gates) * self.g_gates[0].get_input_size() // (2 ** (self.get_max_round()))
        input_size = g_gate_input_size * 2
        coefficient_size = proof_size - input_size - g_gate_input_size

        input_queries = [Query([Int(0) for _ in range(proof_size)]) for _ in range(input_size)]
        for i in range(input_size):
            input_queries[i].query[i] = Int(1)

        res = []
        for i in range(g_gate_input_size):
            g_gate_input = [Query([Int(1) if k == input_size + i else Int(0) for k in range(proof_size)])]
            for j in range(2):
                g_gate_input.append(input_queries[j * g_gate_input_size + i])
            res.append(Query.interpolate(g_gate_input, r))

        p_r_query = [Int(0) for _ in range(proof_size)]
        a = Int(1)
        for i in range(coefficient_size):
            p_r_query[input_size + g_gate_input_size + i] = a
            a *= r
        res.append(Query(p_r_query))

        p_one_query = [Int(0) for _ in range(proof_size)]
        a = Int(1)
        for i in range(coefficient_size):
            p_one_query[input_size + g_gate_input_size + i] = a
            a *= Int(1)
        res.append(Query(p_one_query))

        p_two_query = [Int(0) for _ in range(proof_size)]
        a = Int(1)
        for i in range(coefficient_size):
            p_two_query[input_size + g_gate_input_size + i] = a
            a *= Int(2)
        res.append(Query(p_two_query))

        return res
