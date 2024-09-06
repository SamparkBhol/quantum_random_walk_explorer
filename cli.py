# cli.py
import argparse
from quantum_walk import QuantumRandomWalk
from ai_assistant import GraphSuggestionAI

class QuantumWalkCLI:
    def __init__(self):
        """
        Initializes the command-line interface for the Quantum Random Walk Explorer.
        """
        self.ai_assistant = GraphSuggestionAI()

    def run(self):
        """
        Run the CLI, parsing arguments and executing the quantum random walk.
        """
        parser = argparse.ArgumentParser(
            description="Quantum Random Walk Explorer: Explore quantum walks on predefined graph configurations."
        )
        parser.add_argument('--qubits', type=int, default=3, help="Number of qubits (vertices in the graph).")
        parser.add_argument('--steps', type=int, default=5, help="Number of steps in the quantum random walk.")
        parser.add_argument('--graph', type=str, default=None, choices=['cycle', 'line', 'complete'],
                            help="Type of graph for the walk (cycle, line, complete).")

        parser.add_argument('--suggest', action='store_true',
                            help="Use AI to suggest a graph type for the quantum walk.")
        parser.add_argument('--insight', action='store_true',
                            help="Get an AI-generated insight into quantum walks and their applications.")

        args = parser.parse_args()

        # If --suggest is passed, use the AI assistant to suggest a graph
        if args.suggest:
            graph_type, explanation = self.ai_assistant.suggest_graph()
            print(f"AI Suggestion: Graph Type - {graph_type}")
            print(f"Explanation: {explanation}")
            args.graph = graph_type
        elif args.graph is None:
            print("Error: You must specify a graph type or use the --suggest option.")
            return

        # Display an AI insight if requested
        if args.insight:
            insight = self.ai_assistant.provide_application_insight()
            print(f"AI Insight: {insight}")

        # Run the quantum random walk with specified or suggested parameters
        qr_walk = QuantumRandomWalk(num_qubits=args.qubits, steps=args.steps, graph_type=args.graph)

        # Visualize the graph
        print(f"Visualizing the {args.graph} graph with {args.qubits} qubits.")
        qr_walk.visualize_graph()

        # Run the quantum walk and visualize results
        print(f"Running the quantum walk for {args.steps} steps...")
        results = qr_walk.run_walk()
        qr_walk.visualize_walk_results(results)


if __name__ == '__main__':
    # Run the CLI
    cli = QuantumWalkCLI()
    cli.run()
