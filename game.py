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

    # SET CONFIDENCE FOR EACH NODE RANDOMLY
    certain = 0.0
    uncertain = 0.0
    for node in current_interaction.nodes():
        random_interval = random.choice([-1, 1])
        if random_interval == -1:
            nx.set_node_attributes(current_interaction, {node: "certain"}, name="opinion")
            certain = certain + 1.0
        elif random_interval == 1:
            nx.set_node_attributes(current_interaction, {node: "uncertain"}, name="opinion")
            uncertain = uncertain + 1.0
    if certain > uncertain:
        temp = uncertain / certain
        temp = temp * 100
        temp2 = 100 - temp
        print(str(round(temp)) + "% of", "green team is certain")
        print(str(round(temp2)) + "% of", "green team is uncertain")
        # print(temp2)
    else:
        temp = certain / uncertain
        temp = temp * 100
        temp2 = 100 - temp
        print(str(round(temp)) + "% of", "green team is uncertain")
        print(str(round(temp2)) + "% of", "green team is certain")


    # print(current_interaction.nodes(data=True))







