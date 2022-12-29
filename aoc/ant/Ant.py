import numpy as np


class Ant:
    def __init__(self, current_vertex, vertex_number):
        self.current_vertex = current_vertex
        self.unvisited_vertices = [vertex for vertex in range(vertex_number) if vertex != current_vertex]
        self.path = np.array([current_vertex, ])

    def visit(self, vertex):
        self.current_vertex = vertex
        self.path = np.append(self.path, vertex)
        self.unvisited_vertices.remove(vertex)
