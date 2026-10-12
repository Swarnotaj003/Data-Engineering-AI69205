"""
ASSIGNMENT 10

A weighted undirected graph (V,E) is given, where all weights are positive. Your
goal is to cluster (or group) the nodes of the graph based on its strongest
neighbour as follows.

Two nodes v1 and v2 will be in the same group, if v1 is the strongest neighbour
of v2 or v2 is the strongest neighbour of v1.

Strongest neighbour v of a node u, is defined as follows: v must be adjacent to
u and v has the highest edge weight from u from among all its (u's) neighbours.
Implement an algorithm in python. 

Input file format: Space separated three column file for an edge. The nodes are
given as consecutive integers starting from 1. For example, a line in the input file
will look like:
5 10 6.7
Above line means, there is an edge between the nodes 5 and 10 with weight 6.7

Output format: Output must be printed on screen. Each line in output contains
the comma separated nodes in a group. An example output format is given
below.
1,2,5,7
3,4,6
The above means the graph has two groups: the first group contains four
nodes and the second group contains 3 nodes.
"""

class ClusterNodes:
    def __init__(self):
        self.n = 0
        self.adj_list = {}

    def read_graph(self, filename):
        """
        Construct adjacency list representation of the weighted undirected 
        graph whose edges are given in a three column text file.
        """
        try:
            with open(filename) as file:
                for line in file:
                    u, v, w = line.split()
                    u, v = map(int, (u, v))
                    w = float(w)

                    if u not in self.adj_list:
                        self.adj_list[u] = []
                    if v not in self.adj_list:
                        self.adj_list[v] = []

                    self.adj_list[u].append((v, w))
                    self.adj_list[v].append((u, w))
                    self.n = max(self.n, max(u, v)) 

                print(f"\nConstructed graph (n = {self.n}):")
                print(self.adj_list)

        except Exception as e:
            print(f"ERROR in parsing input file! Path: {filename}")
            print(e)

    def form_clusters(self):
        """
        Cluster nodes based on strongest neighbor test
        """
        # initialize parent and rank arrays
        self.parent = list(range(self.n + 1))
        self.rank = [0] * (self.n + 1)

        # node 0 is undefined
        self.parent[0] = -1    
        self.rank[0] = -1 

        for u in range(1, self.n + 1):
            # find the strongest neighbor of node u
            best_v = None
            best_w = float("-inf")
            for v, w in self.adj_list[u]:
                if w > best_w:
                    best_v = v
                    best_w = w

            # merge u with its strongest neighbor (if any) into the same set
            if best_v is not None:
                self.union(u, best_v)

        # create clusters {(parent: [nodes])}
        clusters = {}
        for u in range(1, self.n + 1):
            root = self.find(u)
            clusters.setdefault(root, []).append(u)
        
        return clusters

    # Methods for Disjoint Set Union (DSU)
    def find(self, u):
        """
        Find the set representative of node u using path compression
        """
        if self.parent[u] != u:
            self.parent[u] = self.find(self.parent[u])

        return self.parent[u]
    
    def union(self, u, v):
        """
        Merge the nodes u and v into the same set using rank
        """
        root_u = self.find(u)
        root_v = self.find(v)

        if root_u == root_v:
            return
        
        if self.rank[root_u] < self.rank[root_v]:
            self.parent[root_u] = root_v
        elif self.rank[root_u] > self.rank[root_v]:
            self.parent[root_v] = root_u
        else:
            self.parent[root_v] = root_u
            self.rank[root_u] += 1


if __name__ == "__main__":
    # Example: files/graph-assgn-10.txt
    filename = input("Enter input file path for the graph: ")
    try:
        cn = ClusterNodes()
        cn.read_graph(filename)
        clusters = cn.form_clusters()

        print("\nClustered nodes:")
        for cluster in clusters.values():
            print(",".join(map(str, cluster)))

    except Exception as e:
        print("\nERROR!", e)
