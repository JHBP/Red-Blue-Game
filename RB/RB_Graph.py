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
        self.graph = nx.erdos_renyi_graph(nodeNum, prob)
        self.pos = nx.spring_layout(self.graph)
        # set node attribute
        self.attrs = {}
        for num in range(self.nodeNum):
            self.attrs[num] = {'number': num, 'color': 'grey'}
        nx.set_node_attributes(self.graph, self.attrs)

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

    #Read a dictionary object from the json file to create graph
    def readGraph(self, graph_data):
        self.graph.clear()
        nodes = []
        edges = []
        num_red = 0
        num_blue = 0
        self.attrs = {}
        for x in range(len(graph_data["graph"])):
            nodes.append(x)
            self.attrs[x] = {'number': x, 'color': graph_data["colors"][x]}
            for adj in range(len(graph_data["graph"][x])):
                edges.append((x, graph_data["graph"][x][adj]))

        for node in self.attrs.values():
            node_color = ''
            color_num = node.get('color')
            if (color_num == 0):
                node_color = 'grey'
            if (color_num == 1):
                num_red += 1
                node_color = 'red'
            if (color_num == 2):
                num_blue += 1
                node_color = 'blue'
            node['color'] = node_color
        self.graph.add_nodes_from(nodes)
        self.graph.add_edges_from(edges)
        self.pos = nx.spring_layout(self.graph)
        nx.set_node_attributes(self.graph, self.attrs)
        return (num_red, num_blue)

    #Game details printed to a file at the end of the game
    def printGraphDetails(self, game, file):
        file.write(
            'If you want to play again using the same graph, use the contents of "game_graph.json" file as an input file\n\n')
        file.write("Game History: \n\n")
        file.write(
            "Total Turns: " + str(len(game.move_list[0]) + len(game.move_list[1])) + "  \t\tScore:\t(Red, Blue)\n\n")
        redmove = 0
        bluemove = 0
        for round in range(len(game.move_list[0]) + len(game.move_list[1])):
            if (round % 2 == 0):
                file.write(
                    "Round " + str(round / 2 + 1) + ':\t Red Chose  ' + str(
                        game.move_list[0][redmove]) + '    \t' + str(
                        game.score_list[round]) + '\n')
                redmove += 1
            else:
                file.write(
                    "       " + ' \t Blue Chose ' + str(game.move_list[1][bluemove]) + '    \t' + str(
                        game.score_list[round]) + '\n')
                bluemove += 1
        file.write('\n\nGame Results: \n\n')
        red_nodes = []
        blue_nodes = []
        grey_nodes = []
        for node in range(self.nodeNum):
            color = self.attrs[node].get('color')
            if (color == "grey"):
                grey_nodes.append(node)
            elif (color == "red"):
                red_nodes.append(node)
            else:
                blue_nodes.append(node)
        file.write("Red has " + str(game.point[0]) + " points \n")
        file.write("Blue has " + str(game.point[1]) + " points \n")
        file.write("Red nodes: " + str(red_nodes) + "\n")
        file.write("Blue nodes: " + str(blue_nodes) + "\n")
        file.write("Neutral nodes: " + str(grey_nodes))
        file.write('\n\n\nGame Graph: \n\nTotal number of nodes: ' + str(self.nodeNum) + '\n\n')
        for node in range(self.nodeNum):
            adj = []
            for neighbor in self.graph.neighbors(node):
                adj.append(neighbor)
            file.write("node: " + str(node) + " \tneighbors: " + str(adj) + "\n")
        file.close()

    #Print the graph json format
    def printGraphJson(self, game, status, file):
        file.write("{\n")
        file.write('\t"rounds": ' + str(game.rounds) + ",\n")
        file.write('\t"time": ' + str(game.time) + ",\n")
        file.write('\t"graph": [\n')
        first1 = True
        for node in range(self.nodeNum):
            if (first1):
                file.write('\t\t[')
                first1 = False
            else:
                file.write(',\n\t\t[')
            first = True
            for neighbor in self.graph.neighbors(node):
                if (first):
                    file.write(str(neighbor))
                    first = False
                else:
                    file.write(', ' + str(neighbor))
            file.write(']')
        file.write('\n\t],\n')
        file.write('\t"colors": [')
        first = True
        color_num = 0
        for node in range(self.nodeNum):
            if(status):
                color = self.attrs[node].get('color')
                if (color == "grey"):
                    color_num = 0
                elif (color == "red"):
                    color_num = 1
                else:
                    color_num = 2
                if(first):
                    file.write(str(color_num))
                    first = False
                else:
                    file.write(', ' + str(color_num))
            else:
                if (first):
                    file.write(str(0))
                    first = False
                else:
                    file.write(', ' + str(0))
        file.write(']\n}')
        file.close()

    def mark(self, player, node):
        """
        mark node that player has chosen.
        return tuple: number of nodes added and number of node subtracted
        """
        colored_nodes = 0
        subtracted_nodes = 0
        if (node not in self.graph.node):
            sys.stderr.write('node does not exist\n')
            return (0, 0)
        if self.attrs[node]['color'] == 'grey':
            self.attrs[node]['color'] = player
            colored_nodes += 1
        else:
            sys.stderr.write('node has been taken')
            return (0, 0)

        for nodes in self.graph.neighbors(node):
            if (self.attrs[nodes]['color'] == player):
                continue
            if (self.attrs[nodes]['color'] != 'grey'):
                subtracted_nodes += 1
            self.attrs[nodes]['color'] = player
            colored_nodes += 1
        nx.set_node_attributes(self.graph, self.attrs)
        return (colored_nodes, subtracted_nodes)

    def printGraph(self, show_edge, final):
        if(not final):
            plt.clf()
        labels = nx.get_node_attributes(self.graph, 'number')
        colors = nx.get_node_attributes(self.graph, 'color')
        for node in colors:
            if (colors[node] == 'red'):
                colors[node] = 'lightcoral'
            if (colors[node] == 'blue'):
                colors[node] = 'skyblue'
        if(show_edge):
            nx.draw(self.graph, self.pos, node_color=colors.values(), with_lables=True, node_size=250)
        else:
            nx.draw_networkx_nodes(self.graph, self.pos, node_color=colors.values(), with_lables=True, node_size=250)
        nx.draw_networkx_labels(self.graph, self.pos, labels, font_size=8)
        plt.axis('off')
        if(not final):
            plt.pause(0.1)
        else:
            plt.show()

    def get_graph(self):
        return self.graph


if __name__ == "__main__":
    n = 50  # 50 nodes
    p = 0.2  # prob
    G = Graph(n, p)
    print G.mark('red', 1)
    print G.mark('blue', 0)
    G.printGraph_node_only()