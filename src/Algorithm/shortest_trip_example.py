from shortest_trip import shortest_trip_greedy

##########################################################################################################################
# Example:                                                                                                               #
# A map contains 21 point of interests (POIs): node 0, ..., node 20.                                                     #
# Node 0, 8, 9, 10 are hotels, and others are tourist attractions.                                                       #
# A user decides to visit node 4, 5, 13.                                                                                 #
# He wants to find a shortest path, starting at a hotel, ending at a hotel, and visiting the three tourists attractions. #
##########################################################################################################################

# Build the adjacency matrix
A = [[(1, 2), (2, 1), (3, 3)], [(0, 2), (4, 2)], [(0, 1), (8, 5), (9, 1)], [(0, 3), (5, 1)], [(1, 2), (6, 4), (7, 4)]]
A += [[(3, 1), (9, 6), (18, 1), (10, 2)], [(4, 4), (7, 3), (11, 2), (19, 3)]]
A += [[(4, 4), (6, 3), (11, 2), (20, 2)], [(2, 5), (12, 1)], [(2, 1), (5, 6), (13, 5), (14, 2)]]
A += [[(5, 2), (14, 2), (18, 4)], [(6, 2), (7, 2), (15, 2), (20, 1)], [(8, 1), (13, 1), (16, 2), (17, 2)]]
A += [[(9, 5), (12, 1), (17, 2)], [(9, 2), (10, 2), (18, 2)]]
A += [[(11, 2), (19, 1)], [(12, 2), (17, 3)], [(12, 2), (13, 2), (16, 3), (19, 1)]]
A += [[(5, 1), (10, 4), (14, 2), (20, 4)], [(6, 3), (15, 1), (17, 1)]]
A += [[(7, 2), (11, 1), (17, 3), (18, 4)]]

# Start at one of the hotels
sources = [0, 8, 9, 19]

# End at one of the hotels
targets = [0, 8, 9, 19]

# Visit all the following tourist attractions
intermediates = [4, 5, 13]

# Calaulate the shortest trip
distance, path = shortest_trip_greedy(A, sources, intermediates, targets)

# Compare and print out the results
print("Hotels are 0, 8, 9, 19; Need to visit nodes 4, 5, 13")
print("The intended outcome by the greedy algorithm should be:")
print("8 -> 12 -> 13: distance = 2")
print("13 -> 17 -> 19 -> 6 -> 4: distance = 10")
print("4 -> 1 -> 0 -> 3 -> 5: distance = 8")
print("5 -> 3 -> 0: distance = 4")
print("Total distance = 24\n")
print("Result by the algorithm:")
print("distance = {0}, path = {1}".format(distance, path))
