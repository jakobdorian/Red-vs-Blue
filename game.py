import networkx as nx
import matplotlib.pyplot as plt
import random
from random import choice, sample
from helper import save_green, get_green, save_energy, get_energy, clear_energy
import pandas as pd
import numpy as np
import time
def start_game(network, green_team, red_team, blue_team, grey_team):
    print("game is starting...")
    lifeline = False
    clear_energy()
    blue_max = 20
    energy = 0
    save_green(green_team)
    rounds = 0

    while True:
        time.sleep(1)
        rounds = rounds + 1

        green = get_green()

        # round where all green agents interact with each of their neighbours, potentially changing their opinions and uncertainty
        green_round(green)

        green = get_green()

        # round where the red agent interacts with all members in green team, potentially affecting their opinions
        #
        red_skip = red_round(green, red_team)

        if red_skip:
            print("red skip")

        green = get_green()
        blue_energy = get_energy()
        print(blue_energy)

        # round where the blue agent interacts with all members of the green team, potentially affecting their opinions
        # the goal of the blue agent is to convince those who are following the red team to follow them instead
        # blue team cannot lose followers
        # each time the blue agent interacts with an agent with a high certainty (0.7 to 1) they lose more energy
        # the blue agent can either lose energy or none at all during a round
        # if the blue agent does run out of energy, they can introduce a grey agent (blue round with no energy cost)
        # however there may be a chance that the grey agent is a spy, which gives the red agent a free round during blue teams round
        blue_round(green, blue_team, grey_team, blue_energy, lifeline)

        current_energy = get_energy()
        # print(current_energy)

        green = get_green()
        # check_current_state(green)

        if current_energy >= 20:
            game_result(green, rounds)
            clear_energy()
            break
def green_round(green_team):
    for node in green_team.nodes():
        temp = list(green_team.neighbors(node))
        for x in range(len(temp)):
            # green_interaction(green_team, node, temp[x])
            agent1_updated_opinion, agent1_updated_uncertainty, agent2_updated_opinion, agent2_updated_uncertainty = green_interaction(green_team, node, temp[x])
            # print(agent1_updated_opinion, agent1_updated_uncertainty, agent2_updated_opinion, agent2_updated_uncertainty)

            # set the updated values to agent1
            nx.set_node_attributes(green_team, {node: agent1_updated_opinion}, name="opinion")
            nx.set_node_attributes(green_team, {node: agent1_updated_uncertainty}, name="uncertainty")
            # set the updated values to agent2
            nx.set_node_attributes(green_team, {temp[x]: agent2_updated_opinion}, name="opinion")
            nx.set_node_attributes(green_team, {temp[x]: agent2_updated_uncertainty}, name="uncertainty")
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
def red_round(green_team, red_team):
    current_interaction = nx.compose(green_team, red_team)
    red_msgs = ["lvl1 potency", "lvl2 potency", "lvl3 potency", "lvl4 potency", "lvl5 potency"]
    red_skip = False
    for node in green_team.nodes():
        # player_message = red_message_selection(red_msgs)

        # randomly pick a potent message - TESTING
        current_redmsg = random.choice(red_msgs)

        # message is not potent enough to have an affect
        if current_redmsg == "lvl1 potency":
            break
        elif current_redmsg == "lvl2 potency":
            break
        elif current_redmsg == "lvl3 potency" and green_team.nodes[node]["opinion"] == 1:
            chance = random.choice([0, 1])
            if chance == 1:
                nx.set_node_attributes(green_team, {node: "red"}, name="following")
        # highly potent message and agent wants to vote
        elif current_redmsg == "lvl4 potency" and green_team.nodes[node]["opinion"] == 1:
            nx.set_node_attributes(green_team, {node: "red"}, name="following")
            red_skip = True
        elif current_redmsg == "lvl5 potency" and green_team.nodes[node]["opinion"] == 1:
            nx.set_node_attributes(green_team, {node: "red"}, name="following")
            red_skip = True

    save_green(green_team)
    return red_skip

# should return new opinion and uncertainty of agent1
def green_interaction(green_team, node1, node2):
    agent1_starting_opinion = green_team.nodes[node1]["opinion"]
    agent1_starting_uncertainty = green_team.nodes[node1]["uncertainty"]

    agent2_starting_opinion = green_team.nodes[node2]["opinion"]
    agent2_starting_uncertainty = green_team.nodes[node2]["uncertainty"]

    agent1_updated_opinion, agent1_updated_uncertainty, agent2_updated_opinion, agent2_updated_uncertainty = update_rules(agent1_starting_opinion, agent1_starting_uncertainty, agent2_starting_opinion, agent2_starting_uncertainty)

    return agent1_updated_opinion, agent1_updated_uncertainty, agent2_updated_opinion, agent2_updated_uncertainty

def update_rules(agent1_starting_opinion, agent1_starting_uncertainty, agent2_starting_opinion, agent2_starting_uncertainty):
    # both agents want to vote and have a high uncertainty
    if agent1_starting_opinion == 1 and agent1_starting_uncertainty > 0.5 and agent2_starting_opinion == 1 and agent2_starting_uncertainty > 0.5:
        agent1_updated_opinion = agent1_starting_opinion
        agent1_updated_uncertainty = agent1_starting_uncertainty - 0.1

        agent2_updated_opinion = agent2_starting_opinion
        agent2_updated_uncertainty = agent2_starting_uncertainty - 0.1
        return agent1_updated_opinion, agent1_updated_uncertainty, agent2_updated_opinion, agent2_updated_uncertainty
    # both agents don't want to vote and have a low uncertainty
    elif agent1_starting_opinion == 0 and agent1_starting_uncertainty < 0.5 and agent2_starting_opinion == 0 and agent2_starting_uncertainty < 0.5:
        agent1_updated_opinion = agent1_starting_opinion
        agent1_updated_uncertainty = agent1_starting_uncertainty + 0.1

        agent2_updated_opinion = agent2_starting_opinion
        agent2_updated_uncertainty = agent2_starting_uncertainty + 0.1
        return agent1_updated_opinion, agent1_updated_uncertainty, agent2_updated_opinion, agent2_updated_uncertainty
    # agent 1 wants to vote but agent 2 does not, if the agent1's uncertainty is greater than agent2's uncertainty,
    # then update the uncertainty
    # else, just update the opinion
    elif agent1_starting_opinion == 1 and agent1_starting_uncertainty > 0.5 and agent2_starting_opinion == 0 and agent2_starting_uncertainty > 0.5:
        if agent1_starting_uncertainty > agent2_starting_uncertainty:
            agent1_updated_opinion = agent1_starting_opinion
            agent1_updated_uncertainty = agent1_starting_uncertainty + 0.1

            agent2_updated_opinion = agent1_updated_opinion
            agent2_updated_uncertainty = agent2_starting_uncertainty + 0.1
            return agent1_updated_opinion, agent1_updated_uncertainty, agent2_updated_opinion, agent2_updated_uncertainty

        else:
            agent1_updated_opinion = agent1_starting_opinion
            agent1_updated_uncertainty = agent1_starting_uncertainty

            agent2_updated_opinion = agent1_updated_opinion
            agent2_updated_uncertainty = agent2_starting_uncertainty
            return agent1_updated_opinion, agent1_updated_uncertainty, agent2_updated_opinion, agent2_updated_uncertainty
    # if the agents do not meet any of the conditions, return the original values
    else:
        return agent1_starting_opinion, agent1_starting_uncertainty, agent2_starting_opinion, agent2_starting_uncertainty

def blue_round(green_team, blue_team, grey_team, energy, lifeline):
    # 80% of the nodes in green team
    energy_max = 20
    blue_msgs = ["lvl1 potency", "lvl2 potency", "lvl3 potency", "lvl4 potency", "lvl5 potency"]
    # if blue team uses all of its energy, the game ends
    random_msg = random.choice(blue_msgs)

    if energy >= energy_max:
        print("implement special grey round")
        random_choice = choice(list(grey_team.nodes()))
        if grey_team.nodes[random_choice]["allegiance"] == "bad":
            lifeline = True
            # energy = 0
            print("grey agent is spy")
            # implement a special grey-red interaction round
            grey_good_round(green_team)
        elif grey_team.nodes[random_choice]["allegiance"] == "good":
            lifeline = True
            energy = 0
            print("blue team has another round")
            #implement a special grey-good interaction round
            grey_good_round(green_team)


    for node in green_team.nodes():
        # randomly pick a potent message - TESTING
        random_msg = random.choice(blue_msgs)

        # message is not potent enough to have an affect
        if random_msg == "lvl1 potency":
            energy = energy
        elif random_msg == "lvl2 potency":
            energy = energy
        elif random_msg == "lvl3 potency" and green_team.nodes[node]["opinion"] == 1 and green_team.nodes[node]["uncertainty"] > 0.5:
            chance = random.choice([0, 1])
            if chance == 1:
                nx.set_node_attributes(green_team, {node: "blue"}, name="following")
                energy + 1
        # highly potent message and agent wants to vote
        elif random_msg == "lvl4 potency" and green_team.nodes[node]["opinion"] == 1 and green_team.nodes[node]["uncertainty"] > 0.5:
            nx.set_node_attributes(green_team, {node: "blue"}, name="following")
            energy = energy + 2
        elif random_msg == "lvl5 potency" and green_team.nodes[node]["opinion"] == 1 and green_team.nodes[node]["uncertainty"] > 0.5:
            nx.set_node_attributes(green_team, {node: "blue"}, name="following")
            energy = energy + 3

    save_green(green_team)
    save_energy(energy)

# grey agent is working for the team
def grey_good_round(green_team):
    blue_msgs = ["lvl1 potency", "lvl2 potency", "lvl3 potency", "lvl4 potency", "lvl5 potency"]
    for node in green_team.nodes():
        # randomly pick a potent message - TESTING
        random_msg = random.choice(blue_msgs)

        # message is not potent enough to have an affect
        if random_msg == "lvl1 potency":
            print("")
        elif random_msg == "lvl2 potency":
            print("")
        elif random_msg == "lvl3 potency" and green_team.nodes[node]["opinion"] == 1 and green_team.nodes[node]["uncertainty"] > 0.5:
            chance = random.choice([0, 1])
            if chance == 1:
                nx.set_node_attributes(green_team, {node: "blue"}, name="following")
        # highly potent message and agent wants to vote
        elif random_msg == "lvl4 potency" and green_team.nodes[node]["opinion"] == 1 and green_team.nodes[node]["uncertainty"] > 0.5:
            nx.set_node_attributes(green_team, {node: "blue"}, name="following")

        elif random_msg == "lvl5 potency" and green_team.nodes[node]["opinion"] == 1 and green_team.nodes[node]["uncertainty"] > 0.5:
            nx.set_node_attributes(green_team, {node: "blue"}, name="following")

    save_green(green_team)

# grey agent is working for the red team
def grey_bad_round(green_team):
    red_msgs = ["lvl1 potency", "lvl2 potency", "lvl3 potency", "lvl4 potency", "lvl5 potency"]
    for node in green_team.nodes():
        # player_message = red_message_selection(red_msgs)

        # randomly pick a potent message - TESTING
        current_redmsg = random.choice(red_msgs)

        # message is not potent enough to have an affect
        if current_redmsg == "lvl1 potency":
            break
        elif current_redmsg == "lvl2 potency":
            break
        elif current_redmsg == "lvl3 potency" and green_team.nodes[node]["opinion"] == 1:
            chance = random.choice([0, 1])
            if chance == 1:
                nx.set_node_attributes(green_team, {node: "red"}, name="following")
        # highly potent message and agent wants to vote
        elif current_redmsg == "lvl4 potency" and green_team.nodes[node]["opinion"] == 1:
            nx.set_node_attributes(green_team, {node: "red"}, name="following")
            red_skip = True
        elif current_redmsg == "lvl5 potency" and green_team.nodes[node]["opinion"] == 1:
            nx.set_node_attributes(green_team, {node: "red"}, name="following")
            red_skip = True

    save_green(green_team)

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
        print("red team wins!")
        print("red followers: ", red)
        print("blue followers: ", blue)
    elif blue > red:
        print("blue team wins!")
        print("red followers: ", red)
        print("blue followers: ", blue)
    elif red == blue:
        print("it's a tie!")
        print("red followers: ", red)
        print("blue followers: ", blue)



