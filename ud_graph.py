# Course: CS 261 - Data Structures
# Author: Jonathon Stoddart
# Assignment: 6
# Description: Part 1 - Undirected Graph (via Adjacency List)


class UndirectedGraph:
    """
    Class to implement undirected graph
    - duplicate edges not allowed
    - loops not allowed
    - no edge weights
    - vertex names are strings
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency list
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.adj_list = dict()

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            for u, v in start_edges:
                self.add_edge(u, v)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = [f'{v}: {self.adj_list[v]}' for v in self.adj_list]
        out = '\n  '.join(out)
        if len(out) < 70:
            out = out.replace('\n  ', ', ')
            return f'GRAPH: {{{out}}}'
        return f'GRAPH: {{\n  {out}}}'

    # ------------------------------------------------------------------ #

    def add_vertex(self, v: str) -> None:
        """
        Add new vertex to the graph. If a vertex with the same name is already present, does nothing.
        """
        if v not in self.adj_list:
            self.adj_list[v] = []  # create vertex in graph
        
    def add_edge(self, u: str, v: str) -> None:
        """
        Add edge to the graph, connecting the two vertices u and v. If either vertex does not exist,
        it will be created then the edge will be created between them. If an edge already exists or u and v
        are the same vertex, does nothing.
        """
        if u != v:
            if u not in self.adj_list:  # check if vertex u exists
                self.add_vertex(u)
            if v not in self.adj_list:  # check if vertex v exists
                self.add_vertex(v)
            if u not in self.adj_list[v]:  # check if edge exists
                self.adj_list[u].append(v)
                self.adj_list[v].append(u)

    def remove_edge(self, v: str, u: str) -> None:
        """
        Remove edge from the graph, disconnecting vertices v and u. If either vertex does not exist or there
        is no edge between them, does nothing.
        """
        if v in self.adj_list:  # check that vertex v exists
            if u in self.adj_list[v]:  # check that edge to/from u exists
                self.adj_list[v].remove(u)
                self.adj_list[u].remove(v)
        
    def remove_vertex(self, v: str) -> None:
        """
        Remove vertex and all connected edges
        """
        # if vertex exists, delete it (and its listed edges)
        if v in self.adj_list:
            del self.adj_list[v]

        # remove all incidences of v stored as a neighbor of another vertex
        for vertex, neighbors in self.adj_list.items():
            if v in neighbors:
                neighbors.remove(v)

    def get_vertices(self) -> []:
        """
        Return list of vertices in the graph (any order)
        """
        vertices = []

        for vertex in self.adj_list.keys():  # fill vertices list
            vertices.append(vertex)

        return vertices

    def get_edges(self) -> []:
        """
        Return list of edges in the graph (any order)
        """
        edges = []

        for vertex, neighbors in self.adj_list.items():
            for neighbor in neighbors:
                if (neighbor, vertex) not in edges:  # avoid duplicates i.e. (A, B) and (B, A)
                    edges.append((vertex, neighbor))
        
        return edges

    def is_valid_path(self, path: []) -> bool:
        """
        Return true if provided path is valid, False otherwise
        """
        if len(path) == 0:  # an empty path is considered valid
            return True

        if path[0] not in self.adj_list:  # check if starting vertex exists
            return False

        for v in range(len(path)-1):  # check if each edge in path exists
            if path[v+1] not in self.adj_list[path[v]]:
                return False

        return True

    def dfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during DFS search
        Vertices are picked in alphabetical order
        """
        if v_start not in self.adj_list:  # start vertex not in graph
            return []

        visited = []  # stack of visited vertices
        stack = []  # stack of neighbors to visit
        stack.append(v_start)

        while len(stack) != 0:
            v = stack.pop()
            if v == v_end:  # we have reached the end. add to visited and return
                visited.append(v)
                return visited
            elif v not in visited:  # avoid duplicates
                visited.append(v)
                for neighbor in sorted(self.adj_list[v], key=None, reverse=True):  # direct successors in descending alphabetical order (stack)
                    stack.append(neighbor)

        return visited

    def bfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during BFS search
        Vertices are picked in alphabetical order
        """
        if v_start not in self.adj_list:
            return []
        
        visited = []
        queue = []
        queue.append(v_start)

        while len(queue) != 0:
            v = queue.pop(0)  # pop first element since list is a queue and not a stack
            if v == v_end:
                visited.append(v)
                return visited
            elif v not in visited:
                visited.append(v)
                for neighbor in sorted(self.adj_list[v]):  # direct successors in ascending alphabetical order (queue)
                    if neighbor not in visited:
                        queue.append(neighbor)

        return visited        

    def count_connected_components(self):
        """
        Return number of connected componets in the graph
        """
        if len(self.adj_list) == 0:  # empty graph - no conencted components
            return 0

        components = []  # list of components
        visited = []  # vertices visited by dfs search

        # run a dfs search for each unvisited vertex in the graph
        for v in self.adj_list:
            if v not in visited:  # skip vertices we already visited in a previous dfs search
                component = self.dfs(v)
                components.append(component)
                for u in component:  # mark each vertex in the component as visited
                    visited.append(u)

        return len(components)

    def has_cycle(self):
        """
        Return True if graph contains a cycle, False otherwise
        """
        if 0 <= len(self.adj_list) <= 1 :  # 0 or 1 vertices - no cycle
            return False

        # first find components that will later undergo BFS search
        components = []
        visited = []

        # run a dfs search for each unvisited vertex in the graph
        for v in self.adj_list:
            if v not in visited:  # skip vertices we already visited in a previous dfs search
                component = self.dfs(v)
                components.append(component)
                for u in component:  # mark each vertex in the component as visited
                    visited.append(u)

        # conduct BFS search on each component to determine whether graph is cyclic or acyclic
        for component in components:
            visited = []
            queue = []
            queue.append(component[0])

            while len(queue) != 0:
                v = queue.pop(0)
                if v not in visited:
                    visited.append(v)
                    for neighbor in sorted(self.adj_list[v]):
                        if neighbor in queue and neighbor not in visited:
                            # if current vertex and a visited vertex share a neighbor, we have a cycle
                            return True
                        queue.append(neighbor)

        return False


if __name__ == '__main__':

    print("\nPDF - method add_vertex() / add_edge example 1")
    print("----------------------------------------------")
    g = UndirectedGraph()
    print(g)

    for v in 'ABCDE':
        g.add_vertex(v)
    print(g)

    g.add_vertex('A')
    print(g)

    for u, v in ['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE', ('B', 'C')]:
        g.add_edge(u, v)
    print(g)


    print("\nPDF - method remove_edge() / remove_vertex example 1")
    print("----------------------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    g.remove_vertex('DOES NOT EXIST')
    g.remove_edge('A', 'B')
    g.remove_edge('X', 'B')
    print(g)
    g.remove_vertex('D')
    print(g)


    print("\nPDF - method get_vertices() / get_edges() example 1")
    print("---------------------------------------------------")
    g = UndirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE'])
    print(g.get_edges(), g.get_vertices(), sep='\n')


    print("\nPDF - method is_valid_path() example 1")
    print("--------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    test_cases = ['ABC', 'ADE', 'ECABDCBE', 'ACDECB', '', 'D', 'Z']
    for path in test_cases:
        print(list(path), g.is_valid_path(list(path)))


    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = 'ABCDEGH'
    for case in test_cases:
        print(f'{case} DFS:{g.dfs(case)} BFS:{g.bfs(case)}')
    print('-----')
    for i in range(1, len(test_cases)):
        v1, v2 = test_cases[i], test_cases[-1 - i]
        print(f'{v1}-{v2} DFS:{g.dfs(v1, v2)} BFS:{g.bfs(v1, v2)}')


    print("\nPDF - method count_connected_components() example 1")
    print("---------------------------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = (
        'add QH', 'remove FG', 'remove GQ', 'remove HQ',
        'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
        'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
        'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG')
    for case in test_cases:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print(g.count_connected_components(), end=' ')
    print()


    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = (
        'add QH', 'remove FG', 'remove GQ', 'remove HQ',
        'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
        'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
        'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG',
        'add FG', 'remove GE')
    for case in test_cases:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print('{:<10}'.format(case), g.has_cycle())
