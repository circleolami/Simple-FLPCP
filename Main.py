from gmpy2 import mpz

from Custom.MyCircuit import MyCircuit
from Custom.MyGGate import MyGGate
from Unit.Integer import Integer

if __name__ == '__main__':
    Integer.set_prime(mpz(2) ** 127)

    dim = 20

    vec0 = [Integer(i) for i in range(dim * 2)]

    my_circuit = MyCircuit(dim)

    proof = my_circuit.make_proof(vec0)

    queries = my_circuit.make_query(len(vec0), proof.get_length(), Integer.get_random())

    validation = []
    for i in range(len(queries)):
        validation.append(proof * queries[i])

    g_gate = MyGGate(dim)
    sum = g_gate(validation[:dim * 2])

    print(sum == validation[-2] and validation[-1] == Integer(6270))

