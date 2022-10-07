import networkx as nx
import matplotlib.pyplot as plt
import random
from random import choice, sample
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
    # redgreen_interaction = interaction_round(green_team, red_team)

    red_interaction_round(green_team, red_team)

    # agents after redgreen interation
    # current_green_agents = lose_followers(redgreen_interaction)
    # current_green_agents = blue_interaction_round(current_green_agents, blue_team, grey_team)
    # game_result(current_green_agents)
    # visualize_game(network)
    # g_dict = nx.to_dict_of_dicts(network)


def red_interaction_round(green_team, red_team):
    current_interaction = nx.compose(green_team, red_team)
    red_msgs = ["lvl1 potency", "lvl2 potency", "lvl3 potency", "lvl4 potency", "lvl5 potency"]

    agent_neighbours = []
    # print(green_team.edges)
    for node in green_team.nodes():
        # print(list(green_team.neighbors(node)))
        temp = list(green_team.neighbors(node))
        for x in range(len(temp)):
            # print(node)
            # print(temp[x])
            green_interaction(green_team, node, temp[x])


# should return new opinion and uncertainty of agent1
def green_interaction(green_team, node1, node2):
    # print(agent1)
    # print(agent2)
    # print("testing green interaction")

    if green_team.nodes[node1]["uncertainty"] > 0.5 and green_team.nodes[node1]["opinion"] == 1:
        print("agent wants to vote!")
    elif green_team.nodes[node1]["uncertainty"] < 0.5 and green_team.nodes[node1]["opinion"] == 0:
        print("agent does NOT want to vote...")

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
    # test1 = round(random.uniform(-1.0, 1.0), 1)
    # print(test1)

    for node in current_interaction.nodes():
        # randomly select a potency message
        # current_redmsg = random.choice(red_msgs)
        # nx.set_node_attributes(agent1, {node: current_redmsg}, name="opinion")
        # random_interval = random.choice([-1, 1])
        random_interval = round(random.uniform(-1.0, 1.0), 1)
        # print(random_interval)
        # current_confidence = get_confidence(green_agents)
        if random_interval < 0.5:
            nx.set_node_attributes(green_agents, {node: "certain"}, name="confidence")
            certain = certain + 1.0
            current_redmsg = random.choice(red_msgs_high)
            nx.set_node_attributes(green_agents, {node: current_redmsg}, name="opinion")
            # nx.set_node_attributes(green_agents, {node: "red"}, name="following")
        elif random_interval > 0.5:
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
    lifeline_used = False
    current_interaction = nx.compose(green_agents, blue_agent)
    random_choice = choice(list(grey_team.nodes()))
    # print(random_choice)
    # go through each green agent in the network and check their confidence level, if they are certain
    for node in current_interaction.nodes():
        # make sure blue team doesn't use more excessive energy interacting with green team
        if energy < 10:
            if "confidence" in current_interaction.nodes[node]:
                if current_interaction.nodes[node]["confidence"] == "uncertain":
                    nx.set_node_attributes(green_agents, {node: "blue"}, name="following")
                elif current_interaction.nodes[node]["confidence"] == "certain":
                    energy = energy + 1
                    # if energy is not exhausted keep interacting with green agents
                    if energy == 10:
                        print("blue team has used up all of its energy!")
                        # the blue team has a 1/2 chance of introducing a grey agent if they run out of energy
                        random_chance = random.choice([1, 2])
                        if random_chance == 1:
                            print("no grey agent")
                            break
                        elif random_chance == 2:
                            print(grey_team.nodes[random_choice])
                            # however, there is a chance that the grey agent is a spy
                            if grey_team.nodes[random_choice]["allegiance"] == "bad":
                                lifeline_used = True
                                energy = 0
                                print("grey agent is a spy!")
                            elif grey_team.nodes[random_choice]["allegiance"] == "good":
                                lifeline_used = True
                                energy = 0
                                print("grey agent is NOT a spy!")
                    else:
                        continue
    return green_agents
                    # print(current_interaction.nodes[node])
def lose_followers(agents):
    # make a copy of graph you can iterate over
    temp_copy = agents.copy()
    for node in temp_copy.nodes():
        # print(temp_copy.nodes[node])
        # if a message is highly potent, then remove it from the current graph
        if agents.nodes[node]["opinion"] == "lvl5 potency" or agents.nodes[node]["opinion"] == "lvl4 potency":
            # agents.remove_node(node)
            # if a message is too potent, that green agent will unfollow the red team
            nx.set_node_attributes(agents, {node: "unfollowed"}, name="red-followers")

    return agents
def visualize_game(network):
    color_nodes = []
    for node in network.nodes():
        # print(network.nodes[node]["team"])
        if network.nodes[node]["team"] == {"green"}:
            color_nodes.append('green')
        elif network.nodes[node]["team"] == {"red"}:
            color_nodes.append('red')
        elif network.nodes[node]["team"] == {"blue"}:
            color_nodes.append('blue')
        elif network.nodes[node]["team"] == {"grey"}:
            color_nodes.append('grey')
    # print(color_nodes)
    nx.draw(network, node_color=color_nodes, with_labels=True)
    plt.show()

def game_result(green_team):
    red = 0
    blue = 0
    for node in green_team.nodes():
        # print(green_team.nodes[node]["following"])
        if "following" in green_team.nodes[node]:
            if green_team.nodes[node]["following"] == "red":
                red = red + 1
            elif green_team.nodes[node]["following"] == "blue":
                blue = blue + 1
    if red > blue:
        print("red team wins!")
    elif blue > red:
        print("blue team wins!")
    elif red == blue:
        print("it's a tie!")


