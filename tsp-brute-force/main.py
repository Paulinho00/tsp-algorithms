def read_file(filename, adjacency_matrix):
    file = open(filename, "r")
    file_lines = file.read().splitlines()
    vertex_number = file_lines[0]
    for line in range(1, len(file_lines)):
        list_of_strings = file_lines[line].split()
        adjacency_matrix.append(list(map(int, list_of_strings)))

    return vertex_number


def main():
    adjacency_matrix = []
    vertex_number = read_file("tsp_10.txt", adjacency_matrix)
    pass

if __name__ == '__main__':
    main()
