from itertools import permutations, product
from sys import maxsize


def read_data_file(filename, adjacency_matrix):
    file = open(filename, "r")
    file_lines = file.read().splitlines()
    vertex_number = int(file_lines[0])

    for line in range(1, len(file_lines)):
        list_of_strings = file_lines[line].split()
        adjacency_matrix.append(list(map(int, list_of_strings)))

    return vertex_number


def read_ini():
    parameters = []
    file = open("config.ini", "r")
    file_lines = file.read().splitlines()

    for line in file_lines:
        instance_parameters = line.split(',')
        parameters.append(instance_parameters)

    return parameters


def tsp_brute_force(adjacency_matrix, vertex_number):
    vertexes = list(range(1, vertex_number))
    paths = permutations(vertexes)
    min_path = maxsize
    min_vertex_path = []
    for path in paths:
        current_pathweight = 0
        current_vertex = 0
        for vertex in path:
            current_pathweight += adjacency_matrix[current_vertex][vertex]
            current_vertex = vertex
        current_pathweight += adjacency_matrix[current_vertex][0]

        if min_path > current_pathweight:
            min_path = current_pathweight
            min_vertex_path = (0,) + path + (0,)

    return (min_path, min_vertex_path)


def main():
    adjacency_matrix = []
    parameters = read_ini()
    for parameters in parameters:
        adjacency_matrix.clear()
        vertex_number = read_data_file(parameters[0], adjacency_matrix)
        result = tsp_brute_force(adjacency_matrix, vertex_number)
        print(result)


if __name__ == '__main__':
    main()
