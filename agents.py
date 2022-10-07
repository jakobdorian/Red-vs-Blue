import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import random
def create_agents():
    print("creating agents...")

    # df = pd.read_csv('network-2.csv')
    Graphtype = nx.Graph()
    # g = nx.from_pandas_edgelist(df, edge_attr='weight', create_using=Graphtype)

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
    # greyTeam_good_graph = nx.Graph()
    # greyTeam_bad_graph = nx.Graph()

    greyTeam_graph = nx.Graph()
    # greyTeam_good_graph.add_nodes_from([29, 30, 32, 34, 36])
    # greyTeam_bad_graph.add_nodes_from([28, 31, 33, 35, 37])
    greyTeam_graph.add_nodes_from([28, 29, 30, 31, 32, 33, 34, 35, 36, 37])
    nx.set_node_attributes(greyTeam_graph, {"grey"}, name="team")

    for node in greyTeam_graph.nodes():
        if node == 29 or node == 30 or node == 32 or node == 34 or node == 36:
            # print("good")
            nx.set_node_attributes(greyTeam_graph, {node: "good"}, name="allegiance")
        elif node == 28 or node == 31 or node == 33 or node == 35 or node == 37:
            # print("bad")
            nx.set_node_attributes(greyTeam_graph, {node: "bad"}, name="allegiance")
    # set the random opinions and uncertainties of green agents
    for node in greenTeam_graph.nodes():
        random_opinion = random.choice([0, 1])
        random_interval = round(random.uniform(-1.0, 1.0), 1)
        nx.set_node_attributes(greenTeam_graph, {node: random_opinion}, name="opinion")
        nx.set_node_attributes(greenTeam_graph, {node: random_interval}, name="uncertainty")


    # SET ATTRIBUTES TO EACH NODE
    nx.set_node_attributes(greenTeam_graph, {"green"}, name="team")
    # nx.set_node_attributes(greenTeam_graph, {"default opinion"}, name="opinion")
    # nx.set_node_attributes(greenTeam_graph, {"followed"}, name="red-followers")
    # nx.set_node_attributes(greenTeam_graph, {"followed"}, name="blue-followers")
    nx.set_node_attributes(greenTeam_graph, "red", name="following")
    # nx.set_node_attributes(greenTeam_graph, {-0.5, 0.5}, name="certainty")

    nx.set_node_attributes(redTeam_graph, "red", name="team")

    high_uncertainty = round(random.uniform(0.5, 1.0), 1)
    nx.set_node_attributes(redTeam_graph, high_uncertainty, name="uncertainty")
    nx.set_node_attributes(blueTeam_graph, "blue", name="team")
    # nx.set_node_attributes(greyTeam_graph, {"grey"}, name="team")
    # nx.set_node_attributes(greyTeam_good_graph, {"grey-good"}, name="team")
    # nx.set_node_attributes(greyTeam_bad_graph, {"grey-bad"}, name="team")

    # COMBINE ALL TEAMS INTO ONE GRAPH
    temp = nx.compose(redTeam_graph, blueTeam_graph)
    temp2 = nx.compose(temp, greyTeam_graph)
    game_network = nx.compose(greenTeam_graph, temp2)

    # print(game_network.nodes(data=True))

    # g_list = nx.to_dict_of_lists(game_network)
    #
    # print(g_list)

    # for node in greyTeam_graph.nodes():
    #     if greyTeam_graph.nodes[node]["allegiance"] == "good":
    #         print(greyTeam_graph.nodes[node])
    #     elif greyTeam_graph.nodes[node]["allegiance"] == "bad":
    #         print(greyTeam_graph.nodes[node])


    return game_network, greenTeam_graph, redTeam_graph, blueTeam_graph, greyTeam_graph





    # nx.draw(greenTeam_graph)
    # nx.draw(game_network)
    # plt.show()
