#Agent Class
import networkx as nx
import sys
import matplotlib.pyplot as plt
import RB_Graph as G
#TODO:
"""
greedy algo
person vs person
infuse code to webdev
"""

class human(object):
    def __init__(self,color):
        self.color = color
    
    def getColor(self):
        return self.color
    
    def run(self,graph,color):
        return raw_input()
    
class computer(object):
    def __init__(self,color):
        self.color = color
    
    def getColor(self):
        return self.color
    
    def choose_random(self,graph,player):
        colors = nx.get_node_attributes(graph.get_graph(),'color')
        for i in range(len(colors)):
            if colors[i] == "grey":
                return str(i)
        return str(-1)
    
    def costom_algo(self,graph,player):
        """
        colors are dictionary of dictionary.
        Key is a node number and value is a color of the node.
        You can access your color by self.getColor()
        return string of integer by using str() function
        check given algo (choose_random,greedy) for a references..
        """
        colors = nx.get_node_attributes(graph.get_graph(),'color')
        #Todo Write your code here
        
        return 
    
    def run(self,graph,color):
        #write which algo to run
        """
        change it to your algorithm you want to run
        """
        return self.choose_random(graph,color)
    
if __name__=="__main__":
    graph = G.get_graph()
    choose_random(graph)