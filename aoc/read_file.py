import math

import networkx
import numpy as np
import tsplib95


def read_data_txt(filename: str) -> (np.ndarray, int):
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
    return adjacency_matrix, vertex_number


def read_data_tsp(filename: str) -> (np.ndarray, int):
    tsp = tsplib95.load(filename)
    graph = tsp.get_graph()
    adjacency_matrix = networkx.to_numpy_array(graph)
    adjacency_matrix = insert_inf(adjacency_matrix)
    return adjacency_matrix, len(adjacency_matrix)


def read_ini() -> (list, float, float, bool):
    parameters = []
    file = open("config.ini", "r")
    file_lines = file.read().splitlines()
    for index, line in enumerate(file_lines):
        if index == 0:
            options = line.split(',')
            alpha = float(options[0])
            beta = float(options[1])
            is_cas = bool(options[2])
            continue
        instance_parameters = line.split(',')
        parameters.append(instance_parameters)

    return parameters, alpha, beta, is_cas


def insert_inf(matrix: np.ndarray) -> np.ndarray:
    length = len(matrix)
    for index, row in enumerate(matrix):
        row[index] = math.inf

    return matrix