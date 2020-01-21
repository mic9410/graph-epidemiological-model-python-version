import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

n_nodes = 20
n_edges = 15
rew_prob = 0.15  # prawdopodobieństwo zarażenia
per_infected = 0.4  # Liczba zarażonych na osobę
infection_duration = 7  # Czas trwania infekcji
per_vaccinated = 0.3  # Liczba osób zaszczepionych


def generate_social_network(n_nodes, n_edges, rew_prob):
    graph = nx.watts_strogatz_graph(n_nodes, n_edges, rew_prob)
    for i in range(0, n_nodes):
        graph.nodes[i].update({"exposed_to_infection": np.random.normal(0.5, 0.25)})
        graph.nodes[i].update({"infected": False})
        graph.nodes[i].update({"inf_days": 0})
        graph.nodes[i].update({"color": 0})

    plot_graph_to_file(graph, "init")

    return graph


def plot_graph_to_file(graph, filename="graph"):
    nx.draw(graph)
    plt.tight_layout()
    plt.show()
    plt.savefig(filename + ".png", format="PNG")


def initialize(n_nodes, n_edges, rew_prob, per_infected):
    network = generate_social_network(n_nodes, n_edges, rew_prob)


def run_simulation():
    network = initialize(n_nodes, n_edges, rew_prob, per_infected)


run_simulation()
