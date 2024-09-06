# quantum_walk.py
import qiskit
from qiskit import QuantumCircuit, Aer, execute
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

class QuantumRandomWalk:
    def __init__(self, num_qubits=3, steps=5, graph_type='cycle'):
        """
        Initialize Quantum Random Walk with specified number of qubits, steps, and graph type.
        :param num_qubits: Number of qubits (vertices in the graph).
        :param steps: Number of steps in the quantum walk.
        :param graph_type: Type of graph ('cycle', 'line', 'complete').
        """
        self.num_qubits = num_qubits
        self.steps = steps
        self.graph = self.create_graph(graph_type)
        self.backend = Aer.get_backend('qasm_simulator')
        self.qc = QuantumCircuit(self.num_qubits)

    def create_graph(self, graph_type):
        """
        Create a predefined graph based on the type.
        :param graph_type: Type of graph ('cycle', 'line', 'complete').
        :return: NetworkX graph.
        """
        if graph_type == 'cycle':
            return nx.cycle_graph(self.num_qubits)
        elif graph_type == 'line':
            return nx.path_graph(self.num_qubits)
        elif graph_type == 'complete':
            return nx.complete_graph(self.num_qubits)
        else:
            raise ValueError("Unsupported graph type. Choose 'cycle', 'line', or 'complete'.")

    def apply_hadamard(self):
        """Apply Hadamard gate to all qubits to initialize them in superposition."""
        for qubit in range(self.num_qubits):
            self.qc.h(qubit)

    def apply_coin_operator(self):
        """Apply the coin operator, which is a random walk step in the Hilbert space."""
        for qubit in range(self.num_qubits):
            self.qc.h(qubit)  # Hadamard operator as the coin flip
            self.qc.p(np.pi/4, qubit)  # Phase shift

    def apply_shift_operator(self):
        """Apply the shift operator based on the graph's adjacency matrix."""
        adj_matrix = nx.adjacency_matrix(self.graph).todense()
        for i in range(self.num_qubits):
            for j in range(self.num_qubits):
                if adj_matrix[i, j] == 1:
                    self.qc.cx(i, j)  # Controlled NOT between adjacent vertices

    def run_walk(self):
        """Run the quantum random walk for the specified number of steps."""
        self.apply_hadamard()  # Initialize qubits in superposition
        for _ in range(self.steps):
            self.apply_coin_operator()
            self.apply_shift_operator()

        self.qc.measure_all()

        job = execute(self.qc, backend=self.backend, shots=1024)
        result = job.result()
        counts = result.get_counts()

        return counts

    def visualize_graph(self):
        """Visualize the graph using NetworkX."""
        nx.draw(self.graph, with_labels=True, node_color='skyblue', node_size=1500, font_size=14)
        plt.title(f"Graph Type: {self.graph}")
        plt.show()

    def visualize_walk_results(self, counts):
        """Visualize the results of the quantum walk."""
        plt.bar(counts.keys(), counts.values(), color='purple')
        plt.xlabel('Qubit States')
        plt.ylabel('Counts')
        plt.title('Quantum Walk Results')
        plt.xticks(rotation=90)
        plt.show()


# Example of usage:
if __name__ == '__main__':
    # Initialize a quantum random walk on a cycle graph with 3 qubits and 5 steps
    qr_walk = QuantumRandomWalk(num_qubits=3, steps=5, graph_type='cycle')
    
    # Visualize the graph
    qr_walk.visualize_graph()
    
    # Run the quantum random walk
    results = qr_walk.run_walk()
    
    # Visualize the results
    qr_walk.visualize_walk_results(results)
