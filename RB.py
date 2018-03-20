"""
<Red and Blue game>
Author: Jihoo Brian Park
Class: RB Class (main)
Discription: This class keeps points,time, turn, and determins winner of the game.
color of the player will be determined randomly.
starting player is always red.
"""
#TODO
"""
javascript to networkx - later.
argument to set which algo to use
need to thread timeout function
Question: if times up, is it autometic loss?
"""
import RB_Graph as G
import RB_Agent as Agent
import sys
import time as t
import random
import argparse

"""
Make coin flip optional
Setting costomized graph. maybe use json format to read?
Documentation(README)
server communication: 
1. server will only send graph at the beginning.
2. move will be updated on the server and client machine.

"""
class RBGame(object):
    def __init__(self,n,r,t):
        self.G = G.Graph(n,0.1)
        self.gui = False
        self.node = n
        self.prob = 0.1
        self.time = t
        self.rounds = r
        self.current_round = 1
        self.point = [0,0]#red,blue point
        self.turn ='red'
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
        print "It is round: "+str(self.current_round)+"and is " +self.turn+"'s turn."
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
        if self.turn == "red":
            if self.player1.getColor() == "red":
                return self.player1
            else:
                return self.player2
        else:
            if self.player1.getColor() == "blue":
                return self.player1
            else:
                return self.player2
    def start_game(self):
        if self.gameMode == 0:
            print "Starting computer vs computer"
            self.cvc()
        elif self.gameMode == 1:
            print "Starting human vs computer"
            self.pvc()
        else:
            print "Starting human vs human"
            self.pvp()
            
    def make_play(self,player):
        print "It is "+self.turn+"'s turn."
        print "Select a node or type \"-1\" to skip yout turn"
        counter = t.time()
        print "Time count starts now:"
        selected_node = 'node'
        while True:
            while selected_node.isdigit() == False:
                if (self.time-(t.time()-counter))<0:
                    print "Times up. "+ self.turn+ " lost"
                    return False
                selected_node = player.run(self.G,self.myColor)
                if selected_node!= 'node':
                    print "Not a numeric or skip. "+str(self.time-(t.time()-counter))+" seconds left!"
                if selected_node == "-1":
                    print self.turn+" made a play."
                    print self.turn+ " skipped turn."
                    return True
            result = self.G.mark(self.turn,int(selected_node))
            if result ==(0,0):
                print "\nCannot select: "+str(int(selected_node))+". "
                print str(self.time-(t.time()-counter))+"seconds left!"
                print "Select a node or type \"-1\" to skip yout turn"
                selected_node = 'node'
            else:
                print self.turn+" made a play."
                print self.turn+ " gained "+ str(result[0]) + " and took "+str(result[1])+" from the apponent."
                if self.turn == "red":
                    self.update_point(result[0],-result[1])
                else:
                    self.update_point(-result[1],result[0])
                return True
                

            
    def pvp(self): 
        print "<Starting game>"
        while (self.current_round <= self.rounds):
            print "\n\nRound: "+ str(self.current_round)
            if self.make_play(self.whosTurn()):
                self.current_round+=1
                print "scores are red: "+ str(self.point[0])+" and blue: "+ str(self.point[1])
                if self.turn == "red":
                    self.turn = "blue"
                else:
                    self.turn = "red"
                if self.gui:
                    self.G.printGraph_node_only()
            else:
                print self.turn+ " lost"
                self.G.printGraph()
                return False
        print "RESULT  of the game:"
        print "                    Red: "+ str(self.point[0])
        print "                    Blue: "+ str(self.point[1])
        if self.point[0]>self.point[1]:
            print "Red won!"
        elif self.point[0]<self.point[1]:
            print "Blue won!"
        else:
            print "It is tie game."
        self.G.printGraph()
            
    def pvc(self):
        print "<Starting game>"
        while (self.current_round <= self.rounds):
            print "\n\nRound: "+ str(self.current_round)
            if self.make_play(self.whosTurn()):
                self.current_round+=1
                print "scores are red: "+ str(self.point[0])+" and blue: "+ str(self.point[1])
                if self.turn == "red":
                    self.turn = "blue"
                else:
                    self.turn = "red"
                if self.gui:
                    self.G.printGraph_node_only()
            else:
                print self.turn+ " lost"
                self.G.printGraph()
                return False                
        print "RESULT  of the game:"
        print "                    Red: "+ str(self.point[0])
        print "                    Blue: "+ str(self.point[1])
        if self.point[0]>self.point[1]:
            print "Red won!"
        elif self.point[0]<self.point[1]:
            print "Blue won!"
        else:
            print "It is tie game."
        self.G.printGraph()
        
    def cvc(self): 
        print "<Starting game>"
        while (self.current_round <= self.rounds):
            print "\n\nRound: "+ str(self.current_round)
            if self.make_play(self.whosTurn()):
                self.current_round+=1
                print "scores are red: "+ str(self.point[0])+" and blue: "+ str(self.point[1])
                if self.turn == "red":
                    self.turn = "blue"
                else:
                    self.turn = "red"
                if self.gui:
                    self.G.printGraph_node_only()
            else:
                print self.turn+ " lost"
                
                self.G.printGraph()
                return False
        print "RESULT  of the game:"
        print "                    Red: "+ str(self.point[0])
        print "                    Blue: "+ str(self.point[1])
        if self.point[0]>self.point[1]:
            print "Red won!"
        elif self.point[0]<self.point[1]:
            print "Blue won!"
        else:
            print "It is tie game."            
        self.G.printGraph()
if __name__=="__main__":  
    #parsing the arguments
    parser = argparse.ArgumentParser(description='Setting Red and Blue game.')
    parser.add_argument('-g',type=bool,
                        help='Show GUI  (default: False)')    
    parser.add_argument('-n',type=int,
                       help='set node number (default: 100 nodes)')
    parser.add_argument('-r',type=int, 
                        help='set round number (default: 10 round)')
    parser.add_argument('-t',type=int, 
                        help='set time limit (default: 20 second)') 
    parser.add_argument('-p',type=int, 
                        help='set number of human player(s). Max 2. Default: 0(computer vs computer)')     
    args = parser.parse_args()
    
    game = RBGame(100,10,20) #node number, round, time
    #chose who start first
    game.rand_start()
    if args.g:
        game.setGUI(args.g)    
    if args.n:
        game.setNode(args.n)
    if args.r:
        game.setRound(args.r)
    if args.t:
        game.setTime(args.t)
    if args.p:
        game.setPlayer(args.p)
        
    #game start
    game.start_game()
    
    
