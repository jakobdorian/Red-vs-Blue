import networkx as nx
import matplotlib.pyplot as plt
import random
import pandas as pd
def start_game(network, green_team, red_team, blue_team, grey_good_team, grey_bad_team):
    print("game is starting...")
    # print(network.nodes(data=True))
    # print(green_team)
    # print(red_team)
    # print(blue_team)
    # print(grey_good_team)
    # print(grey_bad_team)
    redgreen_interaction(green_team, red_team)

    g_dict = nx.to_dict_of_dicts(network)


def redgreen_interaction(green_agent, red_agent):
    # combine red and green nodes into one graph
    current_interaction = nx.compose(green_agent, red_agent)
    # print(current_interaction.nodes(data=True))
    # nx.draw(current_interaction)
    # plt.show()
    for node in current_interaction.nodes():
        random_interval = random.choice([-1, 1])
        if random_interval == -1:
            nx.set_node_attributes(current_interaction, {node: "certain"}, name="opinion")
        elif random_interval == 1:
            nx.set_node_attributes(current_interaction, {node: "uncertain"}, name="opinion")

    print(current_interaction.nodes(data=True))


        # print(node)
        # print(current_interaction.nodes[node])






