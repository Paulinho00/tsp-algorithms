import csv
import math
import time
from queue import PriorityQueue, Queue

import numpy as np
from babel.numbers import format_scientific
from memory_profiler import memory_usage

from read_file import read_ini, read_data_tsp, read_data_txt, read_ini_bnb


class Node:
    def __init__(self, vertex, path, c, matrix):
        self.vertex = vertex
        self.path = path
        self.c = c
        self.matrix = matrix

    def __lt__(self, other):
        self_cost = self.c
        other_cost = other.c
        return self_cost < other_cost


def reduce_matrix(matrix):
    c = 0
    min_rows = matrix.min(axis=1)
    reduced_matrix = np.copy(matrix)
    for index, value in enumerate(min_rows):
        if value == math.inf:
            continue
        reduced_matrix[index] -= min_rows[index]
        c += min_rows[index]



    min_columns = reduced_matrix.min(axis=0)
    for index, value in enumerate(min_columns):
        if value == math.inf:
            continue
        reduced_matrix[:,index] -= min_columns[index]
        c += min_columns[index]

    return reduced_matrix, c


def insert_inf(matrix, vertex1, vertex2):
    new_matrix = np.copy(matrix)
    new_matrix[vertex1] = math.inf
    new_matrix[:,vertex2] = math.inf
    new_matrix[vertex1][vertex2] = math.inf
    return new_matrix


def bnb_dfs(adjacency_matrix, graph, vertex_number):
    min_bound = math.inf
    min_cost = math.inf
    adjacency_matrix, c = reduce_matrix(adjacency_matrix)
    path = []
    path.append(0)
    stack = [Node(0, path, c, adjacency_matrix)]
    while len(stack) > 0:
        node = stack.pop()
        if node.c > min_bound:
            continue
        if len(node.path) == vertex_number:
            min_bound = node.c
            min_cost = min_bound
            node.path.append(0)
            path = node.path
            continue

        for neighbor in graph.neighbors(node.vertex):
            if neighbor in node.path:
                continue
            new_matrix = insert_inf(node.matrix, node.vertex, neighbor)
            new_matrix, c = reduce_matrix(new_matrix)
            sum_cost = node.matrix[node.vertex][neighbor] + node.c + c
            stack.append(Node(neighbor, node.path + [neighbor], sum_cost, new_matrix))
    return min_cost, path


def bnb_bfs(adjacency_matrix, graph, vertex_number):
    min_bound = math.inf
    min_cost = math.inf
    adjacency_matrix, c = reduce_matrix(adjacency_matrix)
    path = []
    path.append(0)
    queue = Queue()
    queue.put(Node(0, path, c, adjacency_matrix))
    while queue.qsize() > 0:
        node = queue.get()
        if node.c > min_bound:
            continue
        if len(node.path) == vertex_number:
            min_bound = node.c
            min_cost = min_bound
            node.path.append(0)
            path = node.path
            continue

        for neighbor in graph.neighbors(node.vertex):
            if neighbor in node.path:
                continue
            new_matrix = insert_inf(node.matrix, node.vertex, neighbor)
            new_matrix, c = reduce_matrix(new_matrix)
            sum_cost = node.matrix[node.vertex][neighbor] + node.c + c
            queue.put(Node(neighbor, node.path + [neighbor], sum_cost, new_matrix))
    return min_cost, path

def bnb_best_first(adjacency_matrix, graph, vertex_number):
    min_bound = math.inf
    min_cost = math.inf
    adjacency_matrix, c = reduce_matrix(adjacency_matrix)
    path = []
    path.append(0)
    queue = PriorityQueue()
    queue.put(Node(0, path, c, adjacency_matrix))
    while queue.qsize() > 0:
        node = queue.get()
        if node.c > min_bound:
            continue
        if len(node.path) == vertex_number:
            min_bound = node.c
            min_cost = min_bound
            node.path.append(0)
            path = node.path
            continue

        for neighbor in graph.neighbors(node.vertex):
            if neighbor in node.path:
                continue
            new_matrix = insert_inf(node.matrix, node.vertex, neighbor)
            new_matrix, c = reduce_matrix(new_matrix)
            sum_cost = node.matrix[node.vertex][neighbor] + node.c + c
            queue.put(Node(neighbor, node.path + [neighbor], sum_cost, new_matrix))
    return min_cost, path


def main():
    parameters, option = read_ini_bnb()
    file = open(parameters.pop()[0], 'w', newline='')
    writer = csv.writer(file, delimiter=";")

    for parameters in parameters:
        if parameters[0].endswith(".tsp"):
            adjacency_matrix, vertex_number, graph = read_data_tsp(parameters[0])
        else:
            adjacency_matrix, vertex_number, graph = read_data_txt(parameters[0])

        writer.writerow([parameters[0], parameters[1], parameters[2], parameters[3]])
        for i in range(0, int(parameters[1])):
            if option == 1:
                start = time.perf_counter()
                result = bnb_dfs(adjacency_matrix, graph, vertex_number)
                end = time.perf_counter()
                mem_usage = memory_usage((bnb_dfs, (adjacency_matrix, graph, vertex_number)))
            elif option == 2:
                start = time.perf_counter()
                result = bnb_bfs(adjacency_matrix, graph, vertex_number)
                end = time.perf_counter()
                mem_usage = memory_usage((bnb_bfs, (adjacency_matrix, graph, vertex_number)))
            elif option == 3:
                start = time.perf_counter()
                result = bnb_best_first(adjacency_matrix, graph, vertex_number)
                end = time.perf_counter()
                mem_usage = memory_usage((bnb_best_first, (adjacency_matrix, graph, vertex_number)))

            writer.writerow([format_scientific(end - start, locale="pl_Pl"), result[0], result[1], format_scientific(max(mem_usage), locale="pl_Pl")])
            print([format_scientific(end - start, locale="pl_Pl"), result[0], result[1]], format_scientific(max(mem_usage), locale="pl_Pl"))

    file.close()


if __name__ == '__main__':
    main()