import math
import os

def readFile(filename):
    dirname = os.path.dirname(__file__)
    path = os.path.join(dirname, filename)
    f = open(path, "r")

    f = f.readlines()
    graphs = []
    for i in range(len(f)):
        f[i] = f[i][:-1]    #get rid of \n character
        f[i] = f[i].split(' ')
        graphs.append(f[i])
    return graphs

def parse(input):
    nodes = input[0][2:-2]
    nodes = nodes.split('),(')
    for i in range(len(nodes)):
        nodes[i] = nodes[i].split(',')

    edges = input[1][2:-2]
    edges = edges.split('),(')
    for i in range(len(edges)):
        edges[i] = edges[i].split(',')

    return nodes, edges

def output(graphs):
    counter = 1
    dirname = os.path.dirname(__file__)
    path = os.path.join(dirname, "alphabeta_out.txt")
    open(path, "w").close()
    out = open(path, "a")

    for i in graphs:
        nodes, edges = parse(i)
        T = Tree(nodes, edges)
        T.buildTree()
        score = T.alpha_beta(T.root, None, None)
        out.write("Graph {}: Score: {}; Leaf Nodes Examined: {}\n".format(counter, score, T.count))
        counter += 1

class Node:
    
    def __init__(self, value):
        self.value = value
        self.children = []      #children should be a list of nodes
        self.minmax = None

class Tree:

    def __init__(self, nodes, edges):
        self.root = None
        self.nodes = nodes
        self.edges = edges
        self.tree = []
        self.count = 0      #count leaf nodes visited

    def buildTree(self):      

        node_list = []
        for i in self.nodes:
            node = Node(i[0])
            node.minmax = i[1]
            node_list.append(node)

        for i in node_list:
            for j in self.edges:
                if i.value == j[0]:
                    if j[1].isdigit():
                        node = Node(j[1])
                        i.children.append(node)
    
                    for k in node_list:
                            if j[1] == k.value:
                                i.children.append(k)

        self.tree = node_list
        self.root = self.tree[0]
        return

    def alpha_beta(self, current_node, alpha, beta): #, nodes_left):

        if current_node == self.root:
            alpha = -math.inf
            beta = math.inf
        if len(current_node.children) == 0:      #if current node is leaf node:
            self.count += 1
            return int(current_node.value)       #return static evaluation of current node

        if current_node.minmax == 'MAX':
            for child in current_node.children:
                alpha = max(alpha, self.alpha_beta(child, alpha, beta))
                if alpha >= beta:
                    return alpha
            return alpha
        if current_node.minmax == 'MIN':
            for child in current_node.children:
                beta = min(beta, self.alpha_beta(child, alpha, beta))
                if alpha >= beta:
                    return beta
            return beta             

if __name__ == "__main__":
    graphs = readFile("alphabeta.txt")
    output(graphs)