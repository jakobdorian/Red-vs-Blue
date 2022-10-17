# CITS3001 Project by Jakob Kuriata (23278189)
import networkx as nx
import pandas as pd

green_team = nx.Graph()
energy = 0
lifeline = False
game_network = nx.Graph()
uncertainty_interval = pd.Interval(-1.0, 1.0)
player = 0
# save the current green team
def save_green(green):
    global green_team
    green_team = green.copy()
# return the current green team
def get_green():
    return green_team
# save the current energy level
def save_energy(blue_energy):
    global energy
    energy = blue_energy
# return the current energy level
def get_energy():
    return energy

def clear_energy():
    global energy
    energy = 0

def save_lifeline(current_lifeline):
    global lifeline
    lifeline = current_lifeline

def get_lifeline():
    return lifeline

def save_network(network):
    global game_network
    game_network = network.copy()

def get_network():
    return game_network

def save_interval(interval):
    global uncertainty_interval
    uncertainty_interval = interval

def get_interval():
    return uncertainty_interval

def get_red_messages():
    red_msgs = ["lvl1 potency", "lvl2 potency", "lvl3 potency", "lvl4 potency", "lvl5 potency"]
    return red_msgs

def get_blue_messages():
    blue_msgs = ["lvl1 potency", "lvl2 potency", "lvl3 potency", "lvl4 potency", "lvl5 potency"]
    return blue_msgs

def save_player(current_player):
    global player
    player = current_player

def get_player():
    return player