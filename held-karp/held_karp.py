import csv
import itertools
import time

from babel.numbers import format_scientific
from memory_profiler import memory_usage

from read_file import read_ini, read_data_tsp, read_data_txt


def held_karp(adjacency_vertix, vertex_number):
    subsets = {}
    parents = {}
    for i in range(1, vertex_number):
        subsets[((i,), i)] = (adjacency_vertix[0][i], 0)
        parents[((i,), i)] = 0

    for j in range(2, vertex_number):
        for subset in itertools.combinations(range(1, vertex_number), j):

            for last_vertex_in_subset in subset:
                vertexes = [vertex for vertex in subset if vertex != last_vertex_in_subset]

                path_weights = []
                for n in vertexes:
                    if (tuple(vertexes), n) in subsets.keys():
                        path_weights.append(
                            (subsets[(tuple(vertexes), n)][0] + adjacency_vertix[n][last_vertex_in_subset],
                             n,
                             (tuple(vertexes), n)))

                subsets[tuple(subset), last_vertex_in_subset] = (min(path_weights)[0], min(path_weights)[1])
                parents[tuple(subset), last_vertex_in_subset] = min(path_weights)[2]

    route = []
    vertex_set = tuple(range(1, vertex_number))

    for i in vertex_set:
        route.append((subsets[(vertex_set, i)][0] + adjacency_vertix[i][0], i))

    optimal_cost = min(route)[0]

    min_path = [0, min(route)[1]]
    parent = parents[(vertex_set, min_path[1])]
    for i in range(2, vertex_number):
        min_path.append(parent[1])
        parent = parents[parent]
        pass

    min_path.append(0)
    min_path.reverse()
    return min_path, optimal_cost


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
            result = held_karp(adjacency_matrix, vertex_number)
            end = time.perf_counter()
            mem_usage = memory_usage((held_karp, (adjacency_matrix, vertex_number)))
            writer.writerow([format_scientific(end - start, locale="pl_Pl"), result[0], result[1], max(mem_usage)])
            print([format_scientific(end - start, locale="pl_Pl"), result[0], result[1]], max(mem_usage))

    file.close()


if __name__ == '__main__':
    main()
