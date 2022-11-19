import csv
import math
import time

import numpy as np
from babel.numbers import format_scientific
from memory_profiler import memory_usage

from read_file import read_ini, read_data_tsp, read_data_txt

def get_initial_solution(adjacency_matrix, vertex_number):
    vertexes = np.arange(1, vertex_number)
    solution = np.arange(0, 1)
    last_vertex = 0
    while len(vertexes) != 0:
        possible_neighbors = [index[0] for index, value in np.ndenumerate(adjacency_matrix[last_vertex]) if value != math.inf and index in vertexes ]
        next_vertex_index = np.random.randint(len(possible_neighbors))
        last_vertex = possible_neighbors[next_vertex_index]
        solution = np.append(solution, last_vertex)
        vertexes = np.delete(vertexes, next_vertex_index)
    return solution

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

def set_initial_temp(rate, adjacency_matrix, vertex_number):
    cost = nearest_neighbour(adjacency_matrix, vertex_number)
    return cost * rate

def simulated_annealing(adjacency_matrix, vertex_number):
    first_solution = get_initial_solution(adjacency_matrix, vertex_number)
    temp = set_initial_temp(100, adjacency_matrix, vertex_number)
    pass

def main():
    parameters = read_ini()
    file = open(parameters.pop()[0], 'w', newline='')
    writer = csv.writer(file, delimiter=";")

    for parameters in parameters:
        if parameters[0].endswith(".tsp"):
            adjacency_matrix, vertex_number = read_data_tsp(parameters[0])
        else:
            adjacency_matrix, vertex_number = read_data_txt(parameters[0])

        writer.writerow([parameters[0], parameters[1], parameters[2], parameters[3]])
        for i in range(0, int(parameters[1])):
            start = time.perf_counter()
            result = simulated_annealing(adjacency_matrix, vertex_number)
            end = time.perf_counter()
            # mem_usage = memory_usage((held_karp, (adjacency_matrix, vertex_number)))
            # writer.writerow([format_scientific(end - start, locale="pl_Pl"), result[0], result[1], format_scientific(max(mem_usage), locale="pl_Pl")])
            # print([format_scientific(end - start, locale="pl_Pl"), result[0], result[1]], format_scientific(max(mem_usage), locale="pl_Pl"))

    file.close()


if __name__ == '__main__':
    main()