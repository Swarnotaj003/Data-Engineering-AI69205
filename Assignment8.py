from collections import deque

"""
ASSIGNMENT 8
A common theory in communication network is that if two nodes are far apart (separated by
many hops/intermediate nodes), they have a weaker connection than the two nodes that are
close together.

In this context, suppose an n-node undirected, unweighted graph G = (V, E) contains two
nodes s and t such that the distance between s and t is strictly greater than n/2. Write a
program in python that will take a pair of nodes (s and t) and prints the nodes v (not equal to
s or t) such that v's removal from the graph will destroy all paths between s and t.

Assume that the graph will be given as a space separated two column text file, where each
line represents an edge. The nodes are in integer values starting from 1 to n (for n-node
graph).
"""

class CutVertexDetector:
    def read_graph(self, filename):
        """
        Construct adjacency list representation of the undirected and 
        unweighted graph whose edges are given in a two column text file.
        e.g. filename = 'files/graph-assgn-8.txt'
        """
        self.n = 0
        self.graph = {}

        try:
            with open(filename) as file:
                for line in file:
                    u, v = map(int, line.split())

                    if u not in self.graph:
                        self.graph[u] = []
                    if v not in self.graph:
                        self.graph[v] = []

                    self.graph[u].append(v)
                    self.graph[v].append(u)
                
                self.n = max(self.graph)
                print(f"\nConstructed graph (n = {self.n}):")
                print(self.graph)

        except Exception as e:
            print(f"ERROR in parsing input file! Path: {filename}")
            print(e)

    def bfs_distance(self, s, t):
        """
        Find the shortest distance between s and t using BFS
        """ 
        visited = {s}
        queue = deque([(s, 0)])

        while queue:
            u, distance = queue.popleft()

            # check if t is reached
            if u == t:
                return distance
            
            # explore the neighbour nodes of u
            for v in self.graph.get(u, []):
                if v not in visited:
                    visited.add(v)
                    queue.append((v, distance + 1))

        # s and t are disconnected
        return float("inf")
    
    def is_reachable(self, s, t, cv):
        """
        Check if t is reachable from s without the node cv
        """
        if s == cv or t == cv:
            return False
        
        # perform BFS starting from s
        visited = {s}
        queue = deque([s])

        while queue:
            u = queue.popleft()

            # check if t is reached
            if u == t:
                return True
            
            # explore the neighbour nodes of u
            for v in self.graph.get(u, []):
                if v != cv and v not in visited:
                    visited.add(v)
                    queue.append(v)

        # s and t are disconnected
        return False

    def detect_cut_vertices(self, filename, s, t):
        """
        Find all the vertices v such that removing v
        leads to removal of all paths between s and t
        """
        self.read_graph(filename)
        cut_vertices = []

        # check if s and t exists
        if s not in self.graph or t not in self.graph:
            raise ValueError("s and t must be contained in the nodes of the input graph!")
        
        # check if s and t are connected
        distance = self.bfs_distance(s, t)
        if distance == float("inf"):
            raise ValueError(f"s and t must be connected!")
        
        # check if s and t are more than n/2 distance apart
        if distance <= self.n / 2:
            raise ValueError(f"s and t must have distance greater than n/2 = {self.n / 2}!")

        # try removing all nodes except s and t
        for v in self.graph:
            if v == s or v == t:
                continue
            if not self.is_reachable(s, t, v):
                cut_vertices.append(v)

        return cut_vertices


if __name__ == "__main__":
    filename = input("Enter input file path for the graph: ")
    s, t = map(int, input("Enter s and t: ").split())
    try:
        cvd = CutVertexDetector()
        cut_vertices = cvd.detect_cut_vertices(filename, s, t)
        print("\nAll nodes v such that removal of v will destroy all paths between s and t:", cut_vertices)
    except Exception as e:
        print("\nERROR!", e)
