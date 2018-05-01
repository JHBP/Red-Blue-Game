# Agent Class
import networkx as nx
import sys
import matplotlib.pyplot as plt
import RB_Graph as G
import random
import copy

"""
" This is the file one needs to modify.
" One will be able to write there own algorithm under custom_algorithm.
" Feel free to make multiple custom algorithms.
" Parameters for the algorithm are graph and player.
" Graph is RB_Graph format and player is the string of the player color.
" Return type has to be the string of a node number
" If there are multiple algorithms that has been added, 
" 'run' function under 'computer' class must be modified accordingly.
"""

"""
Random algorithm that makes a move randomly
"""
def RandomAlgorithm(g, player, round):
    return str(random.choice(g.getValidMoves()))


"""
Simple Greedy Algorithm that looks for the node with the most amount of neighboring nodes.
"""
def GreedyNodesAlgorithm(g, player, round):
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
"""
def GreedyPointsAlgorithm(g, player, round):
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
                elif gamestate.get(neighbors) == 'blue':
                    degree += 2
            else:
                if gamestate.get(neighbors) == 'grey':
                    degree += 1
                elif gamestate.get(neighbors) == 'red':
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
"""
def MinimaxAlgorithm(g, player, round):
    m = Minimax(2)
    return str(m.getAction(g, player, round))


class Minimax():
    def __init__(self, depth):
        self.index = 0
        self.player = None
        self.enemy = None
        self.neighbors = None
        self.depth = int(depth)

    def getAction(self, g, player, round):
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
            # print(str(move))
            new_value = self.value(self.generateSuccessor(move, gameinfo), current_agent + 1, current_depth, alpha,
                                   beta)
            # print(self.player + " : " + str(move) + " move and value " + str(new_value))
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

    def value(self, gameinfo, current_agent, current_depth, alpha, beta):
        if current_agent > 1:
            current_depth += 1
            current_agent = 0
        if current_depth >= self.depth or len(gameinfo[1]) == 0:
            return self.evaluate(gameinfo[0])

        if current_agent == 0:
            return self.max_value(gameinfo, current_agent, current_depth, alpha, beta)
        else:
            return self.min_value(gameinfo, current_agent, current_depth, alpha, beta)

    def max_value(self, gameinfo, current_agent, current_depth, alpha, beta):
        if current_depth >= self.depth or len(gameinfo[1]) == 0:
            return self.evaluate(gameinfo[0])
        value = -float("inf")
        valid_moves = gameinfo[1]
        for move in valid_moves:
            new_value = self.value(self.generateSuccessor(move, gameinfo), current_agent + 1, current_depth, alpha,
                                   beta)
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
            new_value = self.value(self.generateSuccessor(move, gameinfo), current_agent + 1, current_depth, alpha,
                                   beta)
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
            if (gamestate.get(node) == 'red'):
                redcount += 1
            if (gamestate.get(node) == 'blue'):
                bluecount += 1
        if self.player == 'red':
            return redcount - bluecount
        else:
            return bluecount - redcount

    def generateSuccessor(self, move, gameinfo):
        gamestate = copy.deepcopy(gameinfo[0])
        valid_moves = set(gameinfo[1])
        agent = int(gameinfo[2])
        if (agent % 2 == 0):
            player = self.player
        else:
            player = self.enemy
        gamestate[move] = player
        valid_moves.remove(move)
        for node in self.neighbors[move]:
            if (gamestate[node] == 'grey'):
                valid_moves.remove(node)
            gamestate[node] = player
        return [gamestate, valid_moves, agent + 1]


def CustomAlgorithm(g, player, round):
    """
    colors is the dictionary of dictionary.
    Key is a node number and value is a color of the node.
    valid_moves contains the uncolored nodes of the graph.
    You can access your color from the 'player' parameter
    return string of an integer by using str() function
    check the given algorithms (random,greedy) for references..
    """
    colors = nx.get_node_attributes(g.get_graph(), 'color')
    valid_moves = g.getValidMoves()
    # Todo: Write your code here!
    return


"""
Agent types
"""


class human(object):
    def __init__(self, color):
        self.name = "Human"
        self.color = color

    def getColor(self):
        return self.color

    def run(self, graph, color):
        return raw_input()


class computer(object):
    def __init__(self, color):
        self.color = color
        self.name = None
        self.algorithm = None
        self.makeSelection = False

    def getColor(self):
        return self.color

    def run(self, graph, color, round):
        # Choose which algo to run
        if self.makeSelection:
            return self.algorithm(graph, color, round)
        else:
            print "Choose an algorithm to use:"
            print "1. Random selection"
            print "2. Greedy Nodes Algorithm"
            print "3. Greedy Points Algorithm"
            print "4. Minimax Algorithm"
            # print "5. Custom Algorithm"
            """
            YOU MAY NEED TO ADD MORE PRINT
            """
            # print "6. Custom Algorithm2"
            # print "7. Custom Algorithm3"
            # print "8. Custom Algorithm4"
            # ...
            valid_choice = False
            while (not valid_choice):
                valid_choice = True
                select = raw_input()
                if select.isdigit():
                    select = int(select)
                if select == 1:
                    self.algorithm = RandomAlgorithm
                    self.name = "Random Algorithm"
                elif select == 2:
                    self.algorithm = GreedyNodesAlgorithm
                    self.name = "Greedy Nodes Algorithm"
                elif select == 3:
                    self.algorithm = GreedyPointsAlgorithm
                    self.name = "Greedy Points Algorithm"
                elif select == 4:
                    self.algorithm = MinimaxAlgorithm
                    self.name = "Minimax Algorithm"
                ### Add more statements when you implement more algorithms
                # elif select == 5 :
                #     self.algorithm = CustomAlgorithm
                else:
                    valid_choice = False
                    print("Invalid choice of algorithm")
            self.makeSelection = True
            return self.algorithm(graph, color, round)


if __name__ == "__main__":
    graph = G.get_graph()