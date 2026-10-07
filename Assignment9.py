"""
ASSIGNMENT 9

Write a python program for the following operations on graph. Assume that the graph is undirected.
1. Create adjacency matrix representation of the graph.
2. Create adjacency list representation of the graph.
3. For a given node, list its neighbours.
4. Given two nodes, find the common neighbours of these two nodes.
5. List the nodes based on descending order of degrees.

Assume that the graph will be given as a space separated two column text file, where each
line represents an edge. The nodes are in integer values starting from 1 to n (for n-node
graph). For example, a file and its graph is given below.
1 2
2 3
1 4
2 4
"""

class GraphOps:
    def __init__(self):
        self.n = 0
        self.edge_list = []

    def read_graph(self, filename):
        """
        Fetch edge list of undirected graph from the two column text file.
        """
        try:
            with open(filename) as file:
                for line in file:
                    u, v = map(int, line.split())
                    self.edge_list.append((u, v))   
                    self.n = max(self.n, max(u, v))   

            return self.edge_list
        
        except Exception as e:
            print(f"ERROR in parsing input file! Path: {filename}")
            print(e)

    def build_adj_matrix(self):
        """
        Create adjacency matrix representation of the graph.
        """
        self.adj_matrix = [[0 for j in range(self.n)] for i in range(self.n)]

        for u, v in self.edge_list:
            self.adj_matrix[u-1][v-1] = 1
            self.adj_matrix[v-1][u-1] = 1

        return self.adj_matrix

    def build_adj_list(self):
        """
        Create adjacency list representation of the graph.
        """
        self.adj_list = {node: [] for node in range(1, self.n + 1)}

        for u, v in self.edge_list:
            self.adj_list[u].append(v)
            self.adj_list[v].append(u)

        return self.adj_list

    def list_neighbors(self, node):
        """
        For the given node, list its neighbours.
        """
        if node not in self.adj_list:
            raise ValueError(f"Node {node} is not present in the graph!")
        
        return self.adj_list[node]
    
    def list_common_neighbors(self, node1, node2):
        """
        Given two nodes, find the common neighbours of these two nodes.
        """
        if node1 not in self.adj_list:
            raise ValueError(f"Node {node1} is not present in the graph!")
        if node2 not in self.adj_list:
            raise ValueError(f"Node {node2} is not present in the graph!")
        
        mask1 = sum(self.adj_matrix[node1 - 1][i] << i for i in range(self.n))
        mask2 = sum(self.adj_matrix[node2 - 1][i] << i for i in range(self.n))
        common_mask = mask1 & mask2
        common_list = []
        neighbor = 1

        while common_mask:
            if (common_mask & 1):
                common_list.append(neighbor)
            common_mask >>= 1
            neighbor += 1

        return common_list
    
    def sort_nodes_by_degree(self):
        """
        List the nodes based on descending order of degrees.
        """
        return sorted(self.adj_list, key = lambda x: len(self.adj_list[x]), reverse = True)


if __name__ == "__main__":
    # e.g. filename = 'graph-assgn-9.txt'
    filename = input("Enter input file path for the graph: ")
    try:
        go = GraphOps()
        edges = go.read_graph(filename)
        adj_matrix = go.build_adj_matrix()
        adj_list = go.build_adj_list()

        print("\nEdge list:", edges)
        print("\nAdjacency matrix:")
        for row in adj_matrix:
            print(row)
        print("\nAdjacency list:", adj_list)

        node = int(input("\nEnter a node: "))
        node_neighbors = go.list_neighbors(node)
        print(f"Neighbors of {node}: {node_neighbors}")

        node1, node2 = map(int, input("\nEnter two nodes (u v): ").split())
        common_neighbors = go.list_common_neighbors(node1, node2)
        print(f"Common neighbors of {node1} and {node2}: {common_neighbors}")

        nodes_sorted = go.sort_nodes_by_degree()
        print("\nNodes ordered by descending degree:", nodes_sorted)

    except Exception as e:
        print("\nERROR!", e)
