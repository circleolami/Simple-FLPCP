import math
from datetime import datetime

from gmpy2.gmpy2 import mpz

from Base.ParallelSum import ParallelSum
from Custom.InnerProductGGate import InnerProductGGate
from Unit.Integer import Integer


def test_inner_product_parallel_sum(dim: int, circuit_count: int, verbose: bool = True):
    """
    Test inner product parallel-sum circuit with recursive linear IOP

    :param dim: each circuit perform inner product with two dimension-dim vectors
    :param circuit_count: the number of inner product circuit
    :param verbose: whether printing information or not
    :return: tuple(is_accepted, verifier_time, prover_time, total_proof_size, query_count)
    """

    Integer.set_prime(mpz(2) ** 127)
    input_vec = [Integer(i) for i in range(dim * 2 * circuit_count)]

    parallel_circuit: ParallelSum = ParallelSum([InnerProductGGate(dim=dim) for _ in range(circuit_count)])

    prover_time = 0
    verifier_time = 0

    start = datetime.now()
    calc_result = parallel_circuit(input_vec)
    end = datetime.now()
    prover_time += (end - start).total_seconds()

    is_accepted = True

    if parallel_circuit.get_max_round() == 1:
        start = datetime.now()
        proof = parallel_circuit.make_first_proof(input_vec, True)
        end = datetime.now()
        prover_time += (end - start).total_seconds()

        start = datetime.now()
        r = Integer.get_random(mpz(3))
        queries = parallel_circuit.make_last_queries(proof.get_size(), r)
        end = datetime.now()
        verifier_time += (end - start).total_seconds()

        start = datetime.now()
        validation = []
        for i in range(len(queries) - 3):
            validation.append(proof * queries[i])
        end = datetime.now()
        prover_time += (end - start).total_seconds()

        start = datetime.now()
        g_gate = [InnerProductGGate(dim) for _ in range(circuit_count // 2)]
        g_r = Integer(0)
        for i in range(circuit_count // 2):
            g_r += g_gate[i](validation[i * (g_gate[0].get_input_size()): (i + 1) * (g_gate[0].get_input_size())])
        end = datetime.now()
        verifier_time += (end - start).total_seconds()

        start = datetime.now()
        is_accepted &= (proof * queries[-3] == g_r)
        is_accepted &= (proof * queries[-1] + proof * queries[-2] == calc_result)
        end = datetime.now()
        prover_time += (end - start).total_seconds()

        if verbose:
            print('-------------------------------------------')
            print(f'Circuit: perform inner product of two {dim}-dim vector (x {circuit_count})')
            print('Accepted!' if is_accepted else 'Rejected!')
            print('Verifier elapsed time(ms): ', verifier_time * 1000)
            print('Prover elapsed time(ms): ', prover_time * 1000)
            print('Proof length: ', proof.get_size())
            print('Query complexity: ', len(queries))
            print('Soundness error: ', (proof.get_size() - 1 - len(input_vec) - parallel_circuit.get_g_gate_count()) / (
                        Integer.get_base() - parallel_circuit.get_g_gate_count()))
            print('-------------------------------------------')

        assert is_accepted

        return is_accepted, verifier_time * 1000, prover_time * 1000, proof.get_size(), len(queries)
    else:
        total_proof_length = 0
        total_query_length = 0

        start = datetime.now()
        proof = parallel_circuit.make_first_proof(input_vec)
        end = datetime.now()
        prover_time += (end - start).total_seconds()
        total_proof_length += proof.get_byte_size()

        start = datetime.now()
        r = Integer.get_random(mpz(3))
        query_at_one = ParallelSum.make_p_query(proof.get_size(), Integer(1))
        query_at_two = ParallelSum.make_p_query(proof.get_size(), Integer(2))
        query_at_r = ParallelSum.make_p_query(proof.get_size(), r)
        end = datetime.now()
        verifier_time += (end - start).total_seconds()

        start = datetime.now()
        p_r = proof * query_at_r
        is_accepted &= (proof * query_at_one + proof * query_at_two == calc_result)
        end = datetime.now()
        prover_time += (end - start).total_seconds()
        total_proof_length += proof.get_byte_size()

        total_query_length += 3

        for i in range(1, parallel_circuit.get_max_round() - 1):
            start = datetime.now()
            proof = parallel_circuit.make_next_proof(r)
            end = datetime.now()
            prover_time += (end - start).total_seconds()
            total_proof_length += proof.get_byte_size()

            start = datetime.now()
            r = Integer.get_random(mpz(3))
            query_at_one = ParallelSum.make_p_query(proof.get_size(), Integer(1))
            query_at_two = ParallelSum.make_p_query(proof.get_size(), Integer(2))
            query_at_r = ParallelSum.make_p_query(proof.get_size(), r)
            end = datetime.now()
            verifier_time += (end - start).total_seconds()

            start = datetime.now()
            is_accepted &= (proof * query_at_one + proof * query_at_two == p_r)
            p_r = proof * query_at_r
            end = datetime.now()
            prover_time += (end - start).total_seconds()

            total_query_length += 3

        start = datetime.now()
        proof = parallel_circuit.make_next_proof(r, True)
        end = datetime.now()
        prover_time += (end - start).total_seconds()
        total_proof_length += proof.get_byte_size()

        start = datetime.now()
        r = Integer.get_random(mpz(3))
        queries = parallel_circuit.make_last_queries(proof.get_size(), r)
        end = datetime.now()
        verifier_time += (end - start).total_seconds()
        total_query_length += len(queries)

        start = datetime.now()
        validation = []
        for i in range(len(queries) - 3):
            validation.append(proof * queries[i])
        end = datetime.now()
        prover_time += (end - start).total_seconds()

        start = datetime.now()
        g_gate = [InnerProductGGate(dim) for _ in range(len(validation) // parallel_circuit.get_g_gate_input_size())]
        g_r = Integer(0)
        for i in range(len(validation) // parallel_circuit.get_g_gate_input_size()):
            g_r += g_gate[i](validation[i * (g_gate[0].get_input_size()): (i + 1) * (g_gate[0].get_input_size())])
        end = datetime.now()
        verifier_time += (end - start).total_seconds()

        start = datetime.now()
        is_accepted &= (proof * queries[-3] == g_r)
        is_accepted &= (proof * queries[-1] + proof * queries[-2] == p_r)
        end = datetime.now()
        prover_time += (end - start).total_seconds()

        if verbose:
            print('-------------------------------------------')
            print(f'Circuit: perform inner product of two {dim}-dim vector (x {circuit_count})')
            print('Accepted!' if is_accepted else 'Rejected!')
            print('Verifier elapsed time(ms): ', verifier_time * 1000)
            print('Prover elapsed time(ms): ', prover_time * 1000)
            print('Proof length: ', total_proof_length)
            print('Query complexity: ', total_query_length)
            print('Soundness error: ', (math.log2(parallel_circuit.get_max_round()) * 2) / (Integer.get_base()))
            print('-------------------------------------------')

        assert is_accepted

        return is_accepted, verifier_time * 1000, prover_time * 1000, total_proof_length, total_query_length


if __name__ == '__main__':
    print('/-----------------------------------------------\\')
    print('|       Simple Fully Linear IOP Simulator       |')
    print('| Recursive linear IOP for parallel-sum circuit |')
    print('\\-----------------------------------------------/')
    print('')

    test_inner_product_parallel_sum(dim=3, circuit_count=1024)
