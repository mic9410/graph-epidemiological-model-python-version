from collections import Counter

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

n_nodes = 20
n_edges = 15
rew_prob = 0.34  # prawdopodobieństwo zarażenia
per_infected = 0.6  # Liczba zarażonych na osobę
infection_duration = 7  # Czas trwania infekcji
per_vaccinated = 0.2  # Liczba osób zaszczepionych
max_iter = 5000

class Infection:
    def __init__(self, graph):
        self.graph = graph
        self.sir = []

    def infect(self, person_id):
        self.graph.nodes[person_id].update({"infected": True})
        self.graph.nodes[person_id].update({"color": 1})
        self.graph.nodes[person_id].update({"inf_days": 1})

    def vaccinate(self, person_id):
        self.graph.nodes[person_id].update({"infected": False})
        self.graph.nodes[person_id].update({"color": 2})

    def continue_infection(self, person_id):
        curr = self.graph.nodes[person_id].get("inf_days")
        self.graph.nodes[person_id].update({"inf_days": curr + 1})

    def heal(self, person_id):
        self.graph.nodes[person_id].update({"infected": False})
        self.graph.nodes[person_id].update({"color": 2})
        self.graph.nodes[person_id].update({"inf_days": 0})

    def environmental_conditions_prop(self):
        num_of_sick = 0.0
        for i in self.graph.nodes:
            if self.graph.nodes[i].get("infected"):
                num_of_sick += 1.0
        return -(1.0 - num_of_sick/len(self.graph.nodes))

    def get_occurence(self):
        total = {"0": 0, "1": 0, "2": 0}
        for i in range(0, len(self.graph.nodes)):
            col_nr = str(self.graph.nodes.get(i).get("color"))
            total.update({col_nr: total.get(col_nr) + 1})
        return total


    def update_sir(self):
        occurence = self.get_occurence()
        susceptible = occurence["0"]
        infectious = occurence["1"]
        recovered = occurence["2"]
        self.sir.append([susceptible, infectious, recovered])

    def plot_graph(self, filename="graph"):
        color_map = []
        for i in self.graph.nodes:
            if self.graph.nodes.get(i).get("color") == 0:
                color_map.append('limegreen')
            elif self.graph.nodes.get(i).get("color") == 1:
                color_map.append('darkred')
            else:
                color_map.append('steelblue')

        nx.draw(self.graph, node_color=color_map, with_labels=True)
        plt.tight_layout()
        plt.show(block=False)
        plt.savefig(filename + ".png", format="PNG")
        plt.clf()

    ## TODO - create plot from that - in the colomsn we have [S, I , R] values
    def plot_sir(self):
        sir_t = list(map(list, zip(self.sir)))
        plt.plot(sir_t, [0.00, 1.00])
        plt.show(block=False)
        plt.savefig("sir.png", format="PNG")
        plt.clf()


def generate_social_network(n_nodes, n_edges, rew_prob):
    graph = nx.watts_strogatz_graph(n_nodes, n_edges, rew_prob)
    for i in range(0, n_nodes):
        graph.nodes[i].update({"exposed_to_infection": np.random.normal(0.5, 0.25)})
        graph.nodes[i].update({"infected": False})
        graph.nodes[i].update({"inf_days": 0})
        graph.nodes[i].update({"color": 0})
    return graph


def initialize(n_nodes, n_edges, rew_prob, per_infected):
    graph = generate_social_network(n_nodes, n_edges, rew_prob)
    infection = Infection(graph)
    for i in range(0, n_nodes):
        if graph.nodes.get(i).get("exposed_to_infection") >= 1.0:   # Czy ktoś już jest chory?
            infection.infect(i)  # Tak - zaznaczamy

    # Losowy wybór osób chorych od początku, na każdą osobę przypada per_infected zarażonej
    infected = np.random.choice(graph.nodes, int(len(graph.nodes)*per_infected), replace=False)
    for i in infected:
        infection.infect(i)

    # osoba nie może być jednocześnie chora i odporna, dlatego należy odrzucić osoby chore
    # numery wierzchołków - kandydatów do szczepienia zapisujemy w tabeli immune_candidates
    immune_candidates = []
    for i in graph.nodes:
        if graph.nodes.get(i).get("infected") == 0:
            immune_candidates.append(i)

    # Losowy wybór osób odpornych od początku (zaszczepionych), na każdą osobę przypada per_vaccinated zarażonej
    vaccined = np.random.choice(immune_candidates, int(len(immune_candidates) * per_vaccinated), replace=False)
    for i in vaccined:
        infection.vaccinate(i)
    return infection


def is_active(infection):
    final = 0  # Czy symulacja powinna jeszcze trwać
    for i in infection.graph.nodes:
        if not infection.graph.nodes.get(i).get("infected"):
            env_conditions = infection.environmental_conditions_prop()
            if infection.graph.nodes.get(i).get("exposed_to_infection") + env_conditions > 0 \
                    and not infection.graph.nodes.get(i).get("color") == 2:
                infection.infect(i)
                final = 1
        if infection.graph.nodes.get(i).get("infected") \
                and infection.graph.nodes.get(i).get("inf_days") < infection_duration:
            infection.continue_infection(i)
            final = 1
        if infection.graph.nodes.get(i).get("infected") \
                and infection.graph.nodes.get(i).get("inf_days") >= infection_duration:
            infection.heal(i)
            final = 1
    return final


def run_simulation():
    infection_network = initialize(n_nodes, n_edges, rew_prob, per_infected)
    infection_network.plot_graph("start")
    for i in range(1, max_iter):
        infection_network.update_sir()
        done = is_active(infection_network)
        if done == 0:
            break

    infection_network.plot_graph("end")
    infection_network.plot_sir()

run_simulation()
