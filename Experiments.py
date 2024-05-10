import os

import matplotlib.pyplot as plt

from TestInnerProdcutParallelSum import test_inner_product_parallel_sum
from TestInnerProductParallelSumWithoutIOP import test_inner_product_parallel_sum_without_iop


def plot_by_circuit_count(count: int):
    circuit_counts_iop = []
    prover_times_iop = []
    verifier_times_iop = []
    total_proof_sizes_iop = []
    query_count_iop = []

    for i in range(2, count, 2):
        circuit_counts_iop.append(2 ** i)
        _, v, p, t, q = test_inner_product_parallel_sum(dim=2, circuit_count=2 ** i, verbose=True)
        verifier_times_iop.append(v)
        prover_times_iop.append(p)
        total_proof_sizes_iop.append(t)
        query_count_iop.append(q)

    print(prover_times_iop)
    print(verifier_times_iop)
    print(total_proof_sizes_iop)
    print(query_count_iop)

    circuit_counts = []
    prover_times = []
    verifier_times = []
    total_proof_sizes = []
    query_count = []

    for i in range(2, count, 2):
        circuit_counts.append(2 ** i)
        _, v, p, t, q = test_inner_product_parallel_sum_without_iop(dim=2, circuit_count=2 ** i, verbose=True)
        verifier_times.append(v)
        prover_times.append(p)
        total_proof_sizes.append(t)
        query_count.append(q)

    print(prover_times)
    print(verifier_times)
    print(total_proof_sizes)
    print(query_count)

    fig, ax = plt.subplots()

    ax.plot(circuit_counts, prover_times, color='blue', marker='^', label='FLPCP')
    ax.plot(circuit_counts, prover_times_iop, color='red', marker='o', label='FLIOP')

    plt.xlabel('number of circuits')
    plt.ylabel('prover time(ms)')
    plt.xscale('log', base=2)
    plt.xticks(circuit_counts)
    plt.yscale('log', base=10)
    plt.legend(fontsize="large")

    fig.savefig(os.path.join('Figure', 'fig_prover_time_by_circuit_count.png'), dpi=300, format='png',
                facecolor='white',
                edgecolor='black',
                orientation='portrait', transparent=False,
                bbox_inches='tight', pad_inches=0.1, )

    plt.cla()

    ax.plot(circuit_counts, verifier_times, color='blue', marker='^', label='FLPCP')
    ax.plot(circuit_counts, verifier_times_iop, color='red', marker='o', label='FLIOP')

    plt.xlabel('number of circuits')
    plt.ylabel('verification time(ms)')
    plt.xscale('log', base=2)
    plt.xticks(circuit_counts)
    plt.yscale('log', base=10)
    plt.legend(fontsize="large")

    fig.savefig(os.path.join('Figure', 'fig_verification_time_by_circuit_count.png'), dpi=300, format='png', facecolor='white',
                edgecolor='black', orientation='portrait', transparent=False, bbox_inches='tight', pad_inches=0.1, )

    plt.cla()

    ax.plot(circuit_counts, total_proof_sizes, color='blue', marker='^', label='FLPCP')
    ax.plot(circuit_counts, total_proof_sizes_iop, color='red', marker='o', label='FLIOP')

    plt.xlabel('number of circuits')
    plt.ylabel('proof size(bytes)')
    plt.xscale('log', base=2)
    plt.xticks(circuit_counts)
    plt.yscale('log', base=10)
    plt.legend(fontsize="large")

    fig.savefig(os.path.join('Figure', 'fig_proof_size_by_circuit_count.png'), dpi=300, format='png', facecolor='white',
                edgecolor='black',
                orientation='portrait', transparent=False,
                bbox_inches='tight', pad_inches=0.1, )


def plot_by_dim(dim: int):
    circuit_counts_iop = []
    prover_times_iop = []
    verifier_times_iop = []
    total_proof_sizes_iop = []
    query_count_iop = []

    for i in range(2, dim):
        circuit_counts_iop.append(i)
        _, v, p, t, q = test_inner_product_parallel_sum(dim=i, circuit_count=16, verbose=True)
        verifier_times_iop.append(v)
        prover_times_iop.append(p)
        total_proof_sizes_iop.append(t)
        query_count_iop.append(q)

    print(prover_times_iop)
    print(verifier_times_iop)
    print(total_proof_sizes_iop)
    print(query_count_iop)

    circuit_counts = []
    prover_times = []
    verifier_times = []
    total_proof_sizes = []
    query_count = []

    for i in range(2, dim):
        circuit_counts.append(i)
        _, v, p, t, q = test_inner_product_parallel_sum_without_iop(dim=i, circuit_count=16, verbose=True)
        verifier_times.append(v)
        prover_times.append(p)
        total_proof_sizes.append(t)
        query_count.append(q)

    print(prover_times)
    print(verifier_times)
    print(total_proof_sizes)
    print(query_count)

    fig, ax = plt.subplots()

    ax.plot(circuit_counts, prover_times, color='blue', marker='^', label='FLPCP')
    ax.plot(circuit_counts, prover_times_iop, color='red', marker='o', label='FLIOP')

    plt.xlabel('input vector dimension')
    plt.ylabel('prover time(ms)')
    plt.xticks(circuit_counts)
    plt.legend(fontsize="large")

    fig.savefig(os.path.join('Figure', 'fig_prover_time_by_dim.png'), dpi=300, format='png',
                facecolor='white',
                edgecolor='black',
                orientation='portrait', transparent=False,
                bbox_inches='tight', pad_inches=0.1, )

    plt.cla()

    ax.plot(circuit_counts, verifier_times, color='blue', marker='^', label='FLPCP')
    ax.plot(circuit_counts, verifier_times_iop, color='red', marker='o', label='FLIOP')

    plt.xlabel('input vector dimension')
    plt.ylabel('verification time(ms)')
    plt.xticks(circuit_counts)
    plt.legend(fontsize="large")

    fig.savefig(os.path.join('Figure', 'fig_verification_time_by_dim.png'), dpi=300, format='png', facecolor='white',
                edgecolor='black',
                orientation='portrait', transparent=False,
                bbox_inches='tight', pad_inches=0.1, )

    plt.cla()

    ax.plot(circuit_counts, total_proof_sizes, color='blue', marker='^', label='FLPCP')
    ax.plot(circuit_counts, total_proof_sizes_iop, color='red', marker='o', label='FLIOP')

    plt.xlabel('input vector dimension')
    plt.ylabel('proof size(bytes)')
    plt.xticks(circuit_counts)
    plt.legend(fontsize="large")

    fig.savefig(os.path.join('Figure', 'fig_proof_size_by_dim.png'), dpi=300, format='png', facecolor='white',
                edgecolor='black',
                orientation='portrait', transparent=False,
                bbox_inches='tight', pad_inches=0.1)


if __name__ == '__main__':
    if not os.path.exists('Figure'):
        os.makedirs('Figure')

    plot_by_circuit_count(count=11)
    plot_by_dim(dim=12)
