import csv
import math
import time
from queue import PriorityQueue, Queue

import numpy as np
from babel.numbers import format_scientific
from memory_profiler import memory_usage

from read_file import read_data_tsp, read_data_txt, read_ini_bnb


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
    # odczyt minimalnych wartości z każdego wiersza macierzy i skopiowanie macierzy do utworzenia nowej, zredukowanej
    min_rows = matrix.min(axis=1)
    reduced_matrix = np.copy(matrix)
    # pętla redukująca każdy wiersz macierzy
    for index, value in enumerate(min_rows):
        # jeśli wartość minimalna w wierszu jest równa nieskończoności to komórka jest pomijana
        if value == math.inf:
            continue
        # redukcja wiersza macierzy i dodanie minimum dla danego wiersza do sumarycznego kosztu
        reduced_matrix[index] -= min_rows[index]
        c += min_rows[index]

    # odczyt minimalnych wartości z każdej kolumny macierzy
    min_columns = reduced_matrix.min(axis=0)
    # pętla redukująca każdą kolumnę macierzy
    for index, value in enumerate(min_columns):
        # jeśli wartość minimalna w kolumnie jest równa nieskończoności to komórka jest pomijana
        if value == math.inf:
            continue
            # redukcja kolumny macierzy i dodanie minimum dla danej kolumny do sumarycznego kosztu
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
    # zainicjalizowanie zmiennych przechowujących: granicę wartości funkcji ograniczającej, wyznaczony optymalny koszt i optymalną ścieżkę
    min_bound = math.inf
    min_cost = math.inf
    path = []

    # zredukowanie macierzy sąsiedztwa
    adjacency_matrix, c = reduce_matrix(adjacency_matrix)

    # dodanie do ścieżki wierzchołka startowego i stworzenie stosu do przechowywania wierzchołków do odwiedzenia
    path.append(0)
    stack = [Node(0, path, c, adjacency_matrix)]
    # pętla odwiedzająca wszystkie wierzchołki znajdujące się na stosie
    while len(stack) > 0:
        node = stack.pop()
        # sprawdzenie czy koszt dla danego wierzchołka przekracza granicę, jeśli tak to jego gałąź jest pomijana
        if node.c > min_bound:
            continue
        # sprawdzenie czy wierzchołek jest liściem, jeśli tak to jego ścieżka ma długość równą liczbie wierzchołków
        if len(node.path) == vertex_number:
            # przypisanie nowej granicy i nowego optymalnego rozwiąania i ścieżki
            min_bound = node.c
            min_cost = min_bound
            node.path.append(0)
            path = node.path
            continue

        # pętla dodająca każdego nierozpatrzonego sąsiada wierzchołka o numerze node.vertex na stos
        for neighbor in graph.neighbors(node.vertex):
            # sprawdzenie czy dany wierzchołek był już rozpatrywany w ramach danej gałęzi
            if neighbor in node.path:
                continue

            new_matrix = insert_inf(node.matrix, node.vertex, neighbor)
            # redukcja macierzy dla sąsiedniego wierzchołka, obliczenie kosztu
            new_matrix, c = reduce_matrix(new_matrix)
            sum_cost = node.matrix[node.vertex][neighbor] + node.c + c
            # dodanie wierzchołka na stos wierzchołków do odwiedzenia
            stack.append(Node(neighbor, node.path + [neighbor], sum_cost, new_matrix))
    return min_cost, path

def bnb_best_first(adjacency_matrix, graph, vertex_number):
    # zainicjalizowanie zmiennych przechowujących: granicę wartości funkcji ograniczającej, wyznaczony optymalny koszt i optymalną ścieżkę
    min_bound = math.inf
    min_cost = math.inf
    path = []

    # zredukowanie macierzy sąsiedztwa
    adjacency_matrix, c = reduce_matrix(adjacency_matrix)

    # dodanie do ścieżki wierzchołka startowego i stworzenie kolejki priorytetowej do przechowywania wierzchołków do odwiedzenia
    path.append(0)
    queue = PriorityQueue()
    queue.put(Node(0, path, c, adjacency_matrix))

    # pętla odwiedzająca wszystkie wierzchołki znajdujące się w kolejce priorytetowej
    while queue.qsize() > 0:
        node = queue.get()

        # sprawdzenie czy koszt dla danego wierzchołka przekracza granicę, jeśli tak to jego gałąź jest pomijana
        if node.c > min_bound:
            continue
        # sprawdzenie czy wierzchołek jest liściem, jeśli tak to jego ścieżka ma długość równą liczbie wierzchołków
        if len(node.path) == vertex_number:
            # przypisanie nowej granicy i nowego optymalnego rozwiąania i ścieżki
            min_bound = node.c
            min_cost = min_bound
            node.path.append(0)
            path = node.path
            continue

        # pętla dodająca każdego nierozpatrzonego sąsiada wierzchołka o numerze node.vertex do kolejki priorytetowej
        for neighbor in graph.neighbors(node.vertex):
            if neighbor in node.path:
                continue
            new_matrix = insert_inf(node.matrix, node.vertex, neighbor)
            # redukcja macierzy dla sąsiedniego wierzchołka, obliczenie kosztu
            new_matrix, c = reduce_matrix(new_matrix)
            sum_cost = node.matrix[node.vertex][neighbor] + node.c + c
            # dodanie wierzchołka do kolejki priorytetowej wierzchołków do odwiedzenia
            queue.put(Node(neighbor, node.path + [neighbor], sum_cost, new_matrix))
    return min_cost, path


def main():
    # odczyt nazw plikó do testów i ich optymalnych rozwiązań jak i wybranej opcji przeszukiwania przestrzeni rozwiązań
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
                result = bnb_best_first(adjacency_matrix, graph, vertex_number)
                end = time.perf_counter()
                mem_usage = memory_usage((bnb_best_first, (adjacency_matrix, graph, vertex_number)))

            writer.writerow([format_scientific(end - start, locale="pl_Pl"), result[0], result[1], format_scientific(max(mem_usage), locale="pl_Pl")])
            print([format_scientific(end - start, locale="pl_Pl"), result[0], result[1]],  format_scientific(max(mem_usage), locale="pl_Pl"))

    file.close()


if __name__ == '__main__':
    main()