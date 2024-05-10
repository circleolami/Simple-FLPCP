from datetime import datetime

from gmpy2 import mpz

from Base.ParallelSumRootM import ParallelSumRootM
from Custom.InnerProductGGate import InnerProductGGate
from Unit.Integer import Integer


def test_inner_product_parallel_sum_without_iop(dim: int, circuit_count: int, verbose: bool = True):
    Integer.set_prime(mpz(2) ** 127)

    input_vec = [Integer(i) for i in range(dim * 2 * circuit_count)]

    my_circuit = ParallelSumRootM([InnerProductGGate(dim=dim) for _ in range(circuit_count)])

    prover_time = 0
    verifier_time = 0

    start = datetime.now()
    calc_result = my_circuit(input_vec)
    proof = my_circuit.make_proof(input_vec)
    end = datetime.now()
    prover_time += (end - start).total_seconds()

    start = datetime.now()
    r = Integer.get_random(mpz(my_circuit.get_g_gates_count() + 1))
    queries = my_circuit.make_queries(proof.get_size(), r)
    end = datetime.now()
    verifier_time += (end - start).total_seconds()

    start = datetime.now()
    validation = []
    for i in range(len(queries) - 2):
        validation.append(proof * queries[i])
    end = datetime.now()
    prover_time += (end - start).total_seconds()

    start = datetime.now()
    g_gate = [InnerProductGGate(dim) for _ in range(my_circuit.get_g_gates_count())]
    g_r = Integer(0)
    for i in range(my_circuit.get_g_gates_count()):
        g_r += g_gate[i](validation[g_gate[0].get_input_size() * i:g_gate[0].get_input_size() * (i + 1)])
    end = datetime.now()
    verifier_time += (end - start).total_seconds()

    start = datetime.now()
    is_accepted = proof * queries[-2] == g_r and proof * queries[-1] == calc_result
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
        print('Soundness error: ', (proof.get_size() - 1 - len(input_vec) - my_circuit.get_g_gates_count()) / (
                    Integer.get_base() - my_circuit.get_g_gates_count()))
        print('-------------------------------------------')

    assert is_accepted

    return is_accepted, verifier_time * 1000, prover_time * 1000, proof.get_byte_size(), len(queries)


if __name__ == '__main__':
    print('/-----------------------------------------\\')
    print('|    Simple Fully Linear PCP Simulator    |')
    print('|  Short proof for parallel-sum circuits  |')
    print('\\-----------------------------------------/')
    print('')

    test_inner_product_parallel_sum_without_iop(dim=3, circuit_count=64)
