"""
<Red and Blue game>
Author: Jihoo Brian Park
Class: RB Class (main)
Discription: This class keeps points,time, turn, and determins winner of the game.
Starting player will be determined randomly.
"""
import RB_Graph as G
from RB_Agent import *
import sys
import matplotlib.pyplot as plt
import time as t
import random
import argparse
import json

class RBGame(object):
    def __init__(self,n,r,t):
        self.G = G.Graph(n,0.1)
        self.node = n
        self.prob = 0.1
        self.time = t
        self.rounds = r
        self.current_round = 1
        self.point = [0,0]#red,blue point
        self.turn =''

    def setNode(self,n):
        self.G = G.Graph(n,0.1)
        
    def setRound(self,r):
        self.rounds = r
        
    def setTime(self,t):
        self.time = t
        
    def print_game_info(self):
        print "It is "
    def update_point(self,r,b):
        self.point[0]+=r
        self.point[1]+=b
        
    def rand_start(self):
        if random.choice([True,False]):
            self.turn = 'red'
        else:
            self.turn = 'blue'
    
    def make_play(self):
        self.G.printGraph_node_only()
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
                if selected_node!= 'node':
                    print "Not a numeric or skip. "+str(self.time-(t.time()-counter))+" seconds left!"
                selected_node = raw_input()
                if selected_node == "-1":
                    print self.turn+" made play."
                    print self.turn+ " skipped turn."
                    return True
            result = self.G.mark(self.turn,int(selected_node))
            if result ==(0,0):
                print "\nCannot select: "+str(int(selected_node))+". "
                print str(self.time-(t.time()-counter))+"seconds left!"
                print "Select a node or type \"-1\" to skip yout turn"
                selected_node = 'node'
            else:
                print self.turn+" made play."
                print self.turn+ " gained "+ str(result[0]) + " and took "+str(result[1])+" from the apponent."
                if self.turn == "red":
                    self.update_point(result[0],-result[1])
                else:
                    self.update_point(-result[1],result[0])
                return True
                
    def start_game(self):
        print "<Starting game>"
        while (self.current_round <= self.rounds and len(self.G.getValidMoves()) != 0):
            print "\n\nRound: "+ str(self.current_round)
            if self.make_play():
                self.current_round+=1
                print "scores are red: "+ str(self.point[0])+" and blue: "+ str(self.point[1])
                if self.turn == "red":
                    self.turn = "blue"
                else:
                    self.turn = "red"
                #self.G.printGraph_node_only()
            else:
                print self.turn+ " lost"
                self.G.printGraph()
                return False

        print "RESULT of the game:"
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
    graph_data = json.load(open('graph.json'))
    time = graph_data["timeLimit"]
    numCount = graph_data["nodeCount"]
    roundCount = graph_data["roundCount"]
    game = RBGame(100,10,20) #node number, round, time
    game.point = game.G.readGraph(graph_data["nodes"])


    #parsing the arguments
    # parser = argparse.ArgumentParser(description='Setting Red and Blue game.')
    # parser.add_argument('-n',type=int,
    #                    help='set node number (default: 100 nodes)')
    # parser.add_argument('-r',type=int,
    #                     help='set round number (default: 10 round)')
    # parser.add_argument('-t',type=int,
    #                     help='set time limit (default: 20 second)')
    # args = parser.parse_args()
    # if args.n:
    #     game.setNode(args.n)
    # if args.r:
    #     game.setRound(args.r)
    # if args.t:
    #     game.setTime(args.t)
    #
    #
    #
    # #chose who start first
    game.rand_start()
    #game start
    game.start_game()
    
    
