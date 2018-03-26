"""
<Red and Blue game>
Author: Jihoo Brian Park, William Hsu
Class: RB Class (main)
Description: This class keeps points, time, turn, and determines the winner of the game.
color of the player will be determined randomly.
starting player is always red.
"""
#TODO
"""
javascript to networkx - later.
argument to set which algo to use
need to thread timeout function
"""
import RB_Graph as G
import RB_Agent as Agent
import sys
import time as t
import json
import random
import argparse

"""
server communication: 
1. server will only send graph at the beginning.
2. move will be updated on the server and client machine.
"""
class RBGame(object):
    def __init__(self,n,r,t):
        self.G = G.Graph(n,0.3)
        self.gui = True
        self.node = n
        self.time = t
        self.rounds = r
        self.move_list = [[],[]]
        self.score_list = []
        self.current_turn = 1
        self.point = [0,0]#red,blue point
        self.turn_player ='red'
        self.assigned =[]#"red,blue" or "blue,red"
        self.myColor = ''# this will be fetched from the server
        self.gameMode = 0 # 1 == cvc, 2 == pvc, 3 == pvp
        self.player1 = Agent.computer("red")
        self.player2 = Agent.computer("blue")
    def read_in_graph(self,filename):
        self.G = G.Graph.readGraph()
    def setPlayer(self,gameMode):
        if gameMode == 1:
            self.gameMode = 1
            self.player1 = Agent.human(self.assigned[0])
            self.player2 = Agent.computer(self.assigned[1])
        elif gameMode ==2:
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

    def print_game_info(self):
        print "This game is ",
        if self.gameMode ==0:
            print "computer vs computer game mode."
        elif self.gameMode == 1:
            print "human vs computer game mode."
        else:
            print "human vs human game mode."
        print "It is round: "+str(self.current_turn)+"and is " +self.turn_player+"'s turn."
        print "Current result  of the game:"
        print "                    Red: "+ str(self.point[0])
        print "                    Blue: "+ str(self.point[1])

    def update_point(self,r,b):
        self.point[0]+=r
        self.point[1]+=b

    def rand_start(self):

        #randomely assign red or blue to players
        if random.choice([True,False]):
            self.assigned = ["red","blue"]
        else:
            self.assigned = ["blue","red"]
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
        print 'Select a node or type \"-1\" to skip your turn. Type "print" to retrieve current status of graph'
        counter = t.time()
        print "Time count starts now:"
        selected_node = 'node'
        while True:
            while selected_node.isdigit() == False:
                if (self.time-(t.time()-counter))<0:
                    print "Times up. "+ self.turn_player + " lost"
                    return False
                #selected_node = player.run(self.G,self.myColor)
                selected_node = player.run(self.G,player.color)
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
                    print "Invalid move, please input a node number. "+str(self.time-(t.time()-counter))+" seconds left!"
            result = self.G.mark(self.turn_player,int(selected_node))
            if result ==(0,0):
                print "\nCannot select: "+str(int(selected_node))+". "
                print str(self.time-(t.time()-counter))+"seconds left!"
                print "Select a node or type \"-1\" to skip yout turn"
                selected_node = 'node'
            else:
                self.move_list[(self.current_turn + 1) % 2].append(selected_node)
                print self.turn_player+" made a play and chose " +str(selected_node)
                print self.turn_player+ " gained "+ str(result[0]) + " and took "+str(result[1])+" from the apponent."
                if self.turn_player == "red":
                    self.update_point(result[0],-result[1])
                else:
                    self.update_point(-result[1],result[0])
                self.score_list.append((self.point[0],self.point[1]))
                return True



    def start_game(self):
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
                print "scores are red: "+ str(self.point[0])+" and blue: "+ str(self.point[1])
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

if __name__=="__main__":
    #parsing the arguments
    parser = argparse.ArgumentParser(description='Setting Red and Blue game.')
    parser.add_argument('-g',type=str,
                        help='Show GUI  (default: True)')
    parser.add_argument('-n',type=int,
                       help='set node number (default: 20 nodes)')
    parser.add_argument('-r',type=int,
                        help='set round limit (default: 10 rounds)')
    parser.add_argument('-t',type=int,
                        help='set time limit (default: 30 second)')
    parser.add_argument('-p',type=int,
                        help='set number of human player(s). Max 2. Default: 0(computer vs computer)')
    parser.add_argument('-f', type=str,
                        help='Input a graph as a json file')
    args = parser.parse_args()


    if args.f:
        graph_data = json.load(open(args.f))
        game = RBGame(len(graph_data["graph"]),graph_data["rounds"], graph_data["time"])
        game.point[0],game.point[1] = game.G.readGraph(graph_data)
        game.rand_start()

    else:
        game = RBGame(50,10,30)
        game.rand_start()
        if args.n:
            game.setNode(args.n)
        if args.r:
            game.setRound(args.r)
        if args.t:
            game.setTime(args.t)

    if args.g:
        if(args.g == "False"):
            game.setGUI(False)
    if args.p:
        print(str(args.p))
        game.setPlayer(args.p)
    #game start
    game.start_game()