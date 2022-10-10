from teams import create_teams
from game import start_game

if __name__ == '__main__':
   game_network, green_team, red_team, blue_team, grey_team = create_teams()
   start_game(game_network, green_team, red_team, blue_team, grey_team)
