import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

n_nodes = 20
n_edges = 15
rew_prob = 0.15  # prawdopodobieństwo zarażenia
per_infected = 0.2  # Liczba zarażonych na osobę
infection_duration = 7  # Czas trwania infekcji
per_vaccinated = 0.3  # Liczba osób zaszczepionych


class Infection:
    def __init__(self, graph):
        self.graph = graph

    def infect(self, person_id):
        self.graph.nodes[person_id].update({"infected": True})
        self.graph.nodes[person_id].update({"color": 1})

    def plot_graph_to_file(graph, filename="graph"):
        nx.draw(graph)
        plt.tight_layout()
        plt.show()
        plt.savefig(filename + ".png", format="PNG")


def generate_social_network(n_nodes, n_edges, rew_prob):
    graph = nx.watts_strogatz_graph(n_nodes, n_edges, rew_prob)
    for i in range(0, n_nodes):
        graph.nodes[i].update({"exposed_to_infection": np.random.normal(0.5, 0.25)})
        graph.nodes[i].update({"infected": False})
        graph.nodes[i].update({"inf_days": 0})
        graph.nodes[i].update({"color": 0})

    # plot_graph_to_file(graph, "init")
    return graph


def initialize(n_nodes, n_edges, rew_prob, per_infected):
    graph = generate_social_network(n_nodes, n_edges, rew_prob)
    infection = Infection(graph)
    for i in range(0, n_nodes):
        if graph.nodes.get(i).get("exposed_to_infection") >= 1.0:
            infection.infect(i)

    infected = np.random.choice(graph.nodes, int(len(graph.nodes)*per_infected), replace=False)
    for i in infected:
        infection.infect(i)


def run_simulation():
    network = initialize(n_nodes, n_edges, rew_prob, per_infected)


run_simulation()
