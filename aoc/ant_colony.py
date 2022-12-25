import csv
import time

from babel.numbers import format_scientific
from memory_profiler import memory_usage

from aoc.read_file import read_ini, read_data_tsp, read_data_txt

def aoc():
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
            result = aoc()
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