import heapq
from graph import graph

def remove_blocked_trail(graph, blocked_trail):

    new_graph = {
        node: edges.copy()
        for node, edges in graph.items()
    }

    if blocked_trail != "None":

        a, b = blocked_trail.split(" → ")

        new_graph[a] = [
            (node, weight)
            for node, weight in new_graph[a]
            if node != b
        ]

        new_graph[b] = [
            (node, weight)
            for node, weight in new_graph[b]
            if node != a
        ]

    return new_graph


def dijkstra(graph, start):

    distance = {node: float('inf') for node in graph}
    parent = {node: None for node in graph}

    distance[start] = 0

    priority_queue = [(0, start)]

    while priority_queue:

        current_distance, current_node = heapq.heappop(priority_queue)

        for neighbor, weight in graph[current_node]:

            new_distance = current_distance + weight

            if new_distance < distance[neighbor]:

                distance[neighbor] = new_distance
                parent[neighbor] = current_node

                heapq.heappush(
                    priority_queue,
                    (new_distance, neighbor)
                )

    return distance, parent


def get_path(parent, start, end):

    path = []
    current = end

    while current is not None:
        path.append(current)
        current = parent[current]

    path.reverse()

    return path


def patrol_planner(graph, start, required):

    current = start
    route = [start]
    total_distance = 0

    unvisited = set(required)

    while unvisited:

        distances, parent = dijkstra(graph, current)

        next_location = min(
            unvisited,
            key=lambda x: distances[x]
        )

        path = get_path(
            parent,
            current,
            next_location
        )

        route += path[1:]

        total_distance += distances[next_location]

        current = next_location

        unvisited.remove(next_location)

    return route, total_distance


if __name__ == "__main__":
    required = ["Water Point", "Zone A", "Watchtower"]

    route, distance = patrol_planner(
        graph,
        "Base",
        required
    )

    print("Actual Patrol Path:", " -> ".join(route))
    print("Total Distance:", distance, "km")