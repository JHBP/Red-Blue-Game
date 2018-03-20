"""
<Red and Blue game>
Author: Jihoo Brian Park
Class: Graph Class
Discription: This generates Erdos-Renyi graph.
Default color is grey. when nodes are marked by player, graph updates the node color.
"""
import networkx as nx
import sys
import numpy
import matplotlib.pyplot as plt
#TODO
"""
constant graph showing
2D table
"""
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
    def readGraph(self, graph_info):
        self.graph = nx.Graph()
        nodes = []
        edges = []
        num_red = 0
        num_blue = 0
        self.attrs = {}
        for x in range(len(graph_info)):
            id = int(graph_info[x]["id"])
            nodes.append(id)
            self.attrs[x] = {'number':id,'color':int(graph_info[x]['color'])}
            for adj in range(len(graph_info[x]["adj"])):
                edges.append((id,int(graph_info[x]["adj"][adj])))
                #print(graph_info[x]["adj"][0])
            #edges.append((x,graph_info[x]))
        for node in self.attrs.values():
            node_color = ''
            num_color = node.get('color')
            if(num_color == 0):
                node_color = 'grey'
            if(num_color == 1):
                num_red += 1
                node_color = 'red'
            elif(num_color == 2):
                num_blue += 1
                node_color = 'blue'
            node['color'] = node_color
        #print(nodes)
        #print(edges)
        #print(self.attrs)
        self.graph.add_nodes_from(nodes)
        self.graph.add_edges_from(edges)
        self.pos=nx.spring_layout(self.graph)
        nx.set_node_attributes(self.graph, self.attrs)
        return ([num_red, num_blue])
    
    def mark(self, player, node):
        """
        mark node that player has chosen.
        return tuple: number of nodes added and number of node subtracted
        """
        colored_nodes = 0
        subtracted_nodes = 0
        if(node not in self.graph.node):
            sys.stderr.write('node does not exist')
            return (0, 0)
        if self.attrs[node]['color'] == 'grey':
            self.attrs[node]['color'] = player
            colored_nodes+=1
        else:
            sys.stderr.write('node has been taken')
            return(0,0)
            
        for nodes in self.graph.neighbors(node):
            if(self.attrs[nodes]['color'] == player):
                continue
            if (self.attrs[nodes]['color'] != 'grey'):
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
    def get_graph(self):
        return self.graph
    
if __name__=="__main__":
    
    n=50 # 50 nodes
    p=0.2 # prob
    G = Graph(n,p)
    print G.mark('red',1)
    print G.mark('blue',0)
    G.printGraph_node_only()
