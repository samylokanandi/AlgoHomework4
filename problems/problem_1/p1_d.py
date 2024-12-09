def plan_city_d(num_data_hubs, num_service_providers, connections, provider_capacities, preliminary_assignment):
    n = num_data_hubs + num_service_providers + 2
    residual_capacity = [[0] * n for _ in range(n)]
    source, sink = 0, n - 1

    for hub in range(num_data_hubs):
        residual_capacity[source][hub + 1] = 1

    for hub, providers in connections.items():
        for provider in providers:
            residual_capacity[hub + 1][provider + 1] = 1

    for provider in range(num_service_providers):
        provider_index = provider + num_data_hubs + 1
        residual_capacity[provider_index][sink] = provider_capacities[num_data_hubs + provider]

    for hub, provider in preliminary_assignment.items():
        hub_index, provider_index = hub + 1, provider + 1
        if residual_capacity[hub_index][provider_index] > 0:
            residual_capacity[hub_index][provider_index] -= 1
            residual_capacity[provider_index][hub_index] += 1
            residual_capacity[source][hub_index] -= 1
            residual_capacity[provider_index][sink] -= 1

    def bfs(source, sink):
        parent = [-1] * n
        visited = [False] * n
        queue = [source]
        visited[source] = True

        while queue:
            current = queue.pop(0)
            for neighbor in range(n):
                if not visited[neighbor] and residual_capacity[current][neighbor] > 0:
                    parent[neighbor] = current
                    visited[neighbor] = True
                    queue.append(neighbor)
                    if neighbor == sink:
                        return True
        return False

    last_hub = num_data_hubs - 1
    return bfs(last_hub + 1, sink)
