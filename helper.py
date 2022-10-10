import networkx as nx

green_team = nx.Graph()
energy = 0

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
