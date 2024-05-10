from gmpy2 import mpz

from Custom.InnerProductCircuit import InnerProductCircuit
from Custom.InnerProductGGate import InnerProductGGate
from Unit.Integer import Integer

if __name__ == '__main__':
    print('/-------------------------------------------\\')
    print('|     Simple Fully Linear PCP Simulator     |')
    print('| One-round FLPCP for inner product circuit |')
    print('\\-------------------------------------------/')
    print('')

    # Input vector dimension
    dim = 30
    print(f'Circuit: perform inner product of two {dim}-dim vector')

    # Choose base probable prime number greater than 2 ** 127
    Integer.set_prime(mpz(2) ** 127)
    print('Base (probable) prime number: ', Integer.get_base())

    # Concat two operand vector
    input_vec = [Integer(i) for i in range(dim * 2)]
    print('Input vector 1: ', input_vec[:dim])
    print('Input vector 2: ', input_vec[dim:])

    print('-------------------------------------------')

    # Define circuit
    my_circuit = InnerProductCircuit(dim)

    # Perform calculation normally
    calc_result = my_circuit(input_vec)

    # Make proof vector (P)
    proof = my_circuit.make_proof(input_vec)

    # Choose random greater than the number of G-gate (V)
    r = Integer.get_random(mpz(my_circuit.get_g_gate_count() + 1))
    print('r (chosen by verifier): ', r)

    # Make queries only using public circuit (V)
    queries = my_circuit.make_queries(len(input_vec), proof.get_size(), r)

    # Perform dot product between proof and queries (P -> V)
    validation = []
    for i in range(len(queries) - 2):
        validation.append(proof * queries[i])

    # Verification (V)
    g_gate = InnerProductGGate(dim)
    g_r = g_gate(validation)

    print('-------------------------------------------')
    print('G(f_1(r), f_2(r), ..., f_L(r)): ', g_r)
    print('p(r): ', proof * queries[-2])
    print('p(M): ', proof * queries[-1])
    print('Calculation result: ', calc_result)
    print('-------------------------------------------')
    print('p(r) == G(f_1(r), f_2(r), ..., f_L(r)): ', proof * queries[-2] == g_r)
    print('p(M) == Calculation result: ', proof * queries[-1] == calc_result)
    print('-------------------------------------------')
    print('Accepted!' if proof * queries[-2] == g_r and proof * queries[-1] == calc_result else 'Rejected!')
    print('-------------------------------------------')
    print('Proof length: ', proof.get_size())
    print('Query complexity: ', len(queries))
    print('Soundness error: ', (proof.get_size() - 1 - len(input_vec) - my_circuit.get_g_gate_count()) / (Integer.get_base() - my_circuit.get_g_gate_count()))
