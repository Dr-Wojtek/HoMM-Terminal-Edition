from entities import Player
from entities import Gameboard
import os

# This program is a hobby project. Its goal is to simulate the game 'Heroes of Might and Magic 3' in the terminal.
# The code is written by Alex Stråe, from Sweden, aka Dr-Wojtek @ GitHub. Creatures, heroes and town attributes and
# names are, where copied correctly, copied from the original game 'Heroes of Might and Magic 3'.

class Gamecore:
    map_size = "large"
    num_rows = 32
    num_cols = 38
    player_one = None
    player_two = None
    player_three = None
    player_four = None
    available_kingdoms = ["Castle", "Inferno", "Rampart", "Tower"]

    def clear_window():
        os.system('cls' if os.name == 'nt' else 'clear')

    def dialogue_display(input1="", input2="", input3="", input4=""):
        print("-" + '{:-^140s}'.format("") + "-")
        print("|" + '{:^140s}'.format(input1 + input2) + "|")
        print("|" + '{:^140s}'.format(input3 + input4) + "|")
        print("-" + '{:-^140s}'.format("") + "-")

    def dialogue_return(input1="", input2="", input3="", input4=""):
        print("-" + '{:-^140s}'.format("-") + "-")
        print("|" + '{:^140s}'.format(input1 + input2) + "|")
        print("|" + '{:^140s}'.format(input3 + input4) + "|")
        print("-" + '{:-^140s}'.format("-") + "-")
        choice = input("\n")
        return choice

    def print_start():
        choice = input("Is this your first time playing Heroes of Might and Magic - Terminal Edition? Y/N:\n").capitalize()
        if choice == "Y":
            print("\n\nIt is recommended to run this game in full screen, or at least as large as possible. When the map opens, there are two strongly coloured action bars; top and bottom.\n"
                  "Make sure both of these can be seen, they display all available commands to you. This game was developed on 1440p resolution.\n\n")
            print("If the map looks corrupted with black lines and/or you cannot see top and bottom action bars, your resolution is too low. Lower your font size in your terminal settings.\n")
            print("It is recommended to use a light grey background with black letters for your terminal / command line.\n\n")
            input("Press Enter to continue.\n")

    # GAME START
    clear_window()
    print_start()
    clear_window()
    dialogue_display("Welcome to Heroes of Might and Magic 3 - Terminal Edition!")
    number_of_players = dialogue_return("How many human players?", "", "2-4:")
    while number_of_players not in ("2", "3", "4"):
        number_of_players = dialogue_return("Choose the number of players by typing 2, 3 or 4:")
    number_of_players = int(number_of_players)
    list_of_players = []
    for i in range(number_of_players):
        p = None
        if i == 0:
            p = Player(dialogue_return("Player 1: What is your name?").capitalize(), 1, "\033[1;37;41m")
        elif i == 1:
            p = Player(dialogue_return("Player 2: And what is your name?").capitalize(), 2, "\033[1;37;44m")
        elif i == 2:
            p = Player(dialogue_return("Player 3: And you?").capitalize(), 3, "\033[1;37;42m")
        elif i == 3:
            p = Player(dialogue_return("Player 4: Yes?").capitalize(), 4, "\033[1;37;45m")
        list_of_players.append(p)
    clear_window()
    map = Gameboard(num_rows, num_cols)
    map.beautifier(num_rows, num_cols)
    for p in list_of_players:
        p.choose_kingdom(available_kingdoms)
        p.create_heroes()
        p.create_towns()
        p.set_locations(number_of_players, num_rows, num_cols, map)
        p.update_discovery(map)
    map.populator(num_rows, num_cols, number_of_players)
    while len(list_of_players) > 1:
        for p in list_of_players:
            player = p
            clear_window()
            dialogue_return(player.name, "'s turn!", "Press Enter.")
            player.new_turn()
            map.view_board(player)
            choice = dialogue_return("What do you want to do?", "", "")
            player.interpretor(choice, map, list_of_players)
    # TURN ENDS NOW
    dialogue_display(list_of_players[0].name, " has won the game!!!")
