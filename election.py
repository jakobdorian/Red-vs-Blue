import copy

import networkx as nx
import matplotlib.pyplot as plt
import random
from random import choice, sample
from helper import save_green, get_green, save_energy, get_energy, clear_energy, save_lifeline, get_lifeline, save_network, get_network, save_interval, get_interval, get_red_messages, get_blue_messages
import pandas as pd
import numpy as np
import time

RED_NODE = 26
BLUE_NODE = 27
minimax_sim = False
def start_game(network, green_team, red_team, blue_team, grey_team, uncertainty_interval):
    print("game is starting...")
    lifeline = False
    clear_energy()

    save_green(green_team)
    save_lifeline(lifeline)
    save_network(network)
    save_interval(uncertainty_interval)
    rounds = 0

    red_msgs = ["lvl1 potency", "lvl2 potency", "lvl3 potency", "lvl4 potency", "lvl5 potency"]
    blue_msgs = ["lvl1 potency", "lvl2 potency", "lvl3 potency", "lvl4 potency", "lvl5 potency"]
    # check_voters()
    # visualize_game(network)

    while True:
        # time.sleep(1)
        # rounds = rounds + 1

        green = get_green()

        # round where all green agents interact with each of their neighbours, potentially changing their opinions and uncertainty
        green_round(green)
        # check_voters()
        rounds = rounds + 1

        green = get_green()

        # round where the red agent interacts with all members in green team, potentially affecting their opinions
        #
        # red_skip = red_round(green, red_team)

        red_round(green, red_msgs, minimax_sim)
        rounds = rounds + 1

        # if red_skip:
        #     print("red skip")

        green = get_green()
        blue_energy = get_energy()
        # print(blue_energy)

        # round where the blue agent interacts with all members of the green team, potentially affecting their opinions
        # the goal of the blue agent is to convince those who are following the red team to follow them instead
        # blue team cannot lose followers
        # each time the blue agent interacts with an agent with a high certainty (0.7 to 1) they lose more energy
        # the blue agent can either lose energy or none at all during a round
        # if the blue agent does run out of energy, they can introduce a grey agent (blue round with no energy cost)
        # however there may be a chance that the grey agent is a spy, which gives the red agent a free round during blue teams round
        # blue_round(green, blue_team, grey_team, blue_energy)
        blue_round(green, blue_msgs, blue_energy, minimax_sim)
        rounds = rounds + 1

        current_energy = get_energy()
        # print(current_energy)

        green = get_green()
        # check_current_state(green)
        lifeline = get_lifeline()
        if current_energy >= 50 and lifeline == False:
            lifeline = True
            # reset energy
            energy = 0
            save_energy(energy)
            print("lifeline used")
            save_lifeline(lifeline)
            random_choice = choice(list(grey_team.nodes()))
            if grey_team.nodes[random_choice]["allegiance"] == "bad":
                # lifeline = True
                print("grey agent is spy")
                grey_bad_round(green_team, random_choice)
            elif grey_team.nodes[random_choice]["allegiance"] == "good":
                # lifeline = True
                energy = 0
                print("blue team has another round, thanks to grey team")
                grey_good_round(green_team, random_choice)
        elif current_energy >= 100 and lifeline == True:
            game_result(green, rounds)
            clear_energy()
            quit()
            # red_wins, blue_wins, ties, game_rounds = get_result(green, rounds)
            # return red_wins, blue_wins, ties, game_rounds
            # break

            # network = get_network()
            # visualize_game(network)

            # red_wins, blue_wins, ties, game_rounds = get_result(green, rounds)
            # return red_wins, blue_wins, ties, game_rounds

def green_round(green_team):
    for node in green_team.nodes():
        temp = list(green_team.neighbors(node))
        # randomly pick a neighbour to interact with
        temp2 = random.choice(temp)
        # print(temp2)
        # green_interaction(green_team, node, temp[x])
        agent1_updated_opinion, agent1_updated_uncertainty, agent2_updated_opinion, agent2_updated_uncertainty = green_interaction(green_team, node, temp2)
        # print(agent1_updated_opinion, agent1_updated_uncertainty, agent2_updated_opinion, agent2_updated_uncertainty)
        # print("old values:")
        # print(green_team.nodes[node]["opinion"])
        # print(green_team.nodes[node]["uncertainty"])
        # # print("\n")
        # print(green_team.nodes[temp2]["opinion"])
        # print(green_team.nodes[temp2]["uncertainty"])

        # set the updated values to agent1
        nx.set_node_attributes(green_team, {node: agent1_updated_opinion}, name="opinion")
        nx.set_node_attributes(green_team, {node: agent1_updated_uncertainty}, name="uncertainty")
        # set the updated values to agent2
        nx.set_node_attributes(green_team, {temp2: agent2_updated_opinion}, name="opinion")
        nx.set_node_attributes(green_team, {temp2: agent2_updated_uncertainty}, name="uncertainty")

        # print("updated values:")
        # print(green_team.nodes[node]["opinion"])
        # print(green_team.nodes[node]["uncertainty"])
        # # print("\n")
        # print(green_team.nodes[temp2]["opinion"])
        # print(green_team.nodes[temp2]["uncertainty"])


            # print("updated values")
    # return green_team
    save_green(green_team)

def red_message_selection(red_msgs):
    print("1. lvl1 potency msg")
    print("2. lvl2 potency msg")
    print("3. lvl3 potency msg")
    print("4. lvl4 potency msg")
    print("5. lvl5 potency msg")
    player_selection = input('Pick a message to send to the green agent: ')

    if player_selection == "1":
        player_message = red_msgs[0]
    elif player_selection == "2":
        player_message = red_msgs[1]
    elif player_selection == "3":
        player_message = red_msgs[2]
    elif player_selection == "4":
        player_message = red_msgs[3]
    elif player_selection == "5":
        player_message = red_msgs[4]
    else:
        print("invalid option!")
        print("please pick a number between 1-5: ")
    return player_message
def red_round(green_team, red_messages, minimax_sim):
    # red_msgs = ["lvl1 potency", "lvl2 potency", "lvl3 potency", "lvl4 potency", "lvl5 potency"]
    red_skip = False
    network = get_network()
    # randomly pick a potent message - TESTING
    random_msg = random.choice(red_messages)
    interval = get_interval()
    # random_msg = red_msgs[4]
    # player_message = red_message_selection(red_msgs)
    for node in green_team.nodes():
        # randomly pick a potent message - TESTING
        # random_msg = random.choice(red_msgs)
        # current_redmsg = red_msgs[4]
        a1_opinion, a1_uncertainty, red_opinion, red_uncertainty = red_interaction(green_team, node)


        # update new values
        nx.set_node_attributes(green_team, {node: a1_opinion}, name="opinion")
        nx.set_node_attributes(green_team, {node: a1_uncertainty}, name="uncertainty")

        # node wants to vote
        if green_team.nodes[node]["opinion"] == 1:
            # node is certain
            if green_team.nodes[node]["uncertainty"] < interval.mid:
                if random_msg == "lvl1 potency":
                    chance = random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
                    if chance == 1:
                            if green_team.nodes[node]["following"] != "blue":
                                nx.set_node_attributes(green_team, {node: "red"}, name="following")
                                network.add_edge(node, RED_NODE)
                elif random_msg == "lvl2 potency":
                    chance = random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8])
                    if chance == 1:
                        if green_team.nodes[node]["following"] != "blue":
                            nx.set_node_attributes(green_team, {node: "red"}, name="following")
                            network.add_edge(node, RED_NODE)
                elif random_msg == "lvl3 potency":
                    chance = random.choice([0, 1, 2, 3, 4, 5])
                    if chance == 1:
                        if green_team.nodes[node]["following"] != "blue":
                            nx.set_node_attributes(green_team, {node: "red"}, name="following")
                            network.add_edge(node, RED_NODE)
                    elif chance == 0:
                        nx.set_node_attributes(green_team, {node: "blue"}, name="following")
                        network.add_edge(node, RED_NODE)
                elif random_msg == "lvl4 potency":
                    # red team loses followers
                    chance = random.choice([0, 1, 2])
                    if chance == 1:
                        nx.set_node_attributes(green_team, {node: "red"}, name="following")
                        nx.set_node_attributes(green_team, {node: 0}, name="opinion")
                        network.add_edge(node, RED_NODE)
                    # red team loses followers
                    elif chance == 0:
                        nx.set_node_attributes(green_team, {node: "blue"}, name="following")
                        nx.set_node_attributes(green_team, {node: 0}, name="opinion")
                        network.add_edge(node, RED_NODE)
                        # print("red team has lost ", node, " as a follower!")
                elif random_msg == "lvl5 potency":
                    chance = random.choice([0, 1])
                    if chance == 1:
                        # if green_team.nodes[node]["following"] != "blue":
                        nx.set_node_attributes(green_team, {node: "red"}, name="following")
                        nx.set_node_attributes(green_team, {node: 0}, name="opinion")
                        network.add_edge(node, RED_NODE)
                    elif chance == 0:
                        # if green_team.nodes[node]["following"] != "blue":
                        nx.set_node_attributes(green_team, {node: "blue"}, name="following")
                        nx.set_node_attributes(green_team, {node: 0}, name="opinion")
                        network.add_edge(node, BLUE_NODE)
                        # print("red team has lost ", node, " as a follower!")
            # node is uncertain
            elif green_team.nodes[node]["uncertainty"] > interval.mid:
                if random_msg == "lvl1 potency":
                    chance = random.choice([0, 1, 2, 3])
                    if chance == 1:
                        # if green_team.nodes[node]["following"] != "blue":
                        nx.set_node_attributes(green_team, {node: "red"}, name="following")
                        network.add_edge(node, RED_NODE)
                elif random_msg == "lvl2 potency":
                    chance = random.choice([0, 1, 2])
                    if chance == 1:
                        # if green_team.nodes[node]["following"] != "blue":
                        nx.set_node_attributes(green_team, {node: "red"}, name="following")
                        network.add_edge(node, RED_NODE)
                elif random_msg == "lvl3 potency":
                    chance = random.choice([0, 1])
                    if chance == 1:
                        # if green_team.nodes[node]["following"] != "blue":
                        nx.set_node_attributes(green_team, {node: "red"}, name="following")
                        network.add_edge(node, RED_NODE)
                elif random_msg == "lvl4 potency":
                    # if green_team.nodes[node]["following"] != "blue":
                    nx.set_node_attributes(green_team, {node: "red"}, name="following")
                    network.add_edge(node, RED_NODE)
                    nx.set_node_attributes(green_team, {node: 0}, name="opinion")
                elif random_msg == "lvl5 potency":
                    # if green_team.nodes[node]["following"] != "blue":
                    nx.set_node_attributes(green_team, {node: "red"}, name="following")
                    nx.set_node_attributes(green_team, {node: 0}, name="opinion")
                    network.add_edge(node, RED_NODE)

    if not minimax_sim:
        save_green(green_team)
        save_network(network)

def red_interaction(green_team, node1):
    agent1_starting_opinion = green_team.nodes[node1]["opinion"]
    agent1_starting_uncertainty = green_team.nodes[node1]["uncertainty"]

    # TESTING - random choices
    # LET RED AGENT DECIDE THESE VALUES
    red_starting_opinion = random.choice([0, 1])
    # red_starting_uncertainty = round(random.uniform(-1.0, 1.0), 1)
    red_starting_uncertainty = round(random.uniform(0.0, 1.0), 1)

    agent1_updated_opinion, agent1_updated_uncertainty, red_updated_opinion, red_updated_uncertainty = update_rules(agent1_starting_opinion, agent1_starting_uncertainty, red_starting_opinion, red_starting_uncertainty)

    return agent1_updated_opinion, agent1_updated_uncertainty, red_updated_opinion, red_updated_uncertainty

def blue_interaction(green_team, node1):
    agent1_starting_opinion = green_team.nodes[node1]["opinion"]
    agent1_starting_uncertainty = green_team.nodes[node1]["uncertainty"]

    # TESTING - random choices
    # LET BLUE AGENT DECIDE THESE VALUES
    blue_starting_opinion = random.choice([0, 1])
    blue_starting_uncertainty = round(random.uniform(-1.0, 1.0), 1)

    agent1_updated_opinion, agent1_updated_uncertainty, blue_updated_opinion, blue_updated_uncertainty = update_rules(agent1_starting_opinion, agent1_starting_uncertainty, blue_starting_opinion, blue_starting_uncertainty)

    return agent1_updated_opinion, agent1_updated_uncertainty, blue_updated_opinion, blue_updated_uncertainty
# returns new opinion and uncertainty of agent1
def green_interaction(green_team, node1, node2):
    agent1_starting_opinion = green_team.nodes[node1]["opinion"]
    agent1_starting_uncertainty = green_team.nodes[node1]["uncertainty"]

    agent2_starting_opinion = green_team.nodes[node2]["opinion"]
    agent2_starting_uncertainty = green_team.nodes[node2]["uncertainty"]

    agent1_updated_opinion, agent1_updated_uncertainty, agent2_updated_opinion, agent2_updated_uncertainty = update_rules(agent1_starting_opinion, agent1_starting_uncertainty, agent2_starting_opinion, agent2_starting_uncertainty)

    return agent1_updated_opinion, agent1_updated_uncertainty, agent2_updated_opinion, agent2_updated_uncertainty

# returns updated values for the opinion and uncertainty after the interaction of two nodes/agents
def update_rules(agent1_starting_opinion, agent1_starting_uncertainty, agent2_starting_opinion, agent2_starting_uncertainty):
    interval = get_interval()
    # both agents want to vote and have a high uncertainty
    if agent1_starting_opinion == 1 and agent1_starting_uncertainty > interval.mid and agent2_starting_opinion == 1 and agent2_starting_uncertainty > interval.mid:
        # print("1. both agents want to vote and have a highly uncertain. they will change their votes")
        agent1_updated_opinion = agent1_starting_opinion
        agent1_updated_uncertainty = agent1_starting_uncertainty - 0.1

        agent2_updated_opinion = agent2_starting_opinion
        agent2_updated_uncertainty = agent2_starting_uncertainty - 0.1

        return agent1_updated_opinion, agent1_updated_uncertainty, agent2_updated_opinion, agent2_updated_uncertainty
    # both agents don't want to vote and have a low uncertainty
    elif agent1_starting_opinion == 0 and agent1_starting_uncertainty < interval.mid and agent2_starting_opinion == 0 and agent2_starting_uncertainty < interval.mid:
        # print("2. both agents do not want to vote and are certain of their current vote")
        agent1_updated_opinion = agent1_starting_opinion
        agent1_updated_uncertainty = agent1_starting_uncertainty + 0.1

        agent2_updated_opinion = agent2_starting_opinion
        agent2_updated_uncertainty = agent2_starting_uncertainty + 0.1

        return agent1_updated_opinion, agent1_updated_uncertainty, agent2_updated_opinion, agent2_updated_uncertainty
    # agent 1 wants to vote but agent 2 does not, if the agent1's uncertainty is greater than agent2's uncertainty,
    # then update the uncertainty
    # else, just update the opinion
    elif agent1_starting_opinion == 1 and agent1_starting_uncertainty > interval.mid and agent2_starting_opinion == 0 and agent2_starting_uncertainty > interval.mid:
        if agent1_starting_uncertainty > agent2_starting_uncertainty:
            # print("3. agent1 convinces agent2 to vote")
            agent1_updated_opinion = agent1_starting_opinion
            agent1_updated_uncertainty = agent1_starting_uncertainty + 0.1

            agent2_updated_opinion = agent1_updated_opinion
            agent2_updated_uncertainty = agent2_starting_uncertainty + 0.1

            return agent1_updated_opinion, agent1_updated_uncertainty, agent2_updated_opinion, agent2_updated_uncertainty

        else:
            # print("3. true")
            agent1_updated_opinion = agent1_starting_opinion
            agent1_updated_uncertainty = agent1_starting_uncertainty

            agent2_updated_opinion = agent1_updated_opinion
            agent2_updated_uncertainty = agent2_starting_uncertainty

            return agent1_updated_opinion, agent1_updated_uncertainty, agent2_updated_opinion, agent2_updated_uncertainty
    elif agent1_starting_opinion == 0 and agent1_starting_uncertainty < interval.mid and agent2_starting_opinion == 1 and agent2_starting_uncertainty > interval.mid:
        # print("4. agent2 convinces agent1 to vote")
        agent1_updated_opinion = 1
        agent1_updated_uncertainty = agent1_starting_uncertainty + 0.2

        agent2_updated_opinion = agent2_starting_opinion
        agent2_updated_uncertainty = agent2_starting_uncertainty + 0.1

        return agent1_updated_opinion, agent1_updated_uncertainty, agent2_updated_opinion, agent2_updated_uncertainty
    # both agents are highly uncertain and now want to vote
    elif agent1_starting_opinion == 0 and agent1_starting_uncertainty > interval.mid and agent2_starting_opinion == 0 and agent2_starting_uncertainty > interval.mid:
        # print("5. both agents are highly uncertain and now want to vote")
        agent1_updated_opinion = 1
        agent1_updated_uncertainty = agent1_starting_uncertainty - 0.2

        agent2_updated_opinion = 1
        agent2_updated_uncertainty = agent2_starting_uncertainty - 0.2

        return agent1_updated_opinion, agent1_updated_uncertainty, agent2_updated_opinion, agent2_updated_uncertainty
    # if the agents do not meet any of the conditions, return the original values
    else:
        # print("!!!! no conditions met")
        return agent1_starting_opinion, agent1_starting_uncertainty, agent2_starting_opinion, agent2_starting_uncertainty

def blue_round(green_team, blue_messages, energy, minimax_sim):
    # correction messages
    # blue_msgs = ["lvl1 potency", "lvl2 potency", "lvl3 potency", "lvl4 potency", "lvl5 potency"]
    # if blue team uses all of its energy, the game ends
    network = get_network()
    interval = get_interval()
    random_msg = random.choice(blue_messages)
    for node in green_team.nodes():
        # randomly pick a potent message - TESTING
        # random_msg = random.choice(blue_msgs)
        a1_opinion, a1_uncertainty, blue_opinion, blue_uncertainty = blue_interaction(green_team, node)

        nx.set_node_attributes(green_team, {node: a1_opinion}, name="opinion")
        nx.set_node_attributes(green_team, {node: a1_uncertainty}, name="uncertainty")

        # node wants to vote
        if green_team.nodes[node]["opinion"] == 1:
            # node is certain
            if green_team.nodes[node]["uncertainty"] < interval.mid:
                energy = energy + 2
                if random_msg == "lvl1 potency":
                    chance = random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
                    if chance == 1:
                        nx.set_node_attributes(green_team, {node: "blue"}, name="following")
                        network.add_edge(node, BLUE_NODE)
                elif random_msg == "lvl2 potency":
                    chance = random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8])
                    if chance == 1:
                        nx.set_node_attributes(green_team, {node: "blue"}, name="following")
                        network.add_edge(node, BLUE_NODE)
                        energy = energy + 1
                elif random_msg == "lvl3 potency":
                    chance = random.choice([0, 1, 2, 3, 4, 5])
                    if chance == 1:
                        nx.set_node_attributes(green_team, {node: "blue"}, name="following")
                        network.add_edge(node, BLUE_NODE)
                        energy = energy + 2
                elif random_msg == "lvl4 potency":
                    chance = random.choice([0, 1, 2])
                    if chance == 1:
                        nx.set_node_attributes(green_team, {node: "blue"}, name="following")
                        nx.set_node_attributes(green_team, {node: 0}, name="opinion")
                        network.add_edge(node, BLUE_NODE)
                        energy = energy + 3
                elif random_msg == "lvl5 potency":
                    chance = random.choice([0, 1, 2])
                    if chance == 1:
                        nx.set_node_attributes(green_team, {node: "blue"}, name="following")
                        nx.set_node_attributes(green_team, {node: 0}, name="opinion")
                        network.add_edge(node, BLUE_NODE)
                        energy = energy + 4
            # node is uncertain
            elif green_team.nodes[node]["uncertainty"] > interval.mid:
                energy = energy + 1
                if random_msg == "lvl1 potency":
                    chance = random.choice([0, 1, 2, 3])
                    if chance == 1:
                        nx.set_node_attributes(green_team, {node: "blue"}, name="following")
                        network.add_edge(node, BLUE_NODE)
                elif random_msg == "lvl2 potency":
                    chance = random.choice([0, 1, 2])
                    if chance == 1:
                        nx.set_node_attributes(green_team, {node: "blue"}, name="following")
                        network.add_edge(node, BLUE_NODE)
                elif random_msg == "lvl3 potency":
                    chance = random.choice([0, 1])
                    if chance == 1:
                        nx.set_node_attributes(green_team, {node: "blue"}, name="following")
                        network.add_edge(node, BLUE_NODE)
                elif random_msg == "lvl4 potency":
                    nx.set_node_attributes(green_team, {node: "blue"}, name="following")
                    nx.set_node_attributes(green_team, {node: 0}, name="opinion")
                    network.add_edge(node, BLUE_NODE)
                    energy = energy + 1
                elif random_msg == "lvl5 potency":
                    nx.set_node_attributes(green_team, {node: "blue"}, name="following")
                    nx.set_node_attributes(green_team, {node: 0}, name="opinion")
                    network.add_edge(node, BLUE_NODE)
                    energy = energy + 2

    if not minimax_sim:
        save_green(green_team)
        save_network(network)
        save_energy(energy)

# grey agent is working for the team
def grey_good_round(green_team, grey_node):
    network = get_network()
    interval = get_interval()
    blue_msgs = ["lvl1 potency", "lvl2 potency", "lvl3 potency", "lvl4 potency", "lvl5 potency"]
    random_msg = random.choice(blue_msgs)
    for node in green_team.nodes():
        # randomly pick a potent message - TESTING

        a1_opinion, a1_uncertainty, blue_opinion, blue_uncertainty = blue_interaction(green_team, node)

        nx.set_node_attributes(green_team, {node: a1_opinion}, name="opinion")
        nx.set_node_attributes(green_team, {node: a1_uncertainty}, name="uncertainty")

        # node wants to vote
        if green_team.nodes[node]["opinion"] == 1:
            # node is certain
            if green_team.nodes[node]["uncertainty"] < interval.mid:
                if random_msg == "lvl1 potency":
                    chance = random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
                    if chance == 1:
                        nx.set_node_attributes(green_team, {node: "blue"}, name="following")
                        network.add_edge(node, grey_node)
                elif random_msg == "lvl2 potency":
                    chance = random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8])
                    if chance == 1:
                        nx.set_node_attributes(green_team, {node: "blue"}, name="following")
                        network.add_edge(node, grey_node)
                elif random_msg == "lvl3 potency":
                    chance = random.choice([0, 1, 2, 3, 4, 5])
                    if chance == 1:
                        nx.set_node_attributes(green_team, {node: "blue"}, name="following")
                        network.add_edge(node, grey_node)
                elif random_msg == "lvl4 potency":
                    chance = random.choice([0, 1, 2])
                    if chance == 1:
                        nx.set_node_attributes(green_team, {node: "blue"}, name="following")
                        nx.set_node_attributes(green_team, {node: 0}, name="opinion")
                        network.add_edge(node, grey_node)
                elif random_msg == "lvl5 potency":
                    chance = random.choice([0, 1, 2])
                    if chance == 1:
                        nx.set_node_attributes(green_team, {node: "blue"}, name="following")
                        nx.set_node_attributes(green_team, {node: 0}, name="opinion")
                        network.add_edge(node, grey_node)
            # node is uncertain
            elif green_team.nodes[node]["uncertainty"] > interval.mid:
                if random_msg == "lvl1 potency":
                    chance = random.choice([0, 1, 2, 3])
                    if chance == 1:
                        nx.set_node_attributes(green_team, {node: "blue"}, name="following")
                        network.add_edge(node, grey_node)
                elif random_msg == "lvl2 potency":
                    chance = random.choice([0, 1, 2])
                    if chance == 1:
                        nx.set_node_attributes(green_team, {node: "blue"}, name="following")
                        network.add_edge(node, grey_node)
                elif random_msg == "lvl3 potency":
                    chance = random.choice([0, 1])
                    if chance == 1:
                        nx.set_node_attributes(green_team, {node: "blue"}, name="following")
                        network.add_edge(node, grey_node)
                elif random_msg == "lvl4 potency":
                    nx.set_node_attributes(green_team, {node: "blue"}, name="following")
                    nx.set_node_attributes(green_team, {node: 0}, name="opinion")
                    network.add_edge(node, grey_node)
                elif random_msg == "lvl5 potency":
                    nx.set_node_attributes(green_team, {node: "blue"}, name="following")
                    nx.set_node_attributes(green_team, {node: 0}, name="opinion")
                    network.add_edge(node, grey_node)

    save_green(green_team)

# grey agent is working for the red team
def grey_bad_round(green_team, grey_node):
    network = get_network()
    interval = get_interval()
    red_msgs = ["lvl1 potency", "lvl2 potency", "lvl3 potency", "lvl4 potency", "lvl5 potency"]
    random_msg = random.choice(red_msgs)
    for node in green_team.nodes():
        # player_message = red_message_selection(red_msgs)

        # randomly pick a potent message - TESTING

        a1_opinion, a1_uncertainty, red_opinion, red_uncertainty = red_interaction(green_team, node)

        # update new values
        nx.set_node_attributes(green_team, {node: a1_opinion}, name="opinion")
        nx.set_node_attributes(green_team, {node: a1_uncertainty}, name="uncertainty")

        # node wants to vote
        if green_team.nodes[node]["opinion"] == 1:
            # node is certain
            if green_team.nodes[node]["uncertainty"] < interval.mid:
                if random_msg == "lvl1 potency":
                    chance = random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
                    if chance == 1:
                        nx.set_node_attributes(green_team, {node: "red"}, name="following")
                        network.add_edge(node, grey_node)
                elif random_msg == "lvl2 potency":
                    chance = random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8])
                    if chance == 1:
                        nx.set_node_attributes(green_team, {node: "red"}, name="following")
                        network.add_edge(node, grey_node)
                elif random_msg == "lvl3 potency":
                    chance = random.choice([0, 1, 2, 3, 4, 5])
                    if chance == 1:
                        nx.set_node_attributes(green_team, {node: "red"}, name="following")
                        network.add_edge(node, grey_node)
                elif random_msg == "lvl4 potency":
                    chance = random.choice([0, 1, 2])
                    if chance == 1:
                        nx.set_node_attributes(green_team, {node: "red"}, name="following")
                        nx.set_node_attributes(green_team, {node: 0}, name="opinion")
                        network.add_edge(node, grey_node)
                elif random_msg == "lvl5 potency":
                    chance = random.choice([0, 1, 2])
                    if chance == 1:
                        nx.set_node_attributes(green_team, {node: "red"}, name="following")
                        nx.set_node_attributes(green_team, {node: 0}, name="opinion")
                        network.add_edge(node, grey_node)
            # node is uncertain
            elif green_team.nodes[node]["uncertainty"] > interval.mid:
                if random_msg == "lvl1 potency":
                    chance = random.choice([0, 1, 2, 3])
                    if chance == 1:
                        nx.set_node_attributes(green_team, {node: "red"}, name="following")
                        network.add_edge(node, grey_node)
                elif random_msg == "lvl2 potency":
                    chance = random.choice([0, 1, 2])
                    if chance == 1:
                        nx.set_node_attributes(green_team, {node: "red"}, name="following")
                        network.add_edge(node, grey_node)
                elif random_msg == "lvl3 potency":
                    chance = random.choice([0, 1])
                    if chance == 1:
                        nx.set_node_attributes(green_team, {node: "red"}, name="following")
                        network.add_edge(node, grey_node)
                elif random_msg == "lvl4 potency":
                    nx.set_node_attributes(green_team, {node: "red"}, name="following")
                    nx.set_node_attributes(green_team, {node: 0}, name="opinion")
                    network.add_edge(node, grey_node)
                elif random_msg == "lvl5 potency":
                    nx.set_node_attributes(green_team, {node: "red"}, name="following")
                    nx.set_node_attributes(green_team, {node: 0}, name="opinion")
                    network.add_edge(node, grey_node)

    save_green(green_team)

def lose_followers():
    # NEEDS REWORK
    # make a copy of graph you can iterate over
    agents = get_green()
    temp_copy = agents.copy()
    for node in temp_copy.nodes():
        # print(temp_copy.nodes[node])
        # if a message is highly potent, then remove it from the current graph
        if agents.nodes[node]["opinion"] == "lvl5 potency" or agents.nodes[node]["opinion"] == "lvl4 potency":
            # agents.remove_node(node)
            # if a message is too potent, that green agent will unfollow the red team
            nx.set_node_attributes(agents, {node: "no vote"}, name="following")

    save_green(agents)
def visualize_game(network):
    color_nodes = []
    for node in network.nodes():
        # print(network.nodes[node]["team"])
        if network.nodes[node]["team"] == "green":
            color_nodes.append('green')
        elif network.nodes[node]["team"] == "red":
            color_nodes.append('red')
        elif network.nodes[node]["team"] == "blue":
            color_nodes.append('blue')
        elif network.nodes[node]["team"] == "grey":
            color_nodes.append('grey')
    # print(color_nodes)
    nx.draw(network, node_color=color_nodes, with_labels=True)
    plt.show()

# returns the nodes of the green team who want to vote
def check_voters():
    green_team = get_green()
    count = 0
    voters = []
    for node in green_team.nodes():
        if green_team.nodes[node]["opinion"] == 1:
            # print("agent", node, "wants to vote")
            count = count + 1
            voters.append(node)
    print("number of voters:", count)
    print(voters)
    return voters
# returns the current state of the game
def check_current_state(green):
    red = 0
    blue = 0
    for node in green.nodes():
        # print(green_team.nodes[node]["following"])
        if "following" in green.nodes[node]:
            if green.nodes[node]["following"] == "red":
                red = red + 1
            elif green.nodes[node]["following"] == "blue":
                blue = blue + 1
    print("current red followers: ", red)
    print("current blue followers: ", blue)
# returns the result of the game once the game has ended
def game_result(green_team, game_rounds):
    red = 0
    blue = 0

    for node in green_team.nodes():
        # print(green_team.nodes[node]["following"])
        if "following" in green_team.nodes[node]:
            if green_team.nodes[node]["following"] == "red":
                red = red + 1
            elif green_team.nodes[node]["following"] == "blue":
                blue = blue + 1
    print("election has ended after", game_rounds, "rounds of voting!")
    if red > blue:
        print("\n")
        print("red team wins!")
        print("red followers: ", red)
        print("blue followers: ", blue)
        total = red + blue
        print("total voters: ", total)
    elif blue > red:
        print("\n")
        print("blue team wins!")
        print("red followers: ", red)
        print("blue followers: ", blue)
        total = red + blue
        print("total voters: ", total)
    elif red == blue:
        print("\n")
        print("it's a tie!")
        print("red followers: ", red)
        print("blue followers: ", blue)
        total = red + blue
        print("total voters: ", total)

def game_result2(green_team):
    red = 0
    blue = 0

    for node in green_team.nodes():
        # print(green_team.nodes[node]["following"])
        if "following" in green_team.nodes[node]:
            if green_team.nodes[node]["following"] == "red":
                red = red + 1
            elif green_team.nodes[node]["following"] == "blue":
                blue = blue + 1
    # print("election has ended after", game_rounds, "rounds of voting!")
    if red > blue:
        print("\n")
        print("red team wins!")
        print("red followers: ", red)
        print("blue followers: ", blue)
        total = red + blue
        print("total voters: ", total)
    elif blue > red:
        print("\n")
        print("blue team wins!")
        print("red followers: ", red)
        print("blue followers: ", blue)
        total = red + blue
        print("total voters: ", total)
    elif red == blue:
        print("\n")
        print("it's a tie!")
        print("red followers: ", red)
        print("blue followers: ", blue)
        total = red + blue
        print("total voters: ", total)


def get_result(green_team, game_rounds):
    red = 0
    blue = 0
    red_wins = 0
    blue_wins = 0
    ties = 0
    for node in green_team.nodes():
        if "following" in green_team.nodes[node]:
            if green_team.nodes[node]["following"] == "red":
                red = red + 1
            elif green_team.nodes[node]["following"] == "blue":
                blue = blue + 1
    if red > blue:
        red_wins = red_wins + 1
    elif blue > red:
        blue_wins = blue_wins + 1
    elif red == blue:
        ties = ties + 1

    return red_wins, blue_wins, ties, game_rounds

# a minimax agent to play the game as the red or blue agent
def minimax(network, maximizing, alpha, beta, depth):
    # red_messages = get_red_messages()
    minimax_sim = True
    if depth == 0:
        return game_result2(network)
    # red minimax agent
    elif maximizing:
        optimal = -float("Inf")
        messages = get_blue_messages()
        current_messsage = messages[0]
        for msg in messages:
            temp_network = copy.deepcopy(network)
            red_round(temp_network, messages, minimax_sim)
            huer = minimax(temp_network, False, depth - 1, -float("Inf"), float("Inf"))
            if huer > optimal:
                best_message = msg
            alpha = max(alpha, optimal)
            if alpha >= beta:
                break
        return best_message
    # blue minimax agent
    else:
        optimal = float("Inf")
        messages = get_blue_messages()
        current_messsage = messages[0]
        for msg in messages:
            temp_network = copy.deepcopy(network)
            blue_round(temp_network, messages)
            huer = minimax(temp_network, True, depth - 1, -float("Inf"), float("Inf"))
            if huer > optimal:
                best_message = msg
            beta = min(beta, optimal)
            if alpha >= beta:
                break
        return best_message



