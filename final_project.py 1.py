# final_project.py

import heapq

# Algorithm 1: Lowest Cost Delivery Between Two Locations (Dijkstra's Algorithm)
def algorithm_1(graph, start, end):
    # Priority queue to keep track of nodes to explore, format: (cost, path, current_node)
    queue = [(0, [start], start)]
    visited = set()

    while queue:
        cost, path, node = heapq.heappop(queue)
        
        if node == end:
            return path, cost

        if node not in visited:
            visited.add(node)
            for neighbor, weight in graph.get(node, []):
                if neighbor not in visited:
                    heapq.heappush(queue, (cost + weight, path + [neighbor], neighbor))
    
    return None, float('inf')  # If no path found

# Algorithm 2: Best Path from the Hub (Prim's Algorithm for MST)
def algorithm_2(graph, hub):
    visited = set([hub])
    edges = []
    min_edges = [(weight, hub, neighbor) for neighbor, weight in graph.get(hub, [])]
    heapq.heapify(min_edges)
    mst = []
    total_cost = 0

    while min_edges:
        weight, node1, node2 = heapq.heappop(min_edges)
        if node2 not in visited:
            visited.add(node2)
            mst.append((node1, node2, weight))
            total_cost += weight
            for neighbor, neighbor_weight in graph.get(node2, []):
                if neighbor not in visited:
                    heapq.heappush(min_edges, (neighbor_weight, node2, neighbor))

    return mst, total_cost

# Algorithm 3: Dynamic Network Changes (Update and re-run MST)
def algorithm_3(graph, hub, remove_edges, add_edges):
    # Convert remove_edges from "A-B" to a set of tuples
    remove_edges_set = set()
    for edge in remove_edges:
        node1, node2 = edge.split("-")
        remove_edges_set.add((node1, node2))
        remove_edges_set.add((node2, node1))

    # Remove specified edges
    for node in graph:
        graph[node] = [ (neighbor, weight) for neighbor, weight in graph[node] if (node, neighbor) not in remove_edges_set ]

    # Add new edges
    for node1, node2, weight in add_edges:
        graph.setdefault(node1, []).append((node2, weight))
        graph.setdefault(node2, []).append((node1, weight))

    # Now run Prim's algorithm
    return algorithm_2(graph, hub)

# Example usage and testing
if __name__ == "__main__":
    example_graph = {
        "A": [("B", 4), ("C", 2)],
        "B": [("A", 4), ("C", 1), ("D", 5)],
        "C": [("A", 2), ("B", 1), ("D", 8), ("E", 10)],
        "D": [("B", 5), ("C", 8), ("E", 2)],
        "E": [("C", 10), ("D", 2)]
    }

    print("Algorithm 1 Test:")
    path, cost = algorithm_1(example_graph, "A", "E")
    print(f"Shortest Path: {' -> '.join(path)}, Cost: {cost}")

    print("\nAlgorithm 2 Test:")
    mst, total_cost = algorithm_2(example_graph, "A")
    print(f"MST: {mst}, Total Cost: {total_cost}")

    print("\nAlgorithm 3 Test:")
    new_mst, new_total_cost = algorithm_3(
        {
            "A": [("B", 4), ("C", 2)],
            "B": [("A", 4), ("C", 1), ("D", 5)],
            "C": [("A", 2), ("B", 1), ("D", 8), ("E", 10)],
            "D": [("B", 5), ("C", 8), ("E", 2)],
            "E": [("C", 10), ("D", 2)]
        },
        "A",
        ["C-E"], 
        [("B", "E", 3)]
    )
    print(f"Updated MST: {new_mst}, Updated Total Cost: {new_total_cost}")
