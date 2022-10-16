from teams import create_teams
from election import start_election


def game_start():
   print("The election is about to begin!")
   print("1. Simulation 1 - red agent vs random blue agent")
   print("2. Simulation 2 - blue agent vs random red agent")
   print("3. Simulation 3 - red agent vs blue agent")
   print("4. Simulation 4 - player vs red agent")
   print("5. Simulation 5 - player vs blue agent")
   print("6. Quit")
   selection = input("Select an option:")

   if selection == 1:
      print("Simulation 1")
   elif selection == 2:
      print("sim2")
   elif selection == 3:
      print("sim3")
   elif selection == 4:
      print("sim4")
   elif selection == 5:
      print("sim5")
   elif selection == 6:
      quit("quit")
   else:
       print("invalid option!")
       print("please select an option between 1 and 6.")


# runs simulation with random choices
def simulation_random():
    print("simulation random")
    game_network, green_team, red_team, blue_team, grey_team, interval = create_teams()
    start_election(game_network, green_team, red_team, blue_team, grey_team, interval)


def simulation1():
    print("simulation1")
    i = 0
    red_wins = 0
    blue_wins = 0
    ties = 0
    game_rounds = 0
    while i < 100:
        i = i + 1
        print(i)
        game_network, green_team, red_team, blue_team, grey_team = create_teams()
        red_win, blue_win, tie, game_round = start_election(game_network, green_team, red_team, blue_team, grey_team)

        red_wins = red_wins + red_win
        blue_wins = blue_wins + blue_win
        ties = ties + tie
        game_rounds = game_rounds + game_round

    print("\n")
    print("after", i, "simulations:")
    print("total red wins: ", red_wins)
    print("total blue wins: ", blue_wins)
    print("total ties: ", ties)
    print("total game rounds: ", game_rounds)


if __name__ == '__main__':
    # game_network, green_team, red_team, blue_team, grey_team = create_teams()
    # start_game(game_network, green_team, red_team, blue_team, grey_team)
    simulation_random()
    # simulation1()
