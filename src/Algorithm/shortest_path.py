from heapq import heappush, heappop

def shortest_path_dijkstra_multi_source_multi_target(adj, sources, targets=None, pred=None, paths=None):
    A = adj # adjacency matrix; for node i, A[i] is a list of tuple (adjacent node, edge weight)
    D = {} # final distance of nodes that have seen its adjacent nodes
    D_seen = {} # temporary distance of nodes seen by at least one of their adjacent nodes
    fringe = [] # nodes that have been seen but have not seen other nodes
    shortest_target = None
    for s in sources:
        D_seen[s] = 0
        heappush(fringe, (0, s)) # use fringe as a heap containing tuple: (temporary distance, node)
    while fringe:
        (d, v) = heappop(fringe)
        if v in D:
            continue # d is already final distance and cannot become smaller
        D[v] = d
        if shortest_target is not None and v not in sources:
            shortest_target = v
        if targets is not None:
            if v in targets:
                targets.remove(v)
                shortest_target = v
                break # has already found the shortest target
        # update the temporary distance of all adjacent nodes
        for u, w in A[v]:
            new_d = D[v] + w
            if u not in D_seen or new_d < D_seen[u]:
                D_seen[u] = new_d
                heappush(fringe, (new_d, u))
                if paths is not None:
                    paths[u] = paths[v] + [u] # update current shortest path from a source to u
                if pred is not None:
                    pred[u] = [v] # update the predecessor of u
            elif new_d == D_seen[u]:
                if pred is not None:
                    pred[u].append(v) # update the predecessor of u; may not find all predecessors
    return D, shortest_target

# Multi source single target
def shortest_path_dijkstra_multi_source(adj, sources, target=None, pred=None, paths=None):
    D, _ = shortest_path_dijkstra_multi_source_multi_target(adj, sources, targets=[target], pred=pred, paths=paths)
    return D

# Single source multi target
def shortest_path_dijkstra_multi_target(adj, source, targets=None, pred=None, paths=None):
    D, shortest_target = shortest_path_dijkstra_multi_source_multi_target(adj, [source], targets=targets, pred=pred, paths=paths)
    return D, shortest_target

# Single source single target
def shortest_path_dijkstra(adj, source, target=None, pred=None, paths=None):
    D, _ = shortest_path_dijkstra_multi_source_multi_target(adj, [source], targets=[target], pred=pred, paths=paths)
    return D
