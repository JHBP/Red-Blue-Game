#Agent Class
import RB_Graph as G
import RB as RB
import random
import networkx as nx
import copy

#TODO:
"""
greedy algo
person vs person
infuse code to webdev
"""
import RB

"""
Random algorithm that makes a move randomly
"""
def RandomAlgorithm(g, player):
    return random.choice(g.getValidMoves())

"""
Simple Greedy Algorithm that looks for the node with the most amount of neighboring nodes.
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
    return random.choice(chosen_moves)

"""
Greedy Algorithm that considers the amount of nodes gained and the amount of nodes stolen from the opponent
"""
def SmartGreedyAlgorithm(g, player):
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
    return random.choice(chosen_moves)


"""
Minimax algorithm
"""
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
            new_value = self.value(self.generateSuccessor(move,gameinfo), current_agent + 1, current_depth)
            #print(str(move) + " move and value " + str(new_value))
            if value < new_value:
                chosen_moves = []
                chosen_moves.append(move)
                value = new_value
            elif value == new_value:
                chosen_moves.append(move)
        return random.choice(chosen_moves)


    def value(self, gameinfo, current_agent, current_depth):
        if current_agent > 1:
            current_depth += 1
            current_agent = 0
        if current_depth >= self.depth or len(gameinfo[1]) == 0:
            return self.evaluate(gameinfo[0])

        if current_agent == 0:
            return self.max_value(gameinfo, current_agent, current_depth)
        else:
            return self.min_value(gameinfo, current_agent, current_depth)

    def max_value(self, gameinfo,current_agent, current_depth):
        if current_depth >= self.depth or len(gameinfo[1]) == 0:
            return self.evaluate(gameinfo[0])
        value = -float("inf")
        valid_moves = gameinfo[1]
        for move in valid_moves:
            new_value = self.value(self.generateSuccessor(move,gameinfo), current_agent + 1, current_depth)
            if value < new_value:
                value = new_value
        return value

    def min_value(self, gameinfo, current_agent, current_depth):
        if current_depth >= self.depth or len(gameinfo[1]) == 0:
            return self.evaluate(gameinfo[0])
        value = float("inf")
        valid_moves = gameinfo[1]
        for move in valid_moves:
            new_value = self.value(self.generateSuccessor(move,gameinfo), current_agent + 1, current_depth)
            if value > new_value:
                value = new_value
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
        #print("orig")
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

if __name__ == "__main__":
    g = G.Graph(5,0.3)
    print(RandomAlgorithm(g,'red'))
    print(SmartGreedyAlgorithm(g,'red'))
    print(GreedyAlgorithm(g,'red'))
    m = Minimax
    print(m.getAction(Minimax(2),g,'red'))
    g.printGraph()

