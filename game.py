import networkx as nx
import matplotlib.pyplot as plt
import random
import pandas as pd
import numpy as np
def start_game(network, green_team, red_team, blue_team, grey_team):
    print("game is starting...")
    # print(network.nodes(data=True))
    # print(green_team)
    # print(red_team)
    # print(blue_team)
    # print(grey_good_team)
    # print(grey_bad_team)
    redgreen_interaction = interaction_round(green_team, red_team)

    # agents after redgreen interation
    current_green_agents = lose_followers(redgreen_interaction)

    blue_interaction_round(current_green_agents, blue_team, grey_team)
    # print(current_green_agents)

    g_dict = nx.to_dict_of_dicts(network)


def interaction_round(green_agents, interacting_agent):
    # combine red and green nodes into one graph
    current_interaction = nx.compose(green_agents, interacting_agent)
    # list of levels of potency messages
    # red_msgs = ["lvl1 potency", "lvl2 potency", "lvl3 potency", "lvl4 potency", "lvl5 potency"]
    red_msgs_low = ["lvl1 potency", "lvl2 potency", "lvl3 potency"]
    red_msgs_high = ["lvl3 potency", "lvl4 potency", "lvl5 potency"]
    # print(current_interaction.nodes(data=True))
    # nx.draw(current_interaction)
    # plt.show()

    # SET CONFIDENCE FOR EACH NODE RANDOMLY
    certain = 0.0
    uncertain = 0.0
    for node in current_interaction.nodes():
        # randomly select a potency message
        # current_redmsg = random.choice(red_msgs)
        # nx.set_node_attributes(agent1, {node: current_redmsg}, name="opinion")
        random_interval = random.choice([-1, 1])
        current_confidence = get_confidence(green_agents)
        if random_interval == -1:
            nx.set_node_attributes(green_agents, {node: "certain"}, name="confidence")
            certain = certain + 1.0
            current_redmsg = random.choice(red_msgs_high)
            nx.set_node_attributes(green_agents, {node: current_redmsg}, name="opinion")
        elif random_interval == 1:
            nx.set_node_attributes(green_agents, {node: "uncertain"}, name="confidence")
            uncertain = uncertain + 1.0
            current_redmsg = random.choice(red_msgs_low)
            nx.set_node_attributes(green_agents, {node: current_redmsg}, name="opinion")
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

    return green_agents

    # print(current_interaction.nodes.data("confidence"))
    # print(green_agent.nodes(data=True))
    # for node in current_interaction.nodes():
    #     if current_interaction.nodes[node]["confidence"] == "certain":
    #         print(current_interaction.nodes[node])
    #     elif current_interaction.nodes[node]["confidence"] == "uncertain":
    #         print(current_interaction.nodes[node])


def blue_interaction_round(green_agents, blue_agent, grey_team):
    energy = 0
    current_interaction = nx.compose(green_agents, blue_agent)
    # go through each green agent in the network and check their confidence level, if they are certain
    for node in current_interaction.nodes():
        # make sure blue team doesn't use more excessive energy interacting with green team
        if energy < 10:
            if "confidence" in current_interaction.nodes[node]:
                if current_interaction.nodes[node]["confidence"] == "certain":
                    energy = energy + 1
                    # if energy is not exhausted keep interacting with green agents
                    if energy == 10:
                        print("blue team has used up all of its energy!")
                        break
                    else:
                        continue
                    # print(current_interaction.nodes[node])
def update_rules():
    print("")


def get_confidence(agents):
    val = [np.random.choice(agents, size=len(agents), replace=True).mean() for i in range(1000)]
    val2 = np.percentile(val, [100 * (1 - 0.95) / 2, 100 * (1 - (1 - 0.95) / 2)])
    # print(val2)
    return val2

def lose_followers(agents):
    # make a copy of graph you can iterate over
    temp_copy = agents.copy()
    for node in temp_copy.nodes():
        # if a message is highly potent, then remove it from the current graph
        if agents.nodes[node]["opinion"] == "lvl5 potency":
            agents.remove_node(node)
    return agents
def minimax(current_depth, current_nodeindex, max_depth, target_depth, scores):
    if current_depth == target_depth:
        return scores[current_nodeindex]


    # print(current_interaction.nodes(data=True))







