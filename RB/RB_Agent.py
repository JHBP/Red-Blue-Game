#Agent Class
import networkx as nx
import sys
import matplotlib.pyplot as plt
import RB_Graph as G
import random
import copy

"""
" This is the file one needs to modify.
" One will be able to write there own algorithm under costom_algorithem.
" Feel free to make multiple costume Algorithm.
" Parameter for the algorithem are graph and player.
" Graph is RB_Graph format and player is in string.
" Player will be either "red" or "blue"
" Return type has to be node of graph.
" If there are multiple Algorithms that has been added, 
" run" function under "computer" class must be modified accordingly.
"""

"""
Random algorithm that makes a move randomly
"""
def RandomAlgorithm(g, player):
    return str(random.choice(g.getValidMoves()))
"""
Simple Greedy Algorithm that looks for the node with the most amount of neighboring nodes.
Autor: William Hsu
"""
def GreedyAlgorithm(g, player):
    valid_moves = g.getValidMoves()
    chosen_moves = []
    max_degree = -1
    for node in valid_moves:
        degree = 0
        for neighbors in g.graph.neighbors(node):
            degree += 1
        if max_degree < degree:
            chosen_moves = []
            chosen_moves.append(node)
            max_degree = degree
        elif max_degree == degree:
            chosen_moves.append(node)
    return str(random.choice(chosen_moves))

"""
Greedy Algorithm that considers the amount of nodes gained and the amount of nodes stolen from the opponent
Autor: William Hsu
"""
def GreedyAlgorithm2(g, player):
    valid_moves = g.getValidMoves()
    chosen_moves = []
    gamestate = nx.get_node_attributes(g.graph, 'color')
    max_degree = -1
    for node in valid_moves:
        degree = 0
        for neighbors in g.graph.neighbors(node):
            if player == 'red':
                if gamestate.get(neighbors) == 'grey':
                    degree += 1
                if gamestate.get(neighbors) == 'blue':
                    degree += 2
            elif player == 'blue':
                if gamestate.get(neighbors) == 'grey':
                    degree += 1
                if gamestate.get(neighbors) == 'red':
                    degree += 2
        if max_degree < degree:
            chosen_moves = []
            chosen_moves.append(node)
            max_degree = degree
        elif max_degree == degree:
            chosen_moves.append(node)
    return str(random.choice(chosen_moves))
"""
Minimax algorithm
Autor: William Hsu
"""

def MinimaxAlgorithm(g, player):
    m = Minimax(2)
    return str(m.getAction(g,player))

class Minimax():
    def __init__(self, depth):
        self.index = 0
        self.player = None
        self.enemy = None
        self.neighbors = None
        self.depth = int(depth)

    def getAction(self, g, player):
        current_depth = 0
        current_agent = 0
        alpha = -float("inf")
        beta = float("inf")
        value = -float('inf')
        self.player = player
        if player == 'red':
            self.enemy = 'blue'
        else:
            self.enemy = 'red'
        gamestate = nx.get_node_attributes(g.graph, 'color')
        valid_moves = set(g.getValidMoves())

        neighbors = []
        for node in range(g.nodeNum):
            adj = []
            for neighbor in g.graph.neighbors(node):
                adj.append(neighbor)
            neighbors.append(adj)
        self.neighbors = neighbors
        chosen_moves = []
        gameinfo = [gamestate, valid_moves, current_agent]
        for move in valid_moves:
            #print(str(move))
            new_value = self.value(self.generateSuccessor(move,gameinfo), current_agent + 1, current_depth, alpha, beta)
            #print(self.player + " : " + str(move) + " move and value " + str(new_value))
            if value < new_value:
                chosen_moves = []
                chosen_moves.append(move)
                value = new_value
            elif value == new_value:
                chosen_moves.append(move)
            if value > alpha:
                alpha = value
            if value >= beta:
                return eval
        return random.choice(chosen_moves)


    def value(self, gameinfo, current_agent, current_depth, alpha, beta ):
        if current_agent > 1:
            current_depth += 1
            current_agent = 0
        if current_depth >= self.depth or len(gameinfo[1]) == 0:
            return self.evaluate(gameinfo[0])

        if current_agent == 0:
            return self.max_value(gameinfo, current_agent, current_depth, alpha, beta)
        else:
            return self.min_value(gameinfo, current_agent, current_depth, alpha ,beta)

    def max_value(self, gameinfo,current_agent, current_depth, alpha, beta):
        if current_depth >= self.depth or len(gameinfo[1]) == 0:
            return self.evaluate(gameinfo[0])
        value = -float("inf")
        valid_moves = gameinfo[1]
        for move in valid_moves:
            new_value = self.value(self.generateSuccessor(move,gameinfo), current_agent + 1, current_depth, alpha, beta)
            if value < new_value:
                value = new_value
            if value > alpha:
                alpha = value
            if value > beta:
                return value
        return value

    def min_value(self, gameinfo, current_agent, current_depth, alpha, beta):
        if current_depth >= self.depth or len(gameinfo[1]) == 0:
            return self.evaluate(gameinfo[0])
        value = float("inf")
        valid_moves = gameinfo[1]
        for move in valid_moves:
            new_value = self.value(self.generateSuccessor(move,gameinfo), current_agent + 1, current_depth, alpha, beta)
            if value > new_value:
                value = new_value
            if value < beta:
                beta = value
            if value < alpha:
                return value
        return value

    def evaluate(self, gamestate):
        bluecount = 0
        redcount = 0
        for node in gamestate:
            if(gamestate.get(node) == 'red'):
                redcount += 1
            if(gamestate.get(node) == 'blue'):
                bluecount += 1
        if self.player == 'red':
            return redcount - bluecount
        else:
            return bluecount - redcount
    def generateSuccessor(self, move, gameinfo):
        gamestate = copy.deepcopy(gameinfo[0])
        valid_moves = set(gameinfo[1])
        agent = int(gameinfo[2])
        if (agent %2 == 0):
            player = self.player
        else:
            player = self.enemy
        gamestate[move] = player
        valid_moves.remove(move)
        for node in self.neighbors[move]:
            if (gamestate[node] == 'grey'):
                valid_moves.remove(node)
            gamestate[node] = player
        return [gamestate, valid_moves, agent+1]
  


def CostomAlgorithm(g,player):
    """
    colors are dictionary of dictionary.
    Key is a node number and value is a color of the node.
    You can access your color by self.getColor()
    return string of integer by using str() function
    check given algo (choose_random,greedy) for a references..
    """
    colors = nx.get_node_attributes(g.get_graph(),'color')
    #Todo: Write your code here!
    return 


"-------------------------Agent types------------------------"
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
        self.algorithm = RandomAlgorithm
        self.makeSelection = False
    
    def getColor(self):
        return self.color
    
    def run(self,graph,color):
        #write which algo to run
        """
        change it to your algorithm you want to run
        """
        if self.makeSelection:
            return self.algorithm(graph,color)
        else:
            print "Choose algorithm to use:"
            print "1. Random selection"
            print "2. Greedy Algorithm (most neighboring nodes)"
            print "3. Greedy Algorithm2 (most score)"
            print "4. Minimax Algorithm (in development... )"
            print "5. Costom Algorithm"
            """
            YOU MAY NEED TO ADD MORE PRINT
            """
            #print "6. Costom Algorithm2"
            #print "7. Costom Algorithm3"
            #print "8. Costom Algorithm4"
            #...
            select = int(raw_input())
            if select == 1:
                self.algorithm = RandomAlgorithm
            elif select == 2 :
                self.algorithm = GreedyAlgorithm       
            elif select == 3 :
                self.algorithm = GreedyAlgorithm2
            elif select == 4 :
                self.algorithm = MinimaxAlgorithm
            elif select == 5 :
                self.algorithm = CostomAlgorithm 
            """
            YOU MAY NEED TO ADD MORE elif statement
            """            
            #elif select == 6 :
            #    self.algorithm = CostomAlgorithm2
            #elif select == 7 :
            #    self.algorithm = CostomAlgorithm3 
            #elif select == 8 :
            #    self.algorithm = CostomAlgorithm4 
            #elif select == 9 :
            #    self.algorithm = CostomAlgorithm5
            self.makeSelection = True
            return self.algorithm(graph,color)
        
if __name__=="__main__":
    graph = G.get_graph()
    choose_random(graph)