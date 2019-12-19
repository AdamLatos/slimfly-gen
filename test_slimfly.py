from slimfly_gen import find_primitive, find_generator_sets, create_routes
import sys
from collections import deque

def test_primitive():
    q = 5
    Fq = range(q)
    primitive_elem = find_primitive(q, Fq)
    assert primitive_elem == 2

def test_generator_sets():
    q = 5
    primitive_elem = 2
    (X1, X2) = find_generator_sets(q, primitive_elem)
    assert X1 == [1,4] and X2 == [2,3]

def dijkstra(graph, source, dest):
    if source not in graph or dest not in graph:
        return None
    distances = {k: sys.maxsize for k in graph}
    previous_vertices = {k: None for k in graph}
    distances[source] = 0
    vertices = graph.copy()

    while vertices:
        current_vertex = min(vertices, key=lambda vertex: distances[vertex])
        if distances[current_vertex] == sys.maxsize:
            break
        for neighbour in graph[current_vertex]:
            alternative_route = distances[current_vertex] + 1
            if alternative_route < distances[neighbour]:
                distances[neighbour] = alternative_route
                previous_vertices[neighbour] = current_vertex
        vertices.pop(current_vertex, None)

    path, current_vertex = deque(), dest
    while previous_vertices[current_vertex] is not None:
        path.appendleft(current_vertex)
        current_vertex = previous_vertices[current_vertex]
    if path:
        path.appendleft(current_vertex)
    return path

def test_diameter():

    q = 5
    Fq = range(q)
    primitive_elem = 2
    (X1, X2) = ([1,4], [2,3])
    graph = create_routes(q, Fq, X1, X2)

    max_path = 0
    for router1 in graph:
        for router2 in graph:
            if router1 != router2:
                path = dijkstra(graph, router1, router2)
                if path is not None:
                    if(len(path)) > max_path:
                        max_path = len(path)
    assert max_path == 3