import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import random
def create_teams(uncertainty_interval):
    print("generating teams...")

    Graphtype = nx.Graph()

    data = open('network-2.csv', "r")
    next(data, None)
    data2 = open('node-attributes', "r")
    next(data2, None)
    # print(data2)
    # skip first line

    # CREATE GRAPHS FOR EACH TEAM
    greenTeam_graph = nx.parse_edgelist(data, delimiter=',', create_using=Graphtype, nodetype=int, data=(('weight', float),))
    redTeam_graph = nx.Graph()
    redTeam_graph.add_node(26)
    blueTeam_graph = nx.Graph()
    blueTeam_graph.add_node(27)
    greyTeam_graph = nx.Graph()
    greyTeam_graph.add_nodes_from([28, 29, 30, 31, 32, 33, 34, 35, 36, 37])
    nx.set_node_attributes(greyTeam_graph, {"grey"}, name="team")

    for node in greyTeam_graph.nodes():
        if node == 29 or node == 30 or node == 32 or node == 34 or node == 36:
            nx.set_node_attributes(greyTeam_graph, {node: "good"}, name="allegiance")
        elif node == 28 or node == 31 or node == 33 or node == 35 or node == 37:
            nx.set_node_attributes(greyTeam_graph, {node: "bad"}, name="allegiance")

    for node in greenTeam_graph.nodes():
        random_opinion = random.choice([0, 1])
        random_interval = round(random.uniform(uncertainty_interval.left, uncertainty_interval.right), 1)

        nx.set_node_attributes(greenTeam_graph, {node: random_opinion}, name="opinion")
        nx.set_node_attributes(greenTeam_graph, {node: random_interval}, name="uncertainty")
        nx.set_node_attributes(greenTeam_graph, {node: "no vote"}, name="following")

    # SET ATTRIBUTES TO EACH NODE
    nx.set_node_attributes(greenTeam_graph, "red", name="following")
    # nx.set_node_attributes(greenTeam_graph, "none", name="following")
    nx.set_node_attributes(greenTeam_graph, "green", name="team")
    nx.set_node_attributes(redTeam_graph, "red", name="team")
    nx.set_node_attributes(greyTeam_graph, "grey", name="team")
    nx.set_node_attributes(blueTeam_graph, "blue", name="team")

    high_uncertainty = round(random.uniform(0.5, 1.0), 1)
    nx.set_node_attributes(redTeam_graph, high_uncertainty, name="uncertainty")

    # COMBINE ALL TEAMS INTO ONE GRAPH
    temp = nx.compose(redTeam_graph, blueTeam_graph)
    temp2 = nx.compose(temp, greyTeam_graph)
    game_network = nx.compose(greenTeam_graph, temp2)

    return game_network, greenTeam_graph, redTeam_graph, blueTeam_graph, greyTeam_graph, uncertainty_interval

def choose_interval():
    while True:
        try:
            print("Default uncertainty interval is (-1, 1)")
            player_interval_left = float(input('Input a left uncertainty interval for the game: '))
            player_interval_right = float(input('Input a right uncertainty interval for the game: '))
        except ValueError:
            print("Invalid value!")
            print("Please enter a valid float number..")
        if player_interval_left > player_interval_right and player_interval_left == player_interval_right:
            print("Invalid input!")
        else:
            break
    player_interval = pd.Interval(player_interval_left, player_interval_right)
    print("chosen uncertainty interval: ", player_interval)
    return player_interval

