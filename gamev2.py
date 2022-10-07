import networkx as nx
import matplotlib.pyplot as plt
import random
from random import choice, sample

class Game:
    def __init__(self, agents):
        print("init")


class Teams:
    def __init__(self):
        Graphtype = nx.Graph()
        data = open('network-2.csv', "r")
        next(data, None)

        green_team = nx.parse_edgelist(data, delimiter=',', create_using=Graphtype, nodetype=int, data=(('weight', float),))
        g_num = green_team.number_of_nodes
        print(g_num)
