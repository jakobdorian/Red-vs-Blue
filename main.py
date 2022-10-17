from teams import create_teams, choose_interval
from election import start_election

def game_start():
    uncertainty_interval = choose_interval()

    while True:
        try:
            print("\n")
            print("The election is about to begin!")
            print("1. Scenario 1 - red agent vs random blue agent")
            print("2. Scenario 2 - blue agent vs random red agent")
            print("3. Scenario 3 - red agent vs blue agent")
            print("4. Scenario 4 - player (blue) vs red agent")
            print("5. Scenario 5 - player (red) vs blue agent")
            print("6. Test 1 - red agent vs random blue agent (100 simulations)")
            print("7. Test 2 - blue agent vs random red agent (100 simulations)")
            print("8. Test 3 - red agent vs blue agent (100 simulations)")
            print("9. Quit")
            selection = int(input("Select an option:"))
        except ValueError:
            print("Invalid input!")
        if selection < 1 or selection > 9:
            print("Invalid value!")
        else:
            break

    if selection == 1:
        print("Scenario 1 - red agent vs random blue agent")
        scenario_1(uncertainty_interval)
    elif selection == 2:
        print("Scenario 2 - blue agent vs random red agent")
        scenario_2(uncertainty_interval)
    elif selection == 3:
        print("Scenario 3 - red agent vs blue agent")
        scenario_3(uncertainty_interval)
    elif selection == 4:
        print("Scenario 4 - player (blue) vs red agent")
        scenario_4(uncertainty_interval)
    elif selection == 5:
        print("Scenario 5 - player (red) vs blue agent")
        scenario_5(uncertainty_interval)
    elif selection == 6:
        print("Test 1 - red agent vs random blue agent (100 simulations)")
        test_1(uncertainty_interval)
    elif selection == 7:
        print("Test 2 - blue agent vs random red agent (100 simulations)")
        test_2(uncertainty_interval)
    elif selection == 8:
        print("Test 3 - red agent vs blue agent (100 simulations)")
        test_3(uncertainty_interval)
    elif selection == 9:
        print("Exiting game...")
        quit()

def scenario_1(uncertainty_interval):
    player = 1

    game_network, green_team, red_team, blue_team, grey_team, interval = create_teams(uncertainty_interval)
    start_election(game_network, green_team, red_team, blue_team, grey_team, interval, player)

def scenario_2(uncertainty_interval):
    player = 2

    game_network, green_team, red_team, blue_team, grey_team, interval = create_teams(uncertainty_interval)
    start_election(game_network, green_team, red_team, blue_team, grey_team, interval, player)

def scenario_3(uncertainty_interval):
    player = 3

    game_network, green_team, red_team, blue_team, grey_team, interval = create_teams(uncertainty_interval)
    start_election(game_network, green_team, red_team, blue_team, grey_team, interval, player)

def scenario_4(uncertainty_interval):
    player = 4

    game_network, green_team, red_team, blue_team, grey_team, interval = create_teams(uncertainty_interval)
    start_election(game_network, green_team, red_team, blue_team, grey_team, interval, player)

def scenario_5(uncertainty_interval):
    player = 5

    game_network, green_team, red_team, blue_team, grey_team, interval = create_teams(uncertainty_interval)
    start_election(game_network, green_team, red_team, blue_team, grey_team, interval, player)

def test_1(uncertainty_interval):
    player = 6
    i = 0
    red_wins = 0
    blue_wins = 0
    ties = 0
    game_rounds = 0
    while i < 100:
        i = i + 1
        game_network, green_team, red_team, blue_team, grey_team, interval = create_teams(uncertainty_interval)
        red_win, blue_win, tie, game_round = start_election(game_network, green_team, red_team, blue_team, grey_team, interval, player)

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
def test_2(uncertainty_interval):
    player = 7
    i = 0
    red_wins = 0
    blue_wins = 0
    ties = 0
    game_rounds = 0
    while i < 100:
        i = i + 1
        game_network, green_team, red_team, blue_team, grey_team, interval = create_teams(uncertainty_interval)
        red_win, blue_win, tie, game_round = start_election(game_network, green_team, red_team, blue_team, grey_team, interval, player)

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


def test_3(uncertainty_interval):
    player = 8
    i = 0
    red_wins = 0
    blue_wins = 0
    ties = 0
    game_rounds = 0
    while i < 100:
        i = i + 1
        game_network, green_team, red_team, blue_team, grey_team, interval = create_teams(uncertainty_interval)
        red_win, blue_win, tie, game_round = start_election(game_network, green_team, red_team, blue_team, grey_team, interval, player)

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
