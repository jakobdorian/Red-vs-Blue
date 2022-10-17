# CITS3001 Project by Jakob Kuriata (23278189)
import networkx as nx
import matplotlib.pyplot as plt
import random
from random import choice, sample
from helper import save_green, get_green, save_energy, get_energy, clear_energy, save_lifeline, get_lifeline, save_network, get_network, save_interval, get_interval, get_red_messages, get_blue_messages, get_player, save_player
import copy
import time

RED_NODE = 26
BLUE_NODE = 27
minimax_sim = False
def start_election(network, green_team, red_team, blue_team, grey_team, uncertainty_interval, player):
    print("\n")
    print("Election is starting...")
    lifeline = False
    clear_energy()
    save_player(player)

    save_green(green_team)

    save_lifeline(lifeline)
    save_network(network)
    save_interval(uncertainty_interval)
    rounds = 0

    temp_interval = uncertainty_interval.mid

    red_msgs = get_red_messages()
    blue_msgs = get_blue_messages()
    # check_voters()
    # visualize_game(network)

    while True:
        if player == 1 or player == 2 or player == 3 or player == 4 or player == 5:
            time.sleep(0.3)

        green = get_green()
        # round where all green agents interact with each of their neighbours, potentially changing their opinions and uncertainty
        green_round(green)
        rounds = rounds + 1
        green = get_green()
        red_round(green, red_msgs, temp_interval, minimax_sim)
        rounds = rounds + 1
        green = get_green()

        # round where the blue agent interacts with all members of the green team, potentially affecting their opinions
        # the goal of the blue agent is to convince those who are following the red team to follow them instead
        # blue team cannot lose followers
        # each time the blue agent interacts with an agent with a high certainty (0.7 to 1) they lose more energy
        # the blue agent can either lose energy or none at all during a round
        # if the blue agent does run out of energy, they can introduce a grey agent (blue round with no energy cost)
        # however there may be a chance that the grey agent is a spy, which gives the red agent a free round during blue teams round
        # blue_round(green, blue_team, grey_team, blue_energy)
        blue_round(green, blue_msgs, temp_interval, minimax_sim)
        rounds = rounds + 1

        current_energy = get_energy()

        green = get_green()
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
                grey_bad_round(green_team, red_msgs, random_choice, temp_interval, minimax_sim)
            elif grey_team.nodes[random_choice]["allegiance"] == "good":
                # lifeline = True
                energy = 0
                print("blue team has another round, thanks to grey team")
                grey_good_round(green_team, blue_msgs, random_choice, temp_interval, minimax_sim)
        elif current_energy >= 100 and lifeline == True:
            if player == 6 or player == 7 or player == 8:
                red_wins, blue_wins, ties, game_rounds = get_result(green, rounds)
                return red_wins, blue_wins, ties, game_rounds
            else:
                game_result(green, rounds)
                clear_energy()
                network = get_network()
                visualize_game(network)
                quit()
            # test scenarios
            if player == 6 or player == 7 or player == 8:
                red_wins, blue_wins, ties, game_rounds = get_result(green, rounds)
                return red_wins, blue_wins, ties, game_rounds

def green_round(green_team):
    for node in green_team.nodes():
        temp = list(green_team.neighbors(node))
        # randomly pick a neighbour to interact with
        temp2 = random.choice(temp)
        agent1_updated_opinion, agent1_updated_uncertainty, agent2_updated_opinion, agent2_updated_uncertainty = green_interaction(green_team, node, temp2)


        # set the updated values to agent1
        nx.set_node_attributes(green_team, {node: agent1_updated_opinion}, name="opinion")
        nx.set_node_attributes(green_team, {node: agent1_updated_uncertainty}, name="uncertainty")
        # set the updated values to agent2
        nx.set_node_attributes(green_team, {temp2: agent2_updated_opinion}, name="opinion")
        nx.set_node_attributes(green_team, {temp2: agent2_updated_uncertainty}, name="uncertainty")

    # return green_team
    save_green(green_team)

def red_message_selection():
    red_messages = get_red_messages()
    while True:
        try:
            print("1. lvl1 potency msg")
            print("2. lvl2 potency msg")
            print("3. lvl3 potency msg")
            print("4. lvl4 potency msg")
            print("5. lvl5 potency msg")
            selection = int(input("Pick a message to send to the green node: "))
        except ValueError:
            print("Invalid input!")
        if selection < 1 or selection > 5:
            print("Invalid option!")
        else:
            break
    if selection == 1:
        player_message = red_messages[0]
    elif selection == 2:
        player_message = red_messages[1]
    elif selection == 3:
        player_message = red_messages[2]
    elif selection == 4:
        player_message = red_messages[3]
    elif selection == 5:
        player_message = red_messages[4]

    return player_message

def red_uncertainty_selection():
    interval = get_interval()
    while True:
        try:
            print("Please input an uncertainty value based on: ", interval)
            player_uncertainty = float(input("Please input an uncertainty value based on: "))
        except ValueError:
            print("Invalid input!")
        if player_uncertainty < interval.left or player_uncertainty > interval.right:
            print("Invalid value!")
            print("Please input a value between ", interval)
        else:
            break
    return player_uncertainty
def blue_message_selection():
    blue_messages = get_blue_messages()
    while True:
        try:
            print("1. lvl1 potency msg")
            print("2. lvl2 potency msg")
            print("3. lvl3 potency msg")
            print("4. lvl4 potency msg")
            print("5. lvl5 potency msg")
            selection = int(input("Pick a message to send to the green node: "))
        except ValueError:
            print("Invalid input!")
        if selection < 1 or selection > 5:
            print("Invalid option!")
        else:
            break
    if selection == 1:
        player_message = blue_messages[0]
    elif selection == 2:
        player_message = blue_messages[1]
    elif selection == 3:
        player_message = blue_messages[2]
    elif selection == 4:
        player_message = blue_messages[3]
    elif selection == 5:
        player_message = blue_messages[4]

    return player_message

def blue_uncertainty_selection():
    interval = get_interval()
    while True:
        try:
            print("Please input an uncertainty value based on: ", interval)
            player_uncertainty = float(input("Please input an uncertainty value based on: "))
        except ValueError:
            print("Invalid input!")
        if player_uncertainty < interval.left or player_uncertainty > interval.right:
            print("Invalid value!")
            print("Please input a value between ", interval)
        else:
            break
    return player_uncertainty

def red_round(green_team, red_msg, red_uncertainty, minimax_sim):
    red_skip = False
    network = get_network()
    player = get_player()
    red_messages = get_red_messages()
    interval = get_interval()
    highly_potent = 0
    energy = get_energy()
    # randomly pick a potent message - TESTING
    # random_msg = random.choice(red_messages)

    # red_msg = minimax(green_team, True, -float("inf"), float("inf"), 10)
    if not minimax_sim:
        # red agent
        if player == 1:
            chosen_msg, chosen_uncertainty = minimax_redvsblue(green_team, True)
            red_msg = chosen_msg
            red_uncertainty = chosen_uncertainty
        # random red agent
        elif player == 2:
            red_msg = random.choice(red_messages)
            red_uncertainty = round(random.uniform(interval.left, interval.right), 1)
        # red agent
        elif player == 3:
            chosen_msg, chosen_uncertainty = minimax_redvsblue(green_team, True)
            red_msg = chosen_msg
            red_uncertainty = chosen_uncertainty
        # red agent
        elif player == 4:
            chosen_msg, chosen_uncertainty = minimax_redvsblue(green_team, True)
            red_msg = chosen_msg
            red_uncertainty = chosen_uncertainty
        # human player
        elif player == 5:
            red_msg = red_message_selection()
            red_uncertainty = red_uncertainty_selection()
        elif player == 6:
            chosen_msg, chosen_uncertainty = minimax_redvsblue(green_team, True)
            red_msg = chosen_msg
            red_uncertainty = chosen_uncertainty
        elif player == 7:
            red_msg = random.choice(red_messages)
            red_uncertainty = round(random.uniform(interval.left, interval.right), 1)
        elif player == 8:
            chosen_msg, chosen_uncertainty = minimax_redvsblue(green_team, True)
            red_msg = chosen_msg
            red_uncertainty = chosen_uncertainty

    interval = get_interval()
    followers = 0

    for node in green_team.nodes():
        # time.sleep(1)
        if not minimax_sim:
            print("current energy: ", energy, "/ 100")
            print("red agent -> ", red_msg, "-> green node #", node)
            print("current uncertainty: ", red_uncertainty)
            print("----------------------------------")

        a1_opinion, a1_uncertainty = red_interaction(green_team, node, red_uncertainty)

        # update new values
        nx.set_node_attributes(green_team, {node: a1_opinion}, name="opinion")
        nx.set_node_attributes(green_team, {node: a1_uncertainty}, name="uncertainty")
        # time.sleep(0.5)

        # node wants to vote
        if green_team.nodes[node]["opinion"] == 1:
            # node is certain
            if green_team.nodes[node]["uncertainty"] < interval.mid:
                if red_msg == "lvl1 potency":
                    chance = random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
                    if chance == 1:
                            nx.set_node_attributes(green_team, {node: "red"}, name="following")
                            network.add_edge(node, RED_NODE)
                            followers = followers + 1
                elif red_msg == "lvl2 potency":
                    chance = random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8])
                    if chance == 1:
                        nx.set_node_attributes(green_team, {node: "red"}, name="following")
                        network.add_edge(node, RED_NODE)
                        followers = followers + 1
                elif red_msg == "lvl3 potency":
                    chance = random.choice([0, 1, 2, 3, 4, 5])
                    if chance == 1 or chance == 3:
                        nx.set_node_attributes(green_team, {node: "red"}, name="following")
                        network.add_edge(node, RED_NODE)
                        followers = followers + 1
                    elif chance == 0:
                        nx.set_node_attributes(green_team, {node: "blue"}, name="following")
                        network.add_edge(node, RED_NODE)
                        followers = followers + 1
                elif red_msg == "lvl4 potency":
                    # red team loses followers
                    chance = random.choice([0, 1, 2, 3])
                    if chance == 1:
                        nx.set_node_attributes(green_team, {node: "red"}, name="following")
                        nx.set_node_attributes(green_team, {node: 0}, name="opinion")
                        network.add_edge(node, RED_NODE)
                        followers = followers + 1
                    # red team loses followers
                    elif chance == 0:
                        nx.set_node_attributes(green_team, {node: "blue"}, name="following")
                        nx.set_node_attributes(green_team, {node: 0}, name="opinion")
                        network.add_edge(node, RED_NODE)
                        followers = followers + 1
                        # print("red team has lost ", node, " as a follower!")
                elif red_msg == "lvl5 potency":
                    chance = random.choice([0, 1, 3, 4])
                    if chance == 1 and highly_potent <= 2 or chance == 5 and highly_potent <= 2:
                        # if green_team.nodes[node]["following"] != "blue":
                        nx.set_node_attributes(green_team, {node: "red"}, name="following")
                        nx.set_node_attributes(green_team, {node: 0}, name="opinion")
                        network.add_edge(node, RED_NODE)
                        followers = followers + 1
                        highly_potent = highly_potent + 1
                    elif chance == 0 and highly_potent <= 2:
                        # if green_team.nodes[node]["following"] != "blue":
                        nx.set_node_attributes(green_team, {node: "blue"}, name="following")
                        nx.set_node_attributes(green_team, {node: 0}, name="opinion")
                        network.add_edge(node, BLUE_NODE)
                        followers = followers - 1
                        # print("red team has lost ", node, " as a follower!")
            # node is uncertain
            elif green_team.nodes[node]["uncertainty"] > interval.mid:
                if red_msg == "lvl1 potency":
                    chance = random.choice([0, 1, 2, 3])
                    if chance == 1:
                        # if green_team.nodes[node]["following"] != "blue":
                        nx.set_node_attributes(green_team, {node: "red"}, name="following")
                        network.add_edge(node, RED_NODE)
                        followers = followers + 1
                elif red_msg == "lvl2 potency":
                    chance = random.choice([0, 1, 2])
                    if chance == 1:
                        # if green_team.nodes[node]["following"] != "blue":
                        nx.set_node_attributes(green_team, {node: "red"}, name="following")
                        network.add_edge(node, RED_NODE)
                        followers = followers + 1
                elif red_msg == "lvl3 potency":
                    chance = random.choice([0, 1])
                    if chance == 1:
                        # if green_team.nodes[node]["following"] != "blue":
                        nx.set_node_attributes(green_team, {node: "red"}, name="following")
                        network.add_edge(node, RED_NODE)
                        followers = followers + 1
                elif red_msg == "lvl4 potency":
                    # if green_team.nodes[node]["following"] != "blue":
                    chance = random.choice([0, 1, 2])
                    if chance == 1:
                        nx.set_node_attributes(green_team, {node: "red"}, name="following")
                        network.add_edge(node, RED_NODE)
                        nx.set_node_attributes(green_team, {node: 0}, name="opinion")
                        followers = followers + 1
                elif red_msg == "lvl5 potency":
                    chance = random.choice([0, 1, 2, 3])
                    # if green_team.nodes[node]["following"] != "blue":
                    # message is highly potent but node still follows red
                    if chance == 1 and highly_potent <= 2 or chance == 4 and highly_potent <= 2:
                        nx.set_node_attributes(green_team, {node: "red"}, name="following")
                        nx.set_node_attributes(green_team, {node: 0}, name="opinion")
                        network.add_edge(node, RED_NODE)
                        followers = followers + 1
                    # message is highly potent and has led to node to follow blue instead
                    elif chance == 0 and highly_potent <= 2:
                        nx.set_node_attributes(green_team, {node: "blue"}, name="following")
                        nx.set_node_attributes(green_team, {node: 0}, name="opinion")
                        network.add_edge(node, BLUE_NODE)
                        followers = followers - 1

    if not minimax_sim:
        save_green(green_team)
        save_network(network)

    return followers

def red_interaction(green_team, node1, red_starting_uncertainty):
    agent1_starting_opinion = green_team.nodes[node1]["opinion"]
    agent1_starting_uncertainty = green_team.nodes[node1]["uncertainty"]
    # TESTING - random choices
    # LET RED AGENT DECIDE THESE VALUES
    red_starting_opinion = random.choice([0, 1])
    # red_starting_uncertainty = round(random.uniform(-1.0, 1.0), 1)
    # red_starting_uncertainty = round(random.uniform(0.0, 1.0), 1)

    agent1_updated_opinion, agent1_updated_uncertainty, red_updated_opinion, red_updated_uncertainty = update_rules(agent1_starting_opinion, agent1_starting_uncertainty, red_starting_opinion, red_starting_uncertainty)

    return agent1_updated_opinion, agent1_updated_uncertainty

def blue_interaction(green_team, node1, blue_starting_uncertainty):
    agent1_starting_opinion = green_team.nodes[node1]["opinion"]
    agent1_starting_uncertainty = green_team.nodes[node1]["uncertainty"]
    # interval = get_interval()
    # TESTING - random choices
    # LET BLUE AGENT DECIDE THESE VALUES
    blue_starting_opinion = random.choice([0, 1])
    # blue_starting_uncertainty = round(random.uniform(interval.left, interval.right), 1)

    agent1_updated_opinion, agent1_updated_uncertainty, blue_updated_opinion, blue_updated_uncertainty = update_rules(agent1_starting_opinion, agent1_starting_uncertainty, blue_starting_opinion, blue_starting_uncertainty)

    return agent1_updated_opinion, agent1_updated_uncertainty
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
        agent1_updated_uncertainty = interval.left

        agent2_updated_opinion = agent2_starting_opinion
        agent2_updated_uncertainty = interval.left

        return agent1_updated_opinion, agent1_updated_uncertainty, agent2_updated_opinion, agent2_updated_uncertainty
    # both agents don't want to vote and have a low uncertainty
    elif agent1_starting_opinion == 0 and agent1_starting_uncertainty < interval.mid and agent2_starting_opinion == 0 and agent2_starting_uncertainty < interval.mid:
        # print("2. both agents do not want to vote and are certain of their current vote")
        agent1_updated_opinion = agent1_starting_opinion
        agent1_updated_uncertainty = interval.right

        agent2_updated_opinion = agent2_starting_opinion
        agent2_updated_uncertainty = interval.right

        return agent1_updated_opinion, agent1_updated_uncertainty, agent2_updated_opinion, agent2_updated_uncertainty
    # agent 1 wants to vote but agent 2 does not, if the agent1's uncertainty is greater than agent2's uncertainty,
    # then update the uncertainty
    # else, just update the opinion
    elif agent1_starting_opinion == 1 and agent1_starting_uncertainty > interval.mid and agent2_starting_opinion == 0 and agent2_starting_uncertainty > interval.mid:
        if agent1_starting_uncertainty > agent2_starting_uncertainty:
            # print("3. agent1 convinces agent2 to vote")
            agent1_updated_opinion = agent1_starting_opinion
            agent1_updated_uncertainty = interval.right

            agent2_updated_opinion = agent1_updated_opinion
            agent2_updated_uncertainty = interval.right

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
        agent1_updated_uncertainty = interval.right

        agent2_updated_opinion = agent2_starting_opinion
        agent2_updated_uncertainty = interval.right

        return agent1_updated_opinion, agent1_updated_uncertainty, agent2_updated_opinion, agent2_updated_uncertainty
    # both agents are highly uncertain and now want to vote
    elif agent1_starting_opinion == 0 and agent1_starting_uncertainty > interval.mid and agent2_starting_opinion == 0 and agent2_starting_uncertainty > interval.mid:
        # print("5. both agents are highly uncertain and now want to vote")
        agent1_updated_opinion = 1
        agent1_updated_uncertainty = interval.left

        agent2_updated_opinion = 1
        agent2_updated_uncertainty = interval.left

        return agent1_updated_opinion, agent1_updated_uncertainty, agent2_updated_opinion, agent2_updated_uncertainty
    # if the agents do not meet any of the conditions, return the original values
    else:
        # print("!!!! no conditions met")
        return agent1_starting_opinion, agent1_starting_uncertainty, agent2_starting_opinion, agent2_starting_uncertainty

def blue_round(green_team, blue_msg, blue_uncertainty, minimax_sim):
    # if blue team uses all of its energy, the game ends
    network = get_network()
    player = get_player()
    interval = get_interval()
    blue_messages = get_blue_messages()
    # random_msg = random.choice(blue_messages)
    energy = get_energy()
    round_followers = 0
    # teams can only send 2 highly potent messages each round
    highly_potent = 0

    if not minimax_sim:
        # random blue agent
        if player == 1:
            blue_msg = random.choice(blue_messages)
            blue_uncertainty = round(random.uniform(interval.left, interval.right), 1)
        # blue agent
        elif player == 2:
            chosen_msg, chosen_uncertainty = minimax_redvsblue(green_team, False)
            blue_msg = chosen_msg
            blue_uncertainty = chosen_uncertainty
        # blue agent
        elif player == 3:
            chosen_msg, chosen_uncertainty = minimax_redvsblue(green_team, False)
            blue_msg = chosen_msg
            blue_uncertainty = chosen_uncertainty
        # human player
        elif player == 4:
            blue_msg = blue_message_selection()
            blue_uncertainty = blue_uncertainty_selection()
        # blue agent
        elif player == 5:
            chosen_msg, chosen_uncertainty = minimax_redvsblue(green_team, False)
            blue_msg = chosen_msg
            blue_uncertainty = chosen_uncertainty
        # random blue agent
        elif player == 6:
            blue_msg = random.choice(blue_messages)
            blue_uncertainty = round(random.uniform(interval.left, interval.right), 1)
        # blue agent
        elif player == 7:
            chosen_msg, chosen_uncertainty = minimax_redvsblue(green_team, False)
            blue_msg = chosen_msg
            blue_uncertainty = chosen_uncertainty
        # blue agent
        elif player == 8:
            chosen_msg, chosen_uncertainty = minimax_redvsblue(green_team, False)
            blue_msg = chosen_msg
            blue_uncertainty = chosen_uncertainty


    for node in green_team.nodes():
        # time.sleep(1)
        if not minimax_sim:
            print("current energy: ", energy, "/100")
            print("blue agent -> ", blue_msg, "-> green node #", node)
            print("current uncertainty: ", blue_uncertainty)
            print("----------------------------------")

        # random_msg = random.choice(blue_msgs)
        a1_opinion, a1_uncertainty = blue_interaction(green_team, node, blue_uncertainty)

        nx.set_node_attributes(green_team, {node: a1_opinion}, name="opinion")
        nx.set_node_attributes(green_team, {node: a1_uncertainty}, name="uncertainty")

        # node wants to vote
        if green_team.nodes[node]["opinion"] == 1:
            # node is certain
            if green_team.nodes[node]["uncertainty"] < interval.mid:
                energy = energy + 2
                if blue_msg == "lvl1 potency":
                    chance = random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
                    if chance == 1:
                        nx.set_node_attributes(green_team, {node: "blue"}, name="following")
                        network.add_edge(node, BLUE_NODE)
                        round_followers = round_followers + 1
                elif blue_msg == "lvl2 potency":
                    chance = random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8])
                    if chance == 1:
                        nx.set_node_attributes(green_team, {node: "blue"}, name="following")
                        network.add_edge(node, BLUE_NODE)
                        energy = energy + 1
                        round_followers = round_followers + 1
                elif blue_msg == "lvl3 potency":
                    chance = random.choice([0, 1, 2, 3, 4, 5])
                    if chance == 1:
                        nx.set_node_attributes(green_team, {node: "blue"}, name="following")
                        network.add_edge(node, BLUE_NODE)
                        energy = energy + 2
                        round_followers = round_followers + 1
                elif blue_msg == "lvl4 potency":
                    chance = random.choice([0, 1, 2])
                    if chance == 1 and highly_potent <= 2:
                        nx.set_node_attributes(green_team, {node: "blue"}, name="following")
                        highly_potent = highly_potent + 1
                        # nx.set_node_attributes(green_team, {node: 0}, name="opinion")
                        network.add_edge(node, BLUE_NODE)
                        energy = energy + 3
                        round_followers = round_followers + 1
                elif blue_msg == "lvl5 potency":
                    chance = random.choice([0, 1, 2])
                    if chance == 1 and highly_potent <= 2:
                        nx.set_node_attributes(green_team, {node: "blue"}, name="following")
                        highly_potent = highly_potent + 1
                        # nx.set_node_attributes(green_team, {node: 0}, name="opinion")
                        network.add_edge(node, BLUE_NODE)
                        energy = energy + 5
                        round_followers = round_followers + 1
            # node is uncertain
            elif green_team.nodes[node]["uncertainty"] > interval.mid:
                energy = energy + 1
                if blue_msg == "lvl1 potency":
                    chance = random.choice([0, 1, 2, 3])
                    if chance == 1:
                        nx.set_node_attributes(green_team, {node: "blue"}, name="following")
                        network.add_edge(node, BLUE_NODE)
                        round_followers = round_followers + 1
                elif blue_msg == "lvl2 potency":
                    chance = random.choice([0, 1, 2])
                    if chance == 1:
                        nx.set_node_attributes(green_team, {node: "blue"}, name="following")
                        network.add_edge(node, BLUE_NODE)
                        round_followers = round_followers + 1
                elif blue_msg == "lvl3 potency":
                    chance = random.choice([0, 1])
                    if chance == 1:
                        nx.set_node_attributes(green_team, {node: "blue"}, name="following")
                        network.add_edge(node, BLUE_NODE)
                        round_followers = round_followers + 1
                elif blue_msg == "lvl4 potency":
                    chance = random.choice([0, 1, 2, 4, 5])
                    if chance == 1:
                        nx.set_node_attributes(green_team, {node: "blue"}, name="following")
                        nx.set_node_attributes(green_team, {node: 0}, name="opinion")
                        network.add_edge(node, BLUE_NODE)
                        energy = energy + 2
                        round_followers = round_followers + 1
                elif blue_msg == "lvl5 potency":
                    chance = random.choice([0, 1, 2, 3, 4, 5])
                    if chance == 1:
                        nx.set_node_attributes(green_team, {node: "blue"}, name="following")
                        nx.set_node_attributes(green_team, {node: 0}, name="opinion")
                        network.add_edge(node, BLUE_NODE)
                        energy = energy + 5
                        round_followers = round_followers + 1

    if not minimax_sim:
        save_green(green_team)
        save_network(network)
        save_energy(energy)

    return round_followers

# grey agent is working for the team
def grey_good_round(green_team, grey_msg, grey_node, grey_uncertainty, minimax_sim):
    network = get_network()
    interval = get_interval()
    round_followers = 0
    highly_potent = 0
    # random_msg = random.choice(blue_msgs)

    if not minimax_sim:
        chosen_msg, chosen_uncertainty = minimax_goodvsbad(green_team, True)
        grey_msg = chosen_msg
        grey_uncertainty = chosen_uncertainty

    for node in green_team.nodes():
        if not minimax_sim:
            print("grey-good agent -> ", grey_msg, "-> green node #", node)
            print("current uncertainty: ", grey_uncertainty)
            print("----------------------------------")

        # randomly pick a potent message - TESTING

        a1_opinion, a1_uncertainty = blue_interaction(green_team, node, grey_uncertainty)

        nx.set_node_attributes(green_team, {node: a1_opinion}, name="opinion")
        nx.set_node_attributes(green_team, {node: a1_uncertainty}, name="uncertainty")

        # node wants to vote
        if green_team.nodes[node]["opinion"] == 1:
            # node is certain
            if green_team.nodes[node]["uncertainty"] < interval.mid:
                if grey_msg == "lvl1 potency":
                    chance = random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
                    if chance == 1:
                        nx.set_node_attributes(green_team, {node: "blue"}, name="following")
                        network.add_edge(node, grey_node)
                        round_followers = round_followers + 1
                elif grey_msg == "lvl2 potency":
                    chance = random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8])
                    if chance == 1:
                        nx.set_node_attributes(green_team, {node: "blue"}, name="following")
                        network.add_edge(node, grey_node)
                        round_followers = round_followers + 1
                elif grey_msg == "lvl3 potency":
                    chance = random.choice([0, 1, 2, 3, 4, 5])
                    if chance == 1:
                        nx.set_node_attributes(green_team, {node: "blue"}, name="following")
                        network.add_edge(node, grey_node)
                        round_followers = round_followers + 1
                elif grey_msg == "lvl4 potency":
                    chance = random.choice([0, 1, 2])
                    if chance == 1 and highly_potent <= 2:
                        nx.set_node_attributes(green_team, {node: "blue"}, name="following")
                        highly_potent = highly_potent + 1
                        # nx.set_node_attributes(green_team, {node: 0}, name="opinion")
                        network.add_edge(node, grey_node)
                        round_followers = round_followers + 1
                elif grey_msg == "lvl5 potency":
                    chance = random.choice([0, 1, 2])
                    if chance == 1 and highly_potent <= 2:
                        nx.set_node_attributes(green_team, {node: "blue"}, name="following")
                        highly_potent = highly_potent + 1
                        # nx.set_node_attributes(green_team, {node: 0}, name="opinion")
                        network.add_edge(node, grey_node)
                        round_followers = round_followers + 1
            # node is uncertain
            elif green_team.nodes[node]["uncertainty"] > interval.mid:
                if grey_msg == "lvl1 potency":
                    chance = random.choice([0, 1, 2, 3])
                    if chance == 1:
                        nx.set_node_attributes(green_team, {node: "blue"}, name="following")
                        network.add_edge(node, grey_node)
                        round_followers = round_followers + 1
                elif grey_msg == "lvl2 potency":
                    chance = random.choice([0, 1, 2])
                    if chance == 1:
                        nx.set_node_attributes(green_team, {node: "blue"}, name="following")
                        network.add_edge(node, grey_node)
                        round_followers = round_followers + 1
                elif grey_msg == "lvl3 potency":
                    chance = random.choice([0, 1])
                    if chance == 1:
                        nx.set_node_attributes(green_team, {node: "blue"}, name="following")
                        network.add_edge(node, grey_node)
                        round_followers = round_followers + 1
                elif grey_msg == "lvl4 potency":
                    chance = random.choice([0, 1, 2, 4, 5])
                    if chance == 1:
                        nx.set_node_attributes(green_team, {node: "blue"}, name="following")
                        nx.set_node_attributes(green_team, {node: 0}, name="opinion")
                        network.add_edge(node, grey_node)
                        round_followers = round_followers + 1
                elif grey_msg == "lvl5 potency":
                    chance = random.choice([0, 1, 2, 3, 4, 5])
                    if chance == 1:
                        nx.set_node_attributes(green_team, {node: "blue"}, name="following")
                        nx.set_node_attributes(green_team, {node: 0}, name="opinion")
                        network.add_edge(node, grey_node)
                        round_followers = round_followers + 1
    if not minimax_sim:
        save_green(green_team)
        save_network(network)

    return round_followers

# grey agent is working for the red team
def grey_bad_round(green_team, grey_msg, grey_node, grey_uncertainty, minimax_sim):
    network = get_network()
    interval = get_interval()
    followers = 0

    if not minimax_sim:
        chosen_msg, chosen_uncertainty = minimax_goodvsbad(green_team, False)
        grey_msg = chosen_msg
        grey_uncertainty = chosen_uncertainty

    # random_msg = random.choice(red_msgs)
    for node in green_team.nodes():
        if not minimax_sim:
            print("grey-bad agent -> ", grey_msg, "-> green node #", node)
            print("current uncertainty: ", grey_uncertainty)
            print("----------------------------------")
        # player_message = red_message_selection(red_msgs)
        a1_opinion, a1_uncertainty = red_interaction(green_team, node, grey_uncertainty)
        # update new values
        nx.set_node_attributes(green_team, {node: a1_opinion}, name="opinion")
        nx.set_node_attributes(green_team, {node: a1_uncertainty}, name="uncertainty")

        # node wants to vote
        if green_team.nodes[node]["opinion"] == 1:
            # node is certain
            if green_team.nodes[node]["uncertainty"] < interval.mid:
                if grey_msg == "lvl1 potency":
                    chance = random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
                    if chance == 1:
                        nx.set_node_attributes(green_team, {node: "red"}, name="following")
                        network.add_edge(node, grey_node)
                        followers = followers + 1
                elif grey_msg == "lvl2 potency":
                    chance = random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8])
                    if chance == 1:
                        nx.set_node_attributes(green_team, {node: "red"}, name="following")
                        network.add_edge(node, grey_node)
                        followers = followers + 1
                elif grey_msg == "lvl3 potency":
                    chance = random.choice([0, 1, 2, 3, 4, 5])
                    if chance == 1:
                        nx.set_node_attributes(green_team, {node: "red"}, name="following")
                        network.add_edge(node, grey_node)
                        followers = followers + 1
                elif grey_msg == "lvl4 potency":
                    chance = random.choice([0, 1, 2, 3])
                    if chance == 1:
                        nx.set_node_attributes(green_team, {node: "red"}, name="following")
                        nx.set_node_attributes(green_team, {node: 0}, name="opinion")
                        network.add_edge(node, grey_node)
                        followers = followers + 1
                elif grey_msg == "lvl5 potency":
                    chance = random.choice([0, 1, 2, 4, 5])
                    if chance == 1:
                        nx.set_node_attributes(green_team, {node: "red"}, name="following")
                        nx.set_node_attributes(green_team, {node: 0}, name="opinion")
                        network.add_edge(node, grey_node)
                        followers = followers + 1
            # node is uncertain
            elif green_team.nodes[node]["uncertainty"] > interval.mid:
                if grey_msg == "lvl1 potency":
                    chance = random.choice([0, 1, 2, 3])
                    if chance == 1:
                        nx.set_node_attributes(green_team, {node: "red"}, name="following")
                        network.add_edge(node, grey_node)
                        followers = followers + 1
                elif grey_msg == "lvl2 potency":
                    chance = random.choice([0, 1, 2])
                    if chance == 1:
                        nx.set_node_attributes(green_team, {node: "red"}, name="following")
                        network.add_edge(node, grey_node)
                        followers = followers + 1
                elif grey_msg == "lvl3 potency":
                    chance = random.choice([0, 1])
                    if chance == 1:
                        nx.set_node_attributes(green_team, {node: "red"}, name="following")
                        network.add_edge(node, grey_node)
                        followers = followers + 1
                elif grey_msg == "lvl4 potency":
                    chance = random.choice([0, 1, 2])
                    if chance == 1:
                        nx.set_node_attributes(green_team, {node: "red"}, name="following")
                        nx.set_node_attributes(green_team, {node: 0}, name="opinion")
                        network.add_edge(node, grey_node)
                        followers = followers + 1
                elif grey_msg == "lvl5 potency":
                    chance = random.choice([0, 1, 2, 3])
                    if chance == 1 or chance == 3:
                        nx.set_node_attributes(green_team, {node: "red"}, name="following")
                        nx.set_node_attributes(green_team, {node: 0}, name="opinion")
                        network.add_edge(node, grey_node)
                        followers = followers + 1

    if not minimax_sim:
        save_green(green_team)
        save_network(network)
    return followers

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
    interval = get_interval()

    for node in green_team.nodes():
        # print(green_team.nodes[node]["following"])
        if "following" in green_team.nodes[node] and green_team.nodes[node]["uncertainty"] < interval.mid:
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

def minimax_redvsblue(network, red_agent):
    interval = get_interval()
    red_messages = get_red_messages()
    blue_messages = get_blue_messages()
    temp_network = copy.deepcopy(network)
    certain_interval = interval.left
    uncertain_interval = interval.right
    minimax_sim = True
    # red team
    if red_agent:
        messages_followers = [0] * 5
        i = 0
        for message in red_messages:
            i = i + 1
            temp = i - 1

            most_followers_certain = red_round(temp_network, message, certain_interval, minimax_sim)
            most_followers_uncertain = red_round(temp_network, message, uncertain_interval, minimax_sim)

            # print("certain:", most_followers_certain, "message :", message)
            # print("uncertain:", most_followers_uncertain, "message :", message)

            if most_followers_certain > most_followers_uncertain:
                most_followers = most_followers_certain
                best_uncertainty = certain_interval
            else:
                most_followers = most_followers_uncertain
                best_uncertainty = uncertain_interval

            temp2 = messages_followers[temp]
            temp3 = temp2 + most_followers
            messages_followers[temp] = temp3
        best_index = find_best(messages_followers)
        print(best_index)
        best_message = red_messages[best_index]
        return best_message, best_uncertainty
    # blue team
    else:
        messages_followers = [0] * 5
        i = 0
        for message in blue_messages:
            i = i + 1
            temp = i - 1

            most_followers_certain = blue_round(temp_network, message, certain_interval, minimax_sim)
            most_followers_uncertain = blue_round(temp_network, message, uncertain_interval, minimax_sim)

            if most_followers_certain > most_followers_uncertain:
                most_followers = most_followers_certain
                best_uncertainty = certain_interval
            else:
                most_followers = most_followers_uncertain
                best_uncertainty = uncertain_interval

            temp2 = messages_followers[temp]
            temp3 = temp2 + most_followers
            messages_followers[temp] = temp3

        # returns index of message with best value
        best_index = find_best(messages_followers)
        best_message = blue_messages[best_index]
        return best_message, best_uncertainty

# minimax agent for grey good vs grey bad
def minimax_goodvsbad(network, bad_agent):
    interval = get_interval()
    red_messages = get_red_messages()
    blue_messages = get_blue_messages()
    temp_network = copy.deepcopy(network)
    certain_interval = interval.left
    uncertain_interval = interval.right
    minimax_sim = True
    # red team
    if bad_agent:
        messages_followers = [0] * 5
        i = 0
        for message in red_messages:
            i = i + 1
            temp = i - 1

            most_followers_certain = red_round(temp_network, message, certain_interval, minimax_sim)
            most_followers_uncertain = red_round(temp_network, message, uncertain_interval, minimax_sim)

            # print("certain:", most_followers_certain, "message :", message)
            # print("uncertain:", most_followers_uncertain, "message :", message)

            if most_followers_certain > most_followers_uncertain:
                most_followers = most_followers_certain
                best_uncertainty = certain_interval
            else:
                most_followers = most_followers_uncertain
                best_uncertainty = uncertain_interval

            temp2 = messages_followers[temp]
            temp3 = temp2 + most_followers
            messages_followers[temp] = temp3
        best_index = find_best(messages_followers)
        best_message = red_messages[best_index]
        return best_message, best_uncertainty
    # blue team
    else:
        messages_followers = [0] * 5
        i = 0
        for message in blue_messages:
            i = i + 1
            temp = i - 1

            most_followers_certain = blue_round(temp_network, message, certain_interval, minimax_sim)
            most_followers_uncertain = blue_round(temp_network, message, uncertain_interval, minimax_sim)

            if most_followers_certain > most_followers_uncertain:
                most_followers = most_followers_certain
                best_uncertainty = certain_interval
            else:
                most_followers = most_followers_uncertain
                best_uncertainty = uncertain_interval

            temp2 = messages_followers[temp]
            temp3 = temp2 + most_followers
            messages_followers[temp] = temp3

        # returns index of message with best value
        best_index = find_best(messages_followers)
        best_message = blue_messages[best_index]
        return best_message, best_uncertainty


def find_best(message_followers):
    highest_value = max(message_followers)
    index = message_followers.index(highest_value)
    return index


