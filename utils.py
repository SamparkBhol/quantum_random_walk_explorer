# utils.py
import time
import numpy as np
from qiskit import Aer, execute, QuantumCircuit
from qiskit.visualization import plot_bloch_multivector
import matplotlib.pyplot as plt
import networkx as nx

def validate_graph_type(graph_type, supported_graphs=['cycle', 'line', 'complete']):
    """
    Validate if the selected graph type is supported.
    :param graph_type: Graph type as string.
    :param supported_graphs: List of supported graph types.
    :return: Boolean, True if valid, False otherwise.
    """
    return graph_type in supported_graphs

def visualize_bloch_state(qc):
    """
    Visualize the Bloch state of the qubits in the quantum circuit.
    :param qc: QuantumCircuit object.
    """
    backend = Aer.get_backend('statevector_simulator')
    job = execute(qc, backend)
    result = job.result()
    statevector = result.get_statevector(qc)
    plot_bloch_multivector(statevector)
    plt.show()

def benchmark_quantum_walk(num_qubits=3, steps=5, graph_type='cycle'):
    """
    Benchmark the performance of a quantum random walk on a specified graph.
    :param num_qubits: Number of qubits (vertices).
    :param steps: Number of walk steps.
    :param graph_type: Type of graph ('cycle', 'line', 'complete').
    :return: Time taken for the quantum walk.
    """
    start_time = time.time()

    qr_walk = QuantumCircuit(num_qubits)
    for _ in range(steps):
        qr_walk.h(range(num_qubits))
        qr_walk.cx(0, 1)  # Example shift operator
        qr_walk.measure_all()

    backend = Aer.get_backend('qasm_simulator')
    execute(qr_walk, backend, shots=1024).result()

    end_time = time.time()
    return end_time - start_time

def visualize_graph(graph):
    """
    Visualize a NetworkX graph.
    :param graph: NetworkX graph object.
    """
    nx.draw(graph, with_labels=True, node_color='lightblue', node_size=1500, font_size=14)
    plt.show()

# Example Usage:
if __name__ == '__main__':
    # Validate graph type
    print(validate_graph_type('cycle'))

    # Benchmark a quantum walk
    duration = benchmark_quantum_walk()
    print(f"Quantum walk benchmark completed in {duration} seconds.")
