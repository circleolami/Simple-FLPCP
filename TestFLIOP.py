from datetime import datetime
from gmpy2 import mpz
from Base.ParallelSumRootM import ParallelSumRootM
from Custom.InnerProductGGate import InnerProductGGate
from Unit.Integer import Integer

# Function to compute optimal degrees
def compute_degrees(n: int):
    dp = [0] * (n + 1)
    degrees = [0] * n

    # Dynamic Programming to calculate optimal degrees
    for i in range(1, n + 1):
        dp[i] = float('inf')
        for j in range(1, i + 1):
            cost = dp[i // j] + j
            if cost < dp[i]:
                dp[i] = cost
                degrees[i - 1] = j

    return degrees

# Function to test FLIOP
def test_fliop(dim: int, circuit_count: int, verbose: bool = True):
    # Set the base prime number
    Integer.set_prime(mpz(2) ** 127)

    # Generate input vector
    input_vec = [Integer(i) for i in range(dim * 2 * circuit_count)]

    # Compute optimal degrees
    degrees = compute_degrees(dim)

    # Create instances of InnerProductGGate using the optimal degrees
    my_circuit = ParallelSumRootM([InnerProductGGate(dim=dim, degrees=degrees) for _ in range(circuit_count)])

    prover_time = 0
    verifier_time = 0

    # Measure the time taken by the prover to compute the circuit and generate the proof
    start = datetime.now()
    calc_result = my_circuit(input_vec)
    proof = my_circuit.make_proof(input_vec)
    end = datetime.now()
    prover_time += (end - start).total_seconds()

    # Measure the time taken by the verifier to generate queries
    start = datetime.now()
    r = Integer.get_random(mpz(my_circuit.get_g_gates_count() + 1))
    queries = my_circuit.make_queries(proof.get_size(), r)
    end = datetime.now()
    verifier_time += (end - start).total_seconds()

    # Measure the time taken to compute the inner product of proof vector and query vector
    start = datetime.now()
    validation = []
    for i in range(len(queries) - 2):
        validation.append(proof * queries[i])
    end = datetime.now()
    prover_time += (end - start).total_seconds()

    # Measure the time taken by the verifier to perform the final verification
    start = datetime.now()
    g_gate = [InnerProductGGate(dim=dim, degrees=degrees) for _ in range(my_circuit.get_g_gates_count())]
    g_r = Integer(0)
    for i in range(my_circuit.get_g_gates_count()):
        g_r += g_gate[i](validation[g_gate[0].get_input_size() * i:g_gate[0].get_input_size() * (i + 1)])
    end = datetime.now()
    verifier_time += (end - start).total_seconds()

    # Verify the proof vector against the computation result
    start = datetime.now()
    is_accepted = proof * queries[-2] == g_r and proof * queries[-1] == calc_result
    end = datetime.now()
    prover_time += (end - start).total_seconds()

    # Print the results
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

    # Assert that the verification result is correct
    assert is_accepted

    return is_accepted, verifier_time * 1000, prover_time * 1000, proof.get_byte_size(), len(queries)

if __name__ == '__main__':
    print('/-----------------------------------------\\')
    print('|    Simple Fully Linear PCP Simulator    |')
    print('|  Short proof for parallel-sum circuits  |')
    print('\\-----------------------------------------/')
    print('')

    # Perform test with example parameters
    test_fliop(dim=3, circuit_count=64)
