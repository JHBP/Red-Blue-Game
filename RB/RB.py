"""
<Red and Blue game>
Author: Jihoo Brian Park, William Hsu
Class: RB Class (main)
Description: This class keeps points, time, turn, and determines the winner of the game.
color of the player will be determined randomly.
starting player is always red.
"""

import RB_Graph as G
import RB_Agent as Agent
import Server as S
import time as t
import json
import random
import argparse


class RBGame(object):
    def __init__(self,n,r,t,p):
        self.G = G.Graph(n,p)
        self.gui = True
        self.node = n
        self.time = t
        self.rounds = r
        self.prob = p
        self.move_list = [[],[]] #list of red moves, list of blue moves
        self.score_list = [] #list of scores after each turn
        self.current_turn = 1
        self.point = [0,0]#red,blue point
        self.turn_player ='red'
        self.assigned =[]#"red,blue" or "blue,red"
        self.gameMode = 0 # 1 == cvc, 2 == pvc, 3 == pvp
        self.player1 = None
        self.player2 = None

        #For server interaction:
        self.player = None # assigns your color depending on server decision
        self.enemy = None # assigns enemy color depending on server decision
        self.player_id = None # personal id for server to identify your moves
        self.server = None # server address
        self.game_id = None # id of the game you are participating in on the server

    def setPlayer(self,gameMode):
        if gameMode == 1:
            self.gameMode = 1
            self.player1 = Agent.human(self.assigned[0])
            self.player2 = Agent.computer(self.assigned[1])
        elif gameMode == 2:
            self.gameMode = 2
            self.player1 = Agent.human(self.assigned[0])
            self.player2 = Agent.human(self.assigned[1])
        else:
            self.gameMode = 0
            self.player1 = Agent.computer(self.assigned[0])
            self.player2 = Agent.computer(self.assigned[1])
        print "Player 1 is "+self.assigned[0]+" and Player 2 is "+self.assigned[1]

    def setNode(self,n):
        self.G = G.Graph(n,0.1)
    def setGUI(self,OnOff):
        self.gui = OnOff
    def setRound(self,r):
        self.rounds = r

    def setTime(self,t):
        self.time = t

    def update_point(self,r,b):
        self.point[0]+=r
        self.point[1]+=b

    def rand_start(self):
        #randomely assign red or blue to players
        if random.choice([True,False]):
            self.assigned = ["red","blue"]
        else:
            self.assigned = ["blue","red"]
        self.player1 = Agent.computer(self.assigned[0])
        self.player2 = Agent.computer(self.assigned[1])

    def whosTurn(self):
        if self.turn_player == "red":
            if self.player1.getColor() == "red":
                return self.player1
            else:
                return self.player2
        else:
            if self.player1.getColor() == "blue":
                return self.player1
            else:
                return self.player2


    def make_play(self,player):
        print "It is "+self.turn_player+"'s turn."
        if(player.name == "human"):
            print 'Select a node or type \"-1\" to skip your turn. Type "print" to retrieve current status of graph'

        selected_node = 'node'
        while True:
            while selected_node.isdigit() == False:
                selected_node = player.run(self.G,player.color,(self.current_turn+1)/2)

                if selected_node == 'print':
                    output = open('graphStatus.json', 'w')
                    self.G.printGraphJson(self, True, output)
                    print 'Graph status printed to "graph_status.json", now choose your move.'
                    output.close()
                elif selected_node == "-1":
                    print self.turn_player + "chose to skip their turn."
                    self.move_list[(self.current_turn+1)%2].append(selected_node)
                    self.score_list.append((self.point[0],self.point[1]))
                    return True
                elif selected_node.isdigit() == False:
                    print "Invalid move, please input a node number. "
            result = self.G.mark(self.turn_player,int(selected_node))
            ##GET DIFFERENCE
            if result ==(0,0):
                print "\nCannot select: "+str(int(selected_node))+". "
                print "Select a node or type \"-1\" to skip yout turn"
                selected_node = 'node'
            else:
                self.move_list[(self.current_turn + 1) % 2].append(selected_node)
                if (player.name == "human"):
                    print self.turn_player+" made a play and chose " +str(selected_node)
                else:
                    print player.name + " made a play and chose " + str(selected_node)
                print self.turn_player+ " gained "+ str(result[0]) + " and took "+str(result[1])+" from the apponent."
                if self.turn_player == "red":
                    self.update_point(result[0],-result[1])
                else:
                    self.update_point(-result[1],result[0])
                self.score_list.append((self.point[0],self.point[1]))
                return True



    def start_game(self):
        """
        Add another gamemode for playing with the server.
        """
        if self.gameMode == 0:
            print "Starting computer vs computer"
        elif self.gameMode == 1:
            print "Starting human vs computer"
        else:
            print "Starting human vs human"
        if self.gui:
            self.G.printGraph(False, False)
        while ((self.current_turn+1)/2 <= self.rounds and len(self.G.getValidMoves()) != 0):
            print "\n\nRound: "+ str((self.current_turn+1)/2)
            if self.make_play(self.whosTurn()):
                self.current_turn+=1
                print "scores are [ red: "+ str(self.point[0])+" , blue: "+ str(self.point[1]) + " ]"
                if self.turn_player == "red":
                    self.turn_player = "blue"
                else:
                    self.turn_player = "red"
                if self.gui:
                    self.G.printGraph(False, False)
            else:
                print self.turn_player + " lost"
                #self.G.printGraph()
                return False
        print "RESULTS of the game:"
        print "                    Red: "+ str(self.point[0])
        print "                    Blue: "+ str(self.point[1])
        if self.point[0]>self.point[1]:
            print "Red won!"
        elif self.point[0]<self.point[1]:
            print "Blue won!"
        else:
            print "It is tie game."
        final_output = open('graph_details.txt', 'w')
        final_json = open('game_graph.json','w')
        self.G.printGraphDetails(self, final_output)
        self.G.printGraphJson(self, False, final_json)
        final_output.close()
        print '\n\nLook at "graph_details.txt" for more information on this game'
        self.G.printGraph(True, True)


    def make_play_server(self):
        first = True
        while (len(self.G.getValidMoves()) > 0):
            response = S.requestMove(self.server, self.player_id, self.game_id)
            if (response == None):
                break
            data = json.loads(response[1])
            move = -2
            if "delta" in data:
                if (self.player == None):
                    first = False
                    self.player = Agent.computer("blue")
                    self.enemy = 'red'
                for node in data['delta']:
                    adj = [node]
                    for neighbor in self.G.graph.neighbors(node):
                        if not self.G.attrs[neighbor].get('color') == self.enemy:
                            adj.append(neighbor)
                    if (sorted(data['delta']) == sorted(adj)):
                        move = node
                self.G.mark(self.enemy, int(move))
                self.G.printGraph(True, False)
            else:
                if (self.player == None):
                    self.player = Agent.computer("red")
                    self.enemy = 'blue'
                    move = -2
                else:
                    move = -1
            if (not len(self.G.getValidMoves()) > 0):
                break
            if (not first):
                print("Round: " + str(data['round']) + "  Opponent chose " + str(move) + ", it is your turn, input a valid node.")
            else:
                print("Round: " + str(data['round']) + "  It is your turn, input a valid node.")
            first = False
            selected_node = ""
            while not selected_node.isdigit() or (int(selected_node) not in self.G.getValidMoves()):
                selected_node = self.player.run(self.G, self.player.color, data['round'])
                if not selected_node.isdigit():
                    print("Invalid input, please select a node")
                elif int(selected_node) not in self.G.getValidMoves():
                    print("Invalid move, select an uncolored node")
            print("You chose node " + str(selected_node))
            self.G.mark(self.player.color, int(selected_node))
            response = S.submitMove(self.server, self.player_id, self.game_id, selected_node)
            if (len(self.G.getValidMoves()) > 0):
                print("Waiting for opponents response.\n")
            self.G.printGraph(True, False)
        print("game completed")

        self.G.printGraph(True, True)

    def start_game_server(self):
        print("Initializing game with the server.")
        command = None
        while command != quit:
            command = raw_input('> ').split()
            while len(command) == 0:
                command = raw_input('> ').split()
            if command[0] == '?':
                if len(command) == 1:
                    S.usage()
                else:
                    print 'Error: No arguments are allowed'
            if command[0] == 'config':
                if len(command) == 1:
                    S.config()
                else:
                    print 'Error: No arguments are allowed'
            elif command[0] == 'start':
                if len(command) == 1:
                    response, self.game_id = S.startGame(self.server, {'nodes': self.node, 'rounds': self.rounds,
                                                                       'time': self.time, 'prob': self.prob,
                                                                       'seed': None}, self.player_id)
                    data = json.loads(response[1])
                    data["static"]['colors'] = data['colors']
                    self.G.readGraph(data['static'])
                    self.G.printGraph(True, False)
                    break
                else:
                    print 'Error: No arguments are allowed'
            elif command[0] == 'join':
                if len(command) == 2:
                    self.game_id = command[1]
                    response = S.joinGame(self.server, {'game_id': command[1]}, self.player_id)
                    if(response == None):
                        continue
                    print("Joined the game, you will be notified when it is your turn.")
                    data = json.loads(response[1])
                    data["static"]['colors'] = data['colors']
                    self.G.readGraph(data['static'])
                    self.G.printGraph(True, False)
                    break
                else:
                    print 'Error: Need one argument (game id)'
        self.make_play_server()




if __name__=="__main__":
    #parsing the arguments
    parser = argparse.ArgumentParser(description='Setting Red and Blue game.')
    parser.add_argument('-g',action = 'store_true',
                        help='disable GUI')
    parser.add_argument('-n',type=int,
                       help='set node number (default: 20 nodes)')
    parser.add_argument('-r',type=int,
                        help='set round limit (default: 10 rounds)')
    parser.add_argument('-t',type=int,
                        help='set time limit (default: 30 second)')
    parser.add_argument('-p', type=float,
                        help='set the probability of an edge existing between two nodes (for graph generation). default: 0.2')
    parser.add_argument('-pl',type=int,
                        help='set number of human player(s). Max 2. Default: 0(computer vs computer)')
    parser.add_argument('-f', type=str,
                        help='input a graph as a json file, look at the sample file for proper format')
    parser.add_argument('-s', action='store_true',
                        help='connect and play with the server')
    args = parser.parse_args()

    node = 20
    round = 10
    time = 30
    prob = 0.2
    if args.n:
        node = args.n
    if args.r:
        round = args.r
    if args.t:
        time = args.t
    if args.p:
        prob = args.p
    if args.s:
        game = RBGame(node,round,time,prob)
        game.server, game.player_id = S.init()
        game.start_game_server()
        if args.g:
            game.setGUI(False)
    else:
        if args.f:
            graph_data = json.load(open(args.f))
            game = RBGame(len(graph_data["graph"]),graph_data["rounds"], graph_data["time"], prob)
            game.point[0],game.point[1] = game.G.readGraph(graph_data)
            game.rand_start()

        else:
            game = RBGame(node,round,time,prob)
            game.rand_start()
        if args.g:
            game.setGUI(False)
        if args.pl:
            game.setPlayer(args.pl)
        #game start
        game.start_game()