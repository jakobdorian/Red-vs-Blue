from teams import create_teams
from election import start_election


def game_start():
    while True:
        try:
            print("The election is about to begin!")
            print("1. Simulation 1 - red agent vs random blue agent")
            print("2. Simulation 2 - blue agent vs random red agent")
            print("3. Simulation 3 - red agent vs blue agent")
            print("4. Simulation 4 - player (blue) vs red agent")
            print("5. Simulation 5 - player (red) vs blue agent")
            print("6. Quit")
            selection = int(input("Select an option:"))
        except ValueError:
            print("Invalid input!")
        if selection < 1 or selection > 6:
            print("Invalid value!")
        else:
            break

    if selection == 1:
        print("Simulation 1 - red agent vs random blue agent")
        simulation_1()
    elif selection == 2:
        print("Simulation 2 - blue agent vs random red agent")
        simulation_2()
    elif selection == 3:
        print("Simulation 3 - red agent vs blue agent")
        simulation_3()
    elif selection == 4:
        print("Simulation 4 - player (blue) vs red agent")
        simulation_4()
    elif selection == 5:
        print("Simulation 5 - player (red) vs blue agent")
        simulation_5()
    elif selection == 6:
        print("Exiting game...")
        quit()

def simulation_1():
    player = 1

    game_network, green_team, red_team, blue_team, grey_team, interval = create_teams()
    start_election(game_network, green_team, red_team, blue_team, grey_team, interval, player)

def simulation_2():
    player = 2

    game_network, green_team, red_team, blue_team, grey_team, interval = create_teams()
    start_election(game_network, green_team, red_team, blue_team, grey_team, interval, player)

def simulation_3():
    player = 3

    game_network, green_team, red_team, blue_team, grey_team, interval = create_teams()
    start_election(game_network, green_team, red_team, blue_team, grey_team, interval, player)

def simulation_4():
    player = 4

    game_network, green_team, red_team, blue_team, grey_team, interval = create_teams()
    start_election(game_network, green_team, red_team, blue_team, grey_team, interval, player)

def simulation_5():
    player = 5

    game_network, green_team, red_team, blue_team, grey_team, interval = create_teams()
    start_election(game_network, green_team, red_team, blue_team, grey_team, interval, player)

def simulation_6():
    player = 6

    game_network, green_team, red_team, blue_team, grey_team, interval = create_teams()
    start_election(game_network, green_team, red_team, blue_team, grey_team, interval, player)


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
        game_network, green_team, red_team, blue_team, grey_team, interval = create_teams()
        red_win, blue_win, tie, game_round = start_election(game_network, green_team, red_team, blue_team, grey_team, interval)

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
    game_start()
