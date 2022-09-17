from agents import create_agents
from game import start_game

print("main is running")

if __name__ == '__main__':
   game_network = create_agents()
   start_game(game_network)