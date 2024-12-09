from collections import defaultdict, deque

def create_node():
    create_node.counter += 1
    return create_node.counter

create_node.counter = 0

def cards_game(m, n, k, counts):
    graph = defaultdict(list)
    capacity = {}

    def add_edge(u, v, cap):
        graph[u].append(v)
        graph[v].append(u)
        capacity[(u, v)] = cap
        capacity[(v, u)] = 0

    source, sink = create_node(), create_node()
    card_nodes = defaultdict(list)

    for player, card_list in counts.items():
        for value, color in card_list:
            card_node = create_node()
            card_nodes[(value, color)].append((player, card_node))
            if value == 1:
                add_edge(source, card_node, 1)
            if value == m:
                add_edge(card_node, sink, 1)

    for (value, color), nodes in card_nodes.items():
        for player, node in nodes:
            next_value = value + 1
            if next_value <= m:
                for next_color in range(1, k + 1):
                    for next_player, next_node in card_nodes.get((next_value, next_color), []):
                        if next_player == (player % n) + 1:
                            add_edge(node, next_node, 1)

    def bfs():
        parent = {source: None}
        queue = deque([source])
        while queue:
            u = queue.popleft()
            for v in graph[u]:
                if v not in parent and capacity[(u, v)] > 0:
                    parent[v] = u
                    if v == sink:
                        return parent
                    queue.append(v)
        return None

    def dfs(u, flow):
        if u == sink:
            return flow
        for v in graph[u]:
            if parent.get(v) == u and capacity[(u, v)] > 0:
                min_flow = min(flow, capacity[(u, v)])
                result = dfs(v, min_flow)
                if result > 0:
                    capacity[(u, v)] -= result
                    capacity[(v, u)] += result
                    return result
        return 0

    max_flow = 0
    while (parent := bfs()):
        while (flow := dfs(source, float('inf'))):
            max_flow += flow

    return max_flow
