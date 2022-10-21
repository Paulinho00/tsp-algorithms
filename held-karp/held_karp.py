import csv

from read_file import read_ini, read_data_tsp, read_data_txt


def main():
    parameters = read_ini()
    file = open(parameters.pop()[0], 'w', newline='')
    writer = csv.writer(file, delimiter=";")

    for parameters in parameters:
        if(parameters[0].endswith(".tsp")):
            adjacency_matrix, vertex_number = read_data_tsp(parameters[0])
        else:
            adjacency_matrix, vertex_number = read_data_txt(parameters[0])

        pass

if __name__ == '__main__':
    main()
    pass