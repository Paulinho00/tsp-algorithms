import math

import networkx
import numpy as np
import tsplib95


def read_data_txt(filename):
    adjacency_matrix = []
    file = open(filename, "r")
    file_lines = file.read().splitlines()
    vertex_number = int(file_lines[0])

    for line in range(1, len(file_lines)):
        list_of_strings = file_lines[line].split()
        adjacency_matrix.append(list(map(float, list_of_strings)))

    adjacency_matrix = np.array(adjacency_matrix)
    graph = networkx.from_numpy_matrix(adjacency_matrix)
    adjacency_matrix = insert_inf(adjacency_matrix)
    return adjacency_matrix, vertex_number, graph


def read_data_tsp(filename):
    tsp = tsplib95.load(filename)
    graph = tsp.get_graph()
    adjacency_matrix = networkx.to_numpy_array(graph)
    adjacency_matrix = insert_inf(adjacency_matrix)
    return adjacency_matrix, len(adjacency_matrix), graph


def read_ini():
    parameters = []
    file = open("config.ini", "r")
    file_lines = file.read().splitlines()
    for line in file_lines:
        instance_parameters = line.split(',')
        parameters.append(instance_parameters)

    return parameters


def insert_inf(matrix):
    length = len(matrix)
    for index, row in enumerate(matrix):
        row[index] = math.inf

    return matrix