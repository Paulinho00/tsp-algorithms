import csv
import itertools
import multiprocessing
import time

from babel.numbers import format_scientific
from memory_profiler import memory_usage

from read_file import read_ini, read_data_tsp, read_data_txt


def held_karp(adjacency_vertix, vertex_number):
    # inicjalizacja słownika przechowującego rozwiązania podproblemów
    subsets = {}
    # pętla dodająca koszty ścieżek miedzy w. startowym a w. sąsiednimi
    for i in range(1, vertex_number):
        subsets[((i,), i)] = (adjacency_vertix[0][i], 0)

    # pętla obliczająca rozwiązania dla coraz dłuższych kombinacji
    for i in range(2, vertex_number):
        # pętla generująca wszystkie możliwe kombinacje o długości i
        for subset in itertools.combinations(range(1, vertex_number), i):

            # pętla rozpatrująca każdy wierzchołek w kombinacji jako ostatni w ścieżce
            for last_vertex_in_subset in subset:
                # tworzenie zbioru który posłuży jako klucz do odczytu rozwiązania
                vertexes = [vertex for vertex in subset if vertex != last_vertex_in_subset]

                path_weights = []
                # pętla rozpatrująca każdy wierzchołek w vertexes jako ostatni w celu stworzenia pełnego klucza i odczytu rozwiązania
                for n in vertexes:
                    # sprawdzenie czy istnieje klucz (vertexes, n)
                    if (tuple(vertexes), n) in subsets.keys():
                        # obliczenie kosztu aktualnie rozpatrywanej ścieżki przy użyciu odczytanego rozwiązania wcześniejszego podproblemu
                        path_weights.append(
                            (subsets[(tuple(vertexes), n)][0] + adjacency_vertix[n][last_vertex_in_subset],
                             n))

                # wyznaczenie optymalnego kosztu rozpatrywanej ścieżki spośród wyznaczonych w poprzednim kroku i zapisanie go do słownika
                subsets[tuple(subset), last_vertex_in_subset] = (min(path_weights)[0], min(path_weights)[1])

    route = []
    # stworzenie zbioru wszystkich wierzchołków
    vertex_set = list(range(1, vertex_number))

    # pętla obliczająca wszystkie potencjalne optymalne ścieżki
    for i in vertex_set:
        # dodanie do listy route kosztu potencjalnie optymalnej ścieżki
        route.append((subsets[(tuple(vertex_set), i)][0] + adjacency_vertix[i][0], i))

    # znalezienie najbardziej optymalnej ścieżki spośród potencjalnie optymalnych
    optimal_cost = min(route)[0]

    # inicjalizacja zmiennych przechowujących odtwarzaną ścięzkę
    min_path = [0, min(route)[1]]
    # inicjalizacja zmiennej przechowującej ostatni element w ścieżce
    parent = min(route)[1]

    # dopóki ścieżka nie zawiera wszystkich wierzchołków, odtwarzanie ścieżki jest kontynuowane
    while len(min_path) != vertex_number:
        # odczyt następnego wierzchołka ze słownika rozwiązań, przy użyciu parent i zbioru niedodanych do ścieżki wierzchołkó
        next_parent = subsets[tuple(vertex_set), parent][1]
        # usunięcie ze zbioru niedodanych wierzchołków ostatniego elementu w ścieżce i
        vertex_set.remove(parent)
        parent = next_parent
        # dodanie do ścieżki wcześniej odczytany wierzchołek
        min_path.append(parent)

    # dodanie do śćieżki 0
    min_path.append(0)
    # odwrócenie ścieżki
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
            writer.writerow([format_scientific(end - start, locale="pl_Pl"), result[0], result[1], format_scientific(max(mem_usage), locale="pl_Pl")])
            print([format_scientific(end - start, locale="pl_Pl"), result[0], result[1]], format_scientific(max(mem_usage), locale="pl_Pl"))

    file.close()


if __name__ == '__main__':
    main()
