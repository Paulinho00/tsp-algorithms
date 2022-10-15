# PEA - projekt WT 15:15
# Brute force
# Paweł Gryglewicz 259136
import csv
import time
from itertools import combinations
from sys import maxsize
from babel.numbers import format_scientific
from more_itertools import distinct_permutations


def read_data(filename, adjacency_matrix):
    file = open(filename, "r")
    file_lines = file.read().splitlines()
    vertex_number = int(file_lines[0])

    for line in range(1, len(file_lines)):
        list_of_strings = file_lines[line].split()
        adjacency_matrix.append(list(map(int, list_of_strings)))

    return vertex_number


def calculate_vertex_dict(adjacency_matrix):
    dictionary = {}
    for i in range(0, len(adjacency_matrix)):
        dictionary_vertex = {}
        for j in range(0, len(adjacency_matrix[i])):
            dictionary_vertex[j] = adjacency_matrix[i][j]
        dictionary[i] = dictionary_vertex

    return dictionary


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
    # generowanie wszystkich możliwych ścieżek, poprzez obliczenie permutacji wierzchołków.
    paths = distinct_permutations(vertexes)
    min_path = maxsize
    min_vertex_path = []

    # przekonwertowanie macierzy sąsiedztwa na słownik wierzchołków w celu przyśpieszenia algorytmu
    vertexes_dict = calculate_vertex_dict(adjacency_matrix)

    # pętla sprawdzająca wszystkie możliwe ścieżki
    for path in paths:

        # koszt ścieżki
        current_pathweight = 0

        # aktualnie odwiedzany wierzchołek
        current_vertex = 0

        # pętla przechodząca po każdym wierzchołku w ścieżce
        for vertex in path:
            # dodanie krawędzi z obecnego wierzchołka do poprzedniego wierzchołka do sumarycznego kosztu ścieżki
            current_pathweight += vertexes_dict[current_vertex][vertex]

            # sprawdzenie czy koszt ścieżki przekroczył  już  znaleziony najmniejszy koszt
            if current_pathweight > min_path:
                break
            current_vertex = vertex

        # dodanie do kosztu ścieżki, wagi krawędzi z ostatniego wierzchołka do początkowego wierzchołka ścieżki
        current_pathweight += vertexes_dict[current_vertex][0]

        # sprawdzenie czy koszt sprawdzonej ścieżki jest mniejszy niż aktualny najmniejszy koszt
        if min_path > current_pathweight:
            # przypisanie nowego najmniejszego kosztu ścieżki
            min_path = current_pathweight
            # uzupełnienie wyświetlanej ścieżki o wierzchołek początkowy i końcowy
            min_vertex_path = (0,) + path + (0,)

    return min_path, min_vertex_path


def main():
    adjacency_matrix = []
    parameters = read_ini()
    file = open(parameters.pop()[0], 'w', newline='')
    writer = csv.writer(file, delimiter=";")

    for parameters in parameters:
        adjacency_matrix.clear()

        # wczytanie danych z pliku dla danej instancji
        vertex_number = read_data(parameters[0], adjacency_matrix)
        writer.writerow([parameters[0], parameters[1], parameters[2], parameters[3]])
        for i in range(0, int(parameters[1])):
            start = time.perf_counter()
            result = tsp_brute_force(adjacency_matrix, vertex_number)
            end =  time.perf_counter()
            # zapis wyniku
            writer.writerow([format_scientific(end - start, locale="pl_Pl"), result[0], result[1]])
    file.close()


if __name__ == '__main__':
    main()
