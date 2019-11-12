from shortest_path import shortest_path_dijkstra_multi_source_multi_target, shortest_path_dijkstra_multi_target

# Shortest trip from sources (hotels) to targets (hotels) visiting certain intermediate nodes (tourist attractions)
def shortest_trip_greedy(adj, sources, intermediates, targets):
    num = len(adj)
    num_sources = len(sources)
    num_intermediates = len(intermediates)
    num_targets = len(targets)
    # Sources to intermediate
    paths = [None] * num
    for s in sources:
        paths[s] = [s]
    D_0, t_0 = shortest_path_dijkstra_multi_source_multi_target(adj, sources, intermediates, pred=None, paths=paths)
    distance = D_0[t_0]
    path = paths[t_0]
    # Intermediate to intermediate
    source = t_0
    while intermediates:
        paths = [None] * num
        paths[source] = [source]
        D_i, t_i = shortest_path_dijkstra_multi_target(adj, source, intermediates, pred=None, paths=paths)
        distance += D_i[t_i]
        path += paths[t_i][1:]
        source = t_i
    # Intermediate to targets
    paths = [None] * num
    paths[source] = [source]
    D_n, t_n = shortest_path_dijkstra_multi_target(adj, source, targets, pred=None, paths=paths)
    distance += D_n[t_n]
    path += paths[t_n][1:]
    return distance, path
