from teams import create_teams
from game import start_game

def simulation1():
   print("simulation1------------")
   i = 0
   red_wins = 0
   blue_wins = 0
   ties = 0
   game_rounds = 0
   while i < 100:
      i = i + 1
      game_network, green_team, red_team, blue_team, grey_team = create_teams()
      red_win, blue_win, tie, game_round = start_game(game_network, green_team, red_team, blue_team, grey_team)

      red_wins = red_wins + red_win
      blue_wins = blue_wins + blue_win
      ties = ties + tie
      game_rounds = game_rounds + game_round

   print("after", i,"simulations:")
   print("total red wins: ", red_wins)
   print("total blue wins: ", blue_wins)
   print("total ties: ", ties)
   print("total game rounds: ", game_rounds)


if __name__ == '__main__':
   # game_network, green_team, red_team, blue_team, grey_team = create_teams()

   # start_game(game_network, green_team, red_team, blue_team, grey_team)
   simulation1()