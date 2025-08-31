import heapq
import sys
import matplotlib
import matplotlib.pyplot as plt
import networkx as nx

# ✅ Force a proper plotting backend (works in Spyder)
matplotlib.use("Qt5Agg")   # or "TkAgg" if Qt not available

# Function to construct adjacency 
def constructAdj(edges, V):
    adj = [[] for _ in range(V)]
    for edge in edges:
        u, v, wt = edge
        adj[u].append([v, wt])
        adj[v].append([u, wt])
    return adj

# Dijkstra's Algorithm
def dijkstra(V, edges, src):
    adj = constructAdj(edges, V)
    pq = []
    dist = [sys.maxsize] * V
    parent = [-1] * V

    heapq.heappush(pq, [0, src])
    dist[src] = 0

    while pq:
        u = heapq.heappop(pq)[1]
        for v, weight in adj[u]:
            if dist[v] > dist[u] + weight:
                dist[v] = dist[u] + weight
                parent[v] = u
                heapq.heappush(pq, [dist[v], v])

    return dist, parent

# Function to reconstruct path
def get_path(parent, dest):
    path = []
    while dest != -1:
        path.append(dest)
        dest = parent[dest]
    return path[::-1]

if __name__ == "__main__":
    V = int(input("Enter number of nodes (>=6): "))
    E = int(input("Enter number of edges: "))

    edges = []
    print(f"Enter edges in format: u v weight (nodes numbered from 1 to {V})")
    for _ in range(E):
        u, v, w = map(int, input().split())
        if u < 1 or v < 1 or u > V or v > V:
            print(f"❌ Invalid edge: {u} {v}. Nodes must be between 1 and {V}. Try again.")
            continue
        edges.append([u-1, v-1, w])  # store internally as 0-indexed

    src = int(input(f"Enter source node (1 to {V}): ")) - 1
    dest = int(input(f"Enter destination node (1 to {V}): ")) - 1

    dist, parent = dijkstra(V, edges, src)
    path = get_path(parent, dest)

    # Convert path back to 1-indexed for display
    path_display = [p+1 for p in path]

    print(f"\n✅ Shortest Distance from {src+1} to {dest+1}: {dist[dest]}")
    print("✅ Shortest Path:", " -> ".join(map(str, path_display)))

    # Build Graph (store as 1-indexed in nx.Graph for clarity)
    G = nx.Graph()
    for u, v, w in edges:
        G.add_edge(u+1, v+1, weight=w)

    pos = nx.spring_layout(G, seed=42)

    # Draw base graph
    nx.draw(G, pos, with_labels=True, node_size=800, node_color="lightblue", font_size=10)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    # Highlight shortest path
    path_edges = [(path_display[i], path_display[i+1]) for i in range(len(path_display)-1)]
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, width=3, edge_color="red")
    nx.draw_networkx_nodes(G, pos, nodelist=path_display, node_color="orange")

    plt.title(f"Shortest Path from {src+1} to {dest+1}")
    plt.show(block=True)   # ✅ Keeps window open
