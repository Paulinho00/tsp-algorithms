import csv
from datetime import time

from babel.numbers import format_scientific
from memory_profiler import memory_usage

from simulated_annealing.read_file import read_ini, read_data_tsp, read_data_txt



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
            # result = held_karp(adjacency_matrix, vertex_number)
            end = time.perf_counter()
            # mem_usage = memory_usage((held_karp, (adjacency_matrix, vertex_number)))
            # writer.writerow([format_scientific(end - start, locale="pl_Pl"), result[0], result[1], format_scientific(max(mem_usage), locale="pl_Pl")])
            # print([format_scientific(end - start, locale="pl_Pl"), result[0], result[1]], format_scientific(max(mem_usage), locale="pl_Pl"))

    file.close()


if __name__ == '__main__':
    main()