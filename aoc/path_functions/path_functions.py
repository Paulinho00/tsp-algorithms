import math

import numpy as np


def get_initial_solution(adjacency_matrix, vertex_number):
    vertices = np.arange(1, vertex_number)
    solution = np.arange(0, 1)
    last_vertex = 0
    while len(vertices) != 0:
        possible_neighbors = [index[0] for index, value in np.ndenumerate(adjacency_matrix[last_vertex]) if value != math.inf and index in vertices]
        next_vertex_index = np.random.randint(len(possible_neighbors))
        last_vertex = possible_neighbors[next_vertex_index]
        solution = np.append(solution, last_vertex)
        vertices = np.delete(vertices, next_vertex_index)
    return solution


def calculate_cost(solution, adjacency_matrix):
    cost = 0
    for index, vertex in np.ndenumerate(solution[:-1]):
        cost += adjacency_matrix[vertex][solution[index[0]+1]]
    last_vertex = solution[index[0]+1]
    cost += adjacency_matrix[last_vertex][solution[0]]
    return cost