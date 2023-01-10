import math

import numpy as np


def nearest_neighbour(adjacency_matrix, vertex_number):
    vertexes = np.arange(1, vertex_number)
    last_vertex = 0
    cost = 0
    while len(vertexes) != 0:
        unvisited_neighbours = {index[0]: value for index, value in np.ndenumerate(adjacency_matrix[last_vertex]) if value != math.inf and index in vertexes}
        next_vertex = min(unvisited_neighbours, key=unvisited_neighbours.get)
        cost += adjacency_matrix[last_vertex][next_vertex]
        vertexes = vertexes[vertexes != next_vertex]
        last_vertex = next_vertex

    return cost


def calculate_cost(solution, adjacency_matrix):
    cost = 0
    for index, vertex in np.ndenumerate(solution[:-1]):
        cost += adjacency_matrix[vertex][solution[index[0]+1]]
    last_vertex = solution[index[0]+1]
    cost += adjacency_matrix[last_vertex][solution[0]]
    return cost