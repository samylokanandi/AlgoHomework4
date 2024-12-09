# Problem 1a,b,c 
# NOTE: Problem B and C are to be implemented in this file as well

import networkx as nx
import matplotlib.pyplot as plt


def add_edges_for_source_and_sink(G, num_data_hubs, num_service_providers, provider_capacities):
    source = "Source"
    sink = "Sink"
    for hub in range(num_data_hubs):
        G.add_edge(source, hub, capacity=1)
    for i, capacity in enumerate(provider_capacities[num_data_hubs:], start=num_data_hubs):
        if capacity > 0:
            G.add_edge(i, sink, capacity=capacity)


def assign_node_positions(num_data_hubs, num_service_providers):
    pos = {}
    total_height = max(num_data_hubs, num_service_providers)
    y_start = -(total_height - 1) / 2
    pos["Source"] = (-2, 0)
    for i in range(num_data_hubs):
        pos[i] = (0, y_start + i)
    for i in range(num_data_hubs, num_data_hubs + num_service_providers):
        pos[i] = (2, y_start + (i - num_data_hubs))
    pos["Sink"] = (4, 0)
    return pos


def visualize_graph(G, pos, output_file, title):
    edge_labels = nx.get_edge_attributes(G, "capacity")
    filtered_edges = [(u, v) for u, v, data in G.edges(data=True) if data["capacity"] > 0]
    plt.figure(figsize=(12, 6))
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_size=700,
        node_color="skyblue",
        font_size=10,
        font_weight="bold",
        arrowsize=20,
        edgelist=filtered_edges,
    )
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color="red")
    plt.title(title)
    plt.savefig(output_file)
    plt.close()


def plan_city_a(num_data_hubs, num_service_providers, connections, provider_capacities, preliminary_assignment, output_file="graph_no_sink_connections.png"):
    G = nx.DiGraph()
    source = "Source"
    sink = "Sink"
    G.add_node(source)
    G.add_node(sink)
    for hub in range(num_data_hubs):
        G.add_edge(source, hub, capacity=1)
    for hub, providers in connections.items():
        for provider in providers:
            G.add_edge(hub, provider, capacity=1)
    pos = assign_node_positions(num_data_hubs, num_service_providers)
    visualize_graph(G, pos, output_file, "Problem 1.a: Connectivity Graph")


def plan_city_b(num_data_hubs, num_service_providers, connections, provider_capacities, preliminary_assignment, output_file="graph_with_sink_connections.png"):
    G = nx.DiGraph()
    for hub, providers in connections.items():
        for provider in providers:
            G.add_edge(hub, provider, capacity=1)
    add_edges_for_source_and_sink(G, num_data_hubs, num_service_providers, provider_capacities)
    pos = assign_node_positions(num_data_hubs, num_service_providers)
    visualize_graph(G, pos, output_file, "Problem 1.b: Connectivity Graph")


def plan_city_c_residual(num_data_hubs, num_service_providers, connections, provider_capacities, preliminary_assignment, output_file="residual_graph.png"):
    G = nx.DiGraph()
    for hub, providers in connections.items():
        for provider in providers:
            G.add_edge(hub, provider, capacity=1)
    add_edges_for_source_and_sink(G, num_data_hubs, num_service_providers, provider_capacities)
    residual_graph = nx.DiGraph()
    for u, v, data in G.edges(data=True):
        residual_graph.add_edge(u, v, capacity=data["capacity"])
        residual_graph.add_edge(v, u, capacity=0)
    for hub, provider in preliminary_assignment.items():
        if residual_graph.has_edge(hub, provider):
            residual_graph[hub][provider]["capacity"] -= 1
            residual_graph[provider][hub]["capacity"] += 1
        if residual_graph.has_edge("Source", hub):
            residual_graph["Source"][hub]["capacity"] -= 1
            residual_graph[hub]["Source"]["capacity"] += 1
        if residual_graph.has_edge(provider, "Sink"):
            residual_graph[provider]["Sink"]["capacity"] -= 1
            residual_graph["Sink"][provider]["capacity"] += 1
    pos = assign_node_positions(num_data_hubs, num_service_providers)
    visualize_graph(residual_graph, pos, output_file, "Problem 1.c: Residual Graph")


plan_city_a(
    num_data_hubs=5,
    num_service_providers=5,
    connections={
        0: [5, 7, 8],
        1: [5, 8],
        2: [7, 8, 9],
        3: [5, 6, 8, 9],
        4: [5, 6, 7, 8]
    },
    provider_capacities=[0] * 5 + [0, 1, 0, 2, 2],
    preliminary_assignment={0: 8, 1: 8, 2: 9, 3: 9},
    output_file="problem_1a_graph.png"
)

plan_city_b(
   num_data_hubs=5,
    num_service_providers=5,
    connections={
        0: [5, 7, 8],
        1: [5, 8],
        2: [7, 8, 9],
        3: [5, 6, 8, 9],
        4: [5, 6, 7, 8]
    },
    provider_capacities=[0] * 5 + [0, 1, 0, 2, 2],
    preliminary_assignment={0: 8, 1: 8, 2: 9, 3: 9},
    output_file="problem_1b_graph.png"
)

plan_city_c_residual(
    num_data_hubs=5,
    num_service_providers=5,
    connections={
        0: [5, 7, 8],
        1: [5, 8],
        2: [7, 8, 9],
        3: [5, 6, 8, 9],
        4: [5, 6, 7, 8]
    },
    provider_capacities=[0] * 5 + [0, 1, 0, 2, 2],
    preliminary_assignment={0: 8, 1: 8, 2: 9, 3: 9},
    output_file="problem_1c_graph.png"
)
