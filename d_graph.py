# Course: CS261 - Data Structures
# Author: Jonathon Stoddart
# Assignment: 6
# Description: Part 2 - Directed Graph (via Adjacency Matrix)


import heapq as heap


class DirectedGraph:
    """
    Class to implement directed weighted graph
    - duplicate edges not allowed
    - loops not allowed
    - only positive edge weights
    - vertex names are integers
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency matrix
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.v_count = 0
        self.adj_matrix = []

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            v_count = 0
            for u, v, _ in start_edges:
                v_count = max(v_count, u, v)
            for _ in range(v_count + 1):
                self.add_vertex()
            for u, v, weight in start_edges:
                self.add_edge(u, v, weight)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if self.v_count == 0:
            return 'EMPTY GRAPH\n'
        out = '   |'
        out += ' '.join(['{:2}'.format(i) for i in range(self.v_count)]) + '\n'
        out += '-' * (self.v_count * 3 + 3) + '\n'
        for i in range(self.v_count):
            row = self.adj_matrix[i]
            out += '{:2} |'.format(i)
            out += ' '.join(['{:2}'.format(w) for w in row]) + '\n'
        out = f"GRAPH ({self.v_count} vertices):\n{out}"
        return out

    # ------------------------------------------------------------------ #

    def add_vertex(self) -> int:
        """
        Adds a new vertex to the graph. Returns an integer number of vertices in the graph after the addition.
        """
        self.v_count += 1  # update vertex count

        for row in self.adj_matrix:  # add new column to existing rows
            row.append(0)

        self.adj_matrix.append([0]*self.v_count)  # add new row

        return self.v_count

    def add_edge(self, src: int, dst: int, weight=1) -> None:
        """
        Adds a new edge to the graph, connecting vertex src to vertex dst. If either vertex does not exist, weight is 
        not a positive integer, or if src and dst refer to the same vertex, method does nothing. If the edge already
        exists, the method will update its weight.
        """
        if 0 <= src < self.v_count and 0 <= dst < self.v_count and weight > 0 and src != dst:
            self.adj_matrix[src][dst] = weight  # set/update weight

    def remove_edge(self, src: int, dst: int) -> None:
        """
        Removes an edge between vertex src and vertex dst. If either vertex does not exist, or there is no edge
        between them, the method does nothing.
        """
        if 0 <= src < self.v_count and 0 <= dst < self.v_count:
            self.adj_matrix[src][dst] = 0
       
    def get_vertices(self) -> []:
        """
        Returns a list of vertices in the graph.
        """
        vertices = []
        
        for i in range(self.v_count):
            vertices.append(i)

        return vertices

    def get_edges(self) -> []:
        """
        Returns a list of edges in the graph. 
        Each edge is returned as a tuple: (source vertex, destination vertex, weight)
        """
        edges = []

        for src in range(self.v_count):  # source vertices
            for dst in range(self.v_count):  # destination vertices
                if self.adj_matrix[src][dst] != 0:  # edge weight
                    edges.append((src, dst, self.adj_matrix[src][dst]))

        return edges

    def is_valid_path(self, path: []) -> bool:
        """
        Takes a list of vertex indices and returns True if the sequence of vertices represents a valid path in the
        graph (from first to last vertex, at each step traversing over an edge in the graph).
        An empty path is considered valid.
        """
        if len(path) == 0:
            return True
        
        for i in range(len(path)-1):
            # check source and destination exist
            if path[i] < 0 or path[i] >= self.v_count or path[i+1] < 0 or path[i+1] >= self.v_count:
                return False
            # check edge exists
            if self.adj_matrix[path[i]][path[i+1]] == 0:
                return False
        
        return True

    def dfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during DFS search
        Vertices are picked in ascending order
        """
        if v_start not in range(0, self.v_count):  # start vertex not in graph
            return []

        visited = []  # stack of visited vertices
        stack = []  # stack of neighbors to visit
        stack.append(v_start)

        while len(stack) != 0:
            src = stack.pop()
            if src == v_end:  # we have reached the end. add to visited and return
                visited.append(src)
                return visited
            elif src not in visited:  # avoid duplicates
                visited.append(src)
                for dst in range(self.v_count-1, -1, -1):  # all vertices in descending order (due to stack nature)
                    if self.adj_matrix[src][dst] != 0:  # check edge exists
                        stack.append(dst)

        return visited

    def bfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during BFS search
        Vertices are picked in ascending order
        """
        if v_start not in range(0, self.v_count):
            return []
        
        visited = []
        queue = []
        queue.append(v_start)

        while len(queue) != 0:
            src = queue.pop(0)  # pop first element since list is a queue and not a stack
            if src == v_end:
                visited.append(src)
                return visited
            elif src not in visited:
                visited.append(src)
                for dst in range(self.v_count):  # vertices in ascending order (queue)
                    if self.adj_matrix[src][dst] != 0 and dst not in visited:
                        queue.append(dst)

        return visited

    def has_cycle(self):
        """
        Return True if graph contains a cycle, False otherwise
        """
        if 0 <= self.v_count <= 1 :  # 0 or 1 vertices - no cycle
            return False

        white = []  # unvisited list
        grey = []  # visiting list (if we encounter one of these, there is a cycle)
        black = []  # visited list (all its neighbors have also been visited)

        for i in range(self.v_count):  # fill unvisited list
            white.append(i)

        while len(white) > 0:
            src = white[0]  # arbitrary starting point for DFS
            if self.rec_cycle(src, white, grey, black):
                return True
        return False

    def rec_cycle(self, src, white, grey, black):
        """
        DFS search helper method for has_cycle. Takes a source vertex - if we have visited but not fully explored one
        of its neighbors, we found a cycle and the method returns True. If we have not visited a neighbor, method
        recurses, visiting and exploring that neighbor. If no cycles are found, returns False.
        """
        white.remove(src)
        grey.append(src)

        for dst in range(self.v_count):
            if self.adj_matrix[src][dst] != 0:
                if dst in black:  # already fully explored
                    continue
                if dst in grey:  # found a cycle
                    return True
                if self.rec_cycle(dst, white, grey, black):  # must be in white - recurse
                    return True

        grey.remove(src)  # src has been fully explored (all neighbors explored) - return False
        black.append(src)
        return False

    def dijkstra(self, src: int) -> []:
        """
        Implements the Dijkstra algorithm to compute the length of the shortest path from a given vertex src to
        all other vertices in the graph. Returns a list with one value per each vertex in the graph, where the value
        at index 0 is the length of the shortest path from vertex src to vertex 0, etc. If a vertex is not reachable
        from src, the respective value in the list is INFINITY. Assumes src is a valid vertex.
        """
        min_paths = []  # list of shortest distances to each vertex
        pq = [(0, src)]  # priority queue - [priority, vertex] where priority is distance

        for i in range(self.v_count):
            min_paths.append(float('inf'))  # initialize all min paths as infinity (unreachable)

        while len(pq) > 0:
            d, v = heap.heappop(pq)
            if d < min_paths[v]:  # new shortest path
                min_paths[v] = d
                for vi in range(self.v_count):  # find direct successors and enqueue them with their current path distance to priority queue
                    if self.adj_matrix[v][vi] != 0:
                        di = self.adj_matrix[v][vi]
                        pq.append((d + di, vi))

        return min_paths


if __name__ == '__main__':

    print("\nPDF - method add_vertex() / add_edge example 1")
    print("----------------------------------------------")
    g = DirectedGraph()
    print(g)
    for _ in range(5):
        g.add_vertex()
    print(g)

    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    for src, dst, weight in edges:
        g.add_edge(src, dst, weight)
    print(g)


    print("\nPDF - method get_edges() example 1")
    print("----------------------------------")
    g = DirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    print(g.get_edges(), g.get_vertices(), sep='\n')


    print("\nPDF - method is_valid_path() example 1")
    print("--------------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    test_cases = [[0, 1, 4, 3], [1, 3, 2, 1], [0, 4], [4, 0], [], [2]]
    for path in test_cases:
        print(path, g.is_valid_path(path))


    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    for start in range(5):
        print(f'{start} DFS:{g.dfs(start)} BFS:{g.bfs(start)}')


    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)

    edges_to_remove = [(3, 1), (4, 0), (3, 2)]
    for src, dst in edges_to_remove:
        g.remove_edge(src, dst)
        print(g.get_edges(), g.has_cycle(), sep='\n')

    edges_to_add = [(4, 3), (2, 3), (1, 3), (4, 0)]
    for src, dst in edges_to_add:
        g.add_edge(src, dst)
        print(g.get_edges(), g.has_cycle(), sep='\n')
    print('\n', g)


    print("\nPDF - dijkstra() example 1")
    print("--------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')
    g.remove_edge(4, 3)
    print('\n', g)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')
