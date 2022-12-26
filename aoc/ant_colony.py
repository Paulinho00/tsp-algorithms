import csv
import math
import time

import numpy as np
from babel.numbers import format_scientific
from memory_profiler import memory_usage

from aoc.read_file import read_ini, read_data_tsp, read_data_txt


def get_initial_solution(adjacency_matrix: np.ndarray, vertex_number: int) -> np.ndarray:
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


def calculate_cost(solution: np.ndarray, adjacency_matrix: np.ndarray) -> int:
    cost = 0
    for index, vertex in np.ndenumerate(solution[:-1]):
        cost += adjacency_matrix[vertex][solution[index[0]+1]]
    last_vertex = solution[index[0]+1]
    cost += adjacency_matrix[last_vertex][solution[0]]
    return cost


def initialize_pheromone_matrix(vertex_number: int, aproximate_cost: int ) -> np.ndarray:
    starting_pheromone = vertex_number / aproximate_cost
    pheromone_matrix = np.full((vertex_number, vertex_number), starting_pheromone)
    return pheromone_matrix


def aoc(adjacency_matrix: np.ndarray, vertex_number: int, number_of_iterations: int):
    initial_solution = get_initial_solution(adjacency_matrix, vertex_number)
    initial_solution_cost = calculate_cost(initial_solution, adjacency_matrix)
    pheromone_matrix = initialize_pheromone_matrix(vertex_number, initial_solution_cost)
    while number_of_iterations > 0:
        pass


def main():
    parameters, alpha, beta, is_cas = read_ini()
    file = open(parameters.pop()[0], 'w', newline='')
    writer = csv.writer(file, delimiter=";")

    for parameters in parameters:
        if parameters[0].endswith(".tsp") or parameters[0].endswith(".atsp"):
            adjacency_matrix, vertex_number = read_data_tsp(parameters[0])
        else:
            adjacency_matrix, vertex_number = read_data_txt(parameters[0])

        optimal = float(parameters[2])
        writer.writerow([parameters[0], parameters[1], parameters[2]])
        for i in range(0, int(parameters[1])):
            start = time.perf_counter()
            result = aoc(adjacency_matrix, vertex_number, 100)
            end = time.perf_counter()
            error = (result[1] - optimal)/optimal * 100
            if end - start > 1800:
                print(f"Abort for: {parameters[0]}")
                break
            mem_usage = memory_usage((aoc, ()))
            writer.writerow([format_scientific(end - start, locale="pl_Pl"), list(result[0]), result[1], str(error).replace('.', ','), format_scientific(max(mem_usage), locale="pl_Pl")])
            print([format_scientific(end - start, locale="pl_Pl"), list(result[0]), result[1]], str(error).replace('.', ','), format_scientific(max(mem_usage), locale="pl_Pl"))

    file.close()


if __name__ == '__main__':
    main()