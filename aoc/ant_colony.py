import csv
import math
import random
import time
import numpy as np
from babel.numbers import format_scientific
from memory_profiler import memory_usage

from aoc.ant.Ant import Ant
from aoc.path_functions.path_functions import calculate_cost, get_initial_solution
from aoc.read_file import read_ini, read_data_tsp, read_data_txt


def initialize_pheromone_matrix(vertex_number, aprox_cost):
    starting_pheromone = vertex_number / aprox_cost
    pheromone_matrix = np.full((vertex_number, vertex_number), starting_pheromone)
    return pheromone_matrix


def select_vertex(ant, adjacency_matrix, vertex_number, alpha, beta, pheromone_matrix):

    probabilities = list()
    for vertex in ant.unvisited_vertices:
        if adjacency_matrix[ant.current_vertex][vertex] > 0:
            probabilities.append(pow(pheromone_matrix[ant.current_vertex][vertex], alpha) *\
                                     pow(1 / adjacency_matrix[ant.current_vertex][vertex], beta))
        else:
            probabilities.append(pow(pheromone_matrix[ant.current_vertex][vertex], alpha) *\
                                     pow(1 / 0.1, beta))

    return random.choices(ant.unvisited_vertices, weights=probabilities)


def evaporate_cas(pheromone_matrix, ant_colony, adjacency_matrix):
    pheromone_matrix = np.multiply(pheromone_matrix, 0.5)
    for ant in ant_colony:
        path_cost = calculate_cost(ant.path, adjacency_matrix)
        for index, vertex in enumerate(ant.path[:-1]):
            pheromone_matrix[vertex][ant.path[index+1]] += 100 / path_cost

    return pheromone_matrix


def aoc(adjacency_matrix, vertex_number,
        alpha, beta, is_cas):
    solution_cost = math.inf
    solution = []
    initial_solution = get_initial_solution(adjacency_matrix, vertex_number)
    initial_solution_cost = calculate_cost(initial_solution, adjacency_matrix)
    pheromone_matrix = initialize_pheromone_matrix(vertex_number, initial_solution_cost)
    ant_counter = 0
    while ant_counter < 1000:
        ant_colony = [Ant(vertex, vertex_number) for vertex in range(vertex_number)]
        for ant in ant_colony:
            while len(ant.path) != vertex_number:
                selected_vertex = select_vertex(ant, adjacency_matrix, vertex_number, alpha, beta, pheromone_matrix)
                if not is_cas:
                    if adjacency_matrix[ant.current_vertex][selected_vertex] != 0:
                        pheromone_matrix[ant.current_vertex][selected_vertex] +=\
                            100 / adjacency_matrix[ant.current_vertex][selected_vertex]
                    else:
                        pheromone_matrix[ant.current_vertex][selected_vertex] += \
                            100 / 0.1
                ant.visit(selected_vertex[0])
            path_cost = calculate_cost(ant.path, adjacency_matrix)
            if path_cost < solution_cost:
                solution_cost = path_cost
                solution = ant.path

        if is_cas:
            pheromone_matrix = evaporate_cas(pheromone_matrix, ant_colony, adjacency_matrix)
        else:
            pheromone_matrix = np.multiply(pheromone_matrix, 0.5)
        ant_counter += vertex_number
    solution = np.append(solution, solution[0])
    return solution, solution_cost


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
            result = aoc(adjacency_matrix, vertex_number, alpha, beta, is_cas)
            end = time.perf_counter()
            error = (result[1] - optimal)/optimal * 100
            if end - start > 1800:
                print(f"Abort for: {parameters[0]}")
                break
            mem_usage = memory_usage((aoc, (adjacency_matrix, vertex_number, alpha, beta, is_cas)))
            writer.writerow([format_scientific(end - start, locale="pl_Pl"), list(result[0]), result[1],
                             str(error).replace('.', ','), format_scientific(max(mem_usage), locale="pl_Pl")])
            print([format_scientific(end - start, locale="pl_Pl"), list(result[0]), result[1]],
                  str(error).replace('.', ','), format_scientific(max(mem_usage), locale="pl_Pl"))

    file.close()


if __name__ == '__main__':
    main()
