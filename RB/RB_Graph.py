"""
<Red and Blue game>
Author: Jihoo Brian Park, William Hsu
Class: Graph Class
Discription: This generates Erdos-Renyi graph.
Default color is grey. when nodes are marked by player, graph updates the node color.
"""
import networkx as nx
import sys
import matplotlib.pyplot as plt


class Graph(object):
  
    def __init__(self, nodeNum, prob):
        self.nodeNum = nodeNum
        self.graph = nx.erdos_renyi_graph(nodeNum,prob)
        self.pos=nx.spring_layout(self.graph)
        #set node attribute 
        self.attrs = {}
        for num in range(self.nodeNum):
            self.attrs[num] = {'number':num,'color':'grey'}
        nx.set_node_attributes(self.graph,self.attrs)

    def getValidMoves(self):
        """
        Get the list of nodes that have not been colored yet.
        :return: a list of node numbers that are available to be chosen as the next move
        """
        valid_moves = []
        gamestate = nx.get_node_attributes(self.graph, 'color')
        for node in gamestate:
            if gamestate.get(node) == 'grey':
                valid_moves.append(node)

        return valid_moves

    def mark(self, player, node):
        """
        mark node that player has chosen.
        return tuple: number of nodes added and number of node subtracted
        """
        colored_nodes = 0
        subtracted_nodes = 0
        if self.attrs[node]['color'] == 'grey':
            self.attrs[node]['color'] = player
            colored_nodes+=1
        else:
            sys.stderr.write('node does not exist or taken')
            return(0,0)
            
        for nodes in self.graph.neighbors(node):
            if (self.attrs[nodes]['color'] != player) and (self.attrs[nodes]['color'] != 'grey'):
                subtracted_nodes +=1
            self.attrs[nodes]['color'] = player
            colored_nodes+=1
        nx.set_node_attributes(self.graph,self.attrs)
        return (colored_nodes,subtracted_nodes)
        
    def printTable(self):
        """
        print 2D table
        """
        adjacency_matrix = []
        for node in self.graph.nodes():
            row = []
            row2 = []
            for neighbor in range(self.nodeNum):
                if(neighbor in self.graph.neighbors(node)):
                    row.append(1)
                else:
                    row.append(0)
            print(row)
            adjacency_matrix.append(row)
        
    def printGraph(self):
        """
        print Graph
        """
        plt.clf()
        labels = nx.get_node_attributes(self.graph,'number')
        colors = nx.get_node_attributes(self.graph,'color')
        nx.draw(self.graph,self.pos,node_color = colors.values(),with_lables=True,node_size = 250)
        nx.draw_networkx_labels(self.graph,self.pos,labels,font_size=8)
        plt.axis('off')
        plt.show()
        #plt.draw()
        
    def printGraph_node_only(self):
        """
        print Graph
        """
        plt.clf()
        labels = nx.get_node_attributes(self.graph,'number')
        colors = nx.get_node_attributes(self.graph,'color')
        print colors
        nx.draw_networkx_nodes(self.graph,self.pos,node_color = colors.values(),with_lables=True,node_size = 250)
        nx.draw_networkx_labels(self.graph,self.pos,labels,font_size=8)
        plt.axis('off')
        plt.pause(0.1)
        #plt.pause(0.001)
    def get_graph(self):
        return self.graph
if __name__=="__main__":
    
    n=50 # 50 nodes
    p=0.2 # prob
    G = Graph(n,p)
    print G.mark('red',1)
    print G.mark('blue',0)
    G.printGraph_node_only()
