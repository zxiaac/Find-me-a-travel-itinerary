from shortest_path import shortest_path_dijkstra_multi_source_multi_target

A = [[(1, 2), (2, 1), (3, 3)], [(0, 2), (4, 2)], [(0, 1), (8, 5), (9, 1)], [(0, 3), (5, 1)], [(1, 2), (6, 4), (7, 4)]]
A += [[(3, 1), (9, 6), (18, 1), (10, 2)], [(4, 4), (7, 3), (11, 2), (19, 3)]]
A += [[(4, 4), (6, 3), (11, 2), (20, 2)], [(2, 5), (12, 1)], [(2, 1), (5, 6), (13, 5), (14, 2)]]
A += [[(5, 2), (14, 2), (18, 4)], [(6, 2), (7, 2), (15, 2), (20, 1)], [(8, 1), (13, 1), (16, 2), (17, 2)]]
A += [[(9, 5), (12, 1), (17, 2)], [(9, 2), (10, 2), (18, 2)]]
A += [[(11, 2), (19, 1)], [(12, 2), (17, 3)], [(12, 2), (13, 2), (16, 3), (19, 1)]]
A += [[(5, 1), (10, 4), (14, 2), (20, 4)], [(6, 3), (15, 1), (17, 1)]]
A += [[(7, 2), (11, 1), (17, 3), (18, 4)]]

sources = [0, 8, 9, 19]

paths = [None] * len(A)
for s in sources:
    paths[s] = [s]

pred = [None] * len(A)

D, _ = shortest_path_dijkstra_multi_source_multi_target(A, sources, targets=None, pred=pred, paths=paths)

print("Example: source nodes are 0, 8, 9, 19. Calculate the shortest path from any source node to all other nodes.")
for i in range(len(A)):
    print("node {0}: distance = {1}, shortest path is {2}, predecessors are {3}.".format(i, D[i], paths[i], pred[i]))
