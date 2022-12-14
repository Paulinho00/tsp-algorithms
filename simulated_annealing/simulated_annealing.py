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
        possible_neighbors = [index[0] for index, value in np.ndenumerate(adjacency_matrix[last_vertex]) if value != math.inf and index in vertexes]
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


def set_initial_temp(adjacency_matrix, vertex_number):
    cost = nearest_neighbour(adjacency_matrix, vertex_number)
    return cost / vertex_number


def swap2(solution, vertex_number):
    index_first_vertex = np.random.randint(0, vertex_number)
    index_second_vertex = np.random.randint(0, vertex_number)
    if index_second_vertex == index_first_vertex:
        return solution
    else:
        new_solution = np.copy(solution)
        new_solution[index_second_vertex] = solution[index_first_vertex]
        new_solution[index_first_vertex] = solution[index_second_vertex]

    return new_solution


def invert(solution, vertex_number):
    index_first_vertex = np.random.randint(2, vertex_number)
    index_second_vertex = np.random.randint(0, vertex_number)
    if index_second_vertex == index_first_vertex:
        return solution
    else:
        low_index = min(index_first_vertex, index_second_vertex)
        high_index = max(index_first_vertex, index_second_vertex)
        new_solution = np.copy(solution)
        new_solution[low_index:high_index+1] = new_solution[low_index:high_index+1][::-1]
    return new_solution


def calculate_cost(solution, adjacency_matrix):
    cost = 0
    for index, vertex in np.ndenumerate(solution[:-1]):
        cost += adjacency_matrix[vertex][solution[index[0]+1]]
    last_vertex = solution[index[0]+1]
    cost += adjacency_matrix[last_vertex][solution[0]]
    return cost


def anneal_temp_geo(temp, alpha, k):
    return math.pow(alpha, k) * temp


def anneal_temp_log(temp, alpha, k, beta=0.01):
    return temp / (alpha + beta * math.log10(k))


def simulated_annealing(adjacency_matrix, vertex_number, era_length, alpha, beta, is_geo_annealing, is_swap):
    solution = get_initial_solution(adjacency_matrix, vertex_number)
    solution_cost = calculate_cost(solution, adjacency_matrix)
    prev_cost = math.inf
    temp = set_initial_temp(adjacency_matrix, vertex_number)
    iterations_without_new_solution = 0
    iteration_counter = 1
    while iterations_without_new_solution < 50:
        iteration_counter += 1
        i = era_length
        if prev_cost == solution_cost:
            iterations_without_new_solution += 1
        else:
            iterations_without_new_solution = 0
        prev_cost = solution_cost
        while i > 0:
            if is_swap:
                new_solution = swap2(solution, vertex_number)
            else:
                new_solution = invert(solution, vertex_number)
            new_cost = calculate_cost(new_solution, adjacency_matrix)
            cost_difference = new_cost - solution_cost
            if cost_difference < 0:
                solution = new_solution
                solution_cost = new_cost
            else:
                random_float = np.random.uniform()
                probability = math.exp(-cost_difference/temp)
                if random_float < probability:
                    solution = new_solution
                    solution_cost = new_cost
            i -= 1
        if is_geo_annealing:
            temp = anneal_temp_geo(temp, alpha, iteration_counter)
        else:
            temp = anneal_temp_log(temp, alpha, beta, iteration_counter)

    solution = np.append(solution, solution[0])
    return solution, solution_cost


def main():
    parameters, era_length, alpha, beta, is_geo, is_swap = read_ini()
    file = open(parameters.pop()[0], 'w', newline='')
    writer = csv.writer(file, delimiter=";")

    for parameters in parameters:
        if parameters[0].endswith(".tsp") or parameters[0].endswith(".atsp"):
            adjacency_matrix, vertex_number = read_data_tsp(parameters[0])
        else:
            adjacency_matrix, vertex_number = read_data_txt(parameters[0])

        optimal = float(parameters[2])
        writer.writerow([parameters[0], parameters[1], parameters[2], parameters[3]])
        for i in range(0, int(parameters[1])):
            start = time.perf_counter()
            result = simulated_annealing(adjacency_matrix, vertex_number, era_length, alpha, beta, is_geo, is_swap)
            end = time.perf_counter()
            error = (result[1] - optimal)/optimal * 100
            if end - start > 1800:
                print(f"Abort for: {parameters[0]}")
                break
            mem_usage = memory_usage((simulated_annealing, (adjacency_matrix, vertex_number, era_length, alpha, beta, is_geo, is_swap)))
            writer.writerow([format_scientific(end - start, locale="pl_Pl"), list(result[0]), result[1], str(error).replace('.', ','), format_scientific(max(mem_usage), locale="pl_Pl")])
            print([format_scientific(end - start, locale="pl_Pl"), list(result[0]), result[1]], str(error).replace('.', ','), format_scientific(max(mem_usage), locale="pl_Pl"))

    file.close()


if __name__ == '__main__':
    main()