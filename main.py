import numpy as np
from networkx import watts_strogatz_graph

##  Parametry  ##
dist = np.random.normal(0.5, 0.25)  # mi - średnia, sigma - odchylenie standardowe, a więc oczekujemy wartości między 0.25 a 0.75
n_nodes = 20
n_edges = 15
rew_prob = 0.15  # prawdopodobieństwo zarażenia
per_infected = 0.4  # Liczba zarażonych na osobę
infection_duration = 7  # Czas trwania infekcji
per_vaccinated = 0.3  # Liczba osób zaszczepionych


def generate_social_network(n_nodes, n_edges, rew_prob, dist):
    graph = watts_strogatz_graph(n_nodes, n_edges, rew_prob)
    
    print(graph)


def initialize(n_nodes, n_edges, rew_prob, dist, per_infected):
    network = generate_social_network(n_nodes, n_edges, rew_prob, dist)


def run_simulation():
    network = initialize(n_nodes, n_edges, rew_prob, dist, per_infected)


run_simulation()