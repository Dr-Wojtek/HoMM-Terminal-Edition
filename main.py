import random
from entities import Player
from entities import Gameboard
import os
import time

class Gamecore:
    map_size = "large"
    num_rows = 26
    num_cols = 38
    player_one = None
    player_two = None
    player_three = None
    player_four = None
    available_kingdoms = ["Castle", "Inferno"]

    def clear_window():
        os.system('cls' if os.name == 'nt' else 'clear')

    def dialogue_display(input1 = "", input2 = "", input3 = "", input4 = ""):
        print("" + '{:-^100s}'.format(""))
        print("|" + '{:^100s}'.format(input1 + input2) + "|")
        print("|" + '{:^100s}'.format(input3) + "|")
        print("" + '{:-^100s}'.format(""))

    def dialogue_return(input1 = "", input2 = "", input3 = "", input4 = ""):
        print("" +'{:-^100s}'.format("-"))
        print("|" + '{:^100s}'.format(input1 + input2) + "|")
        print("|" + '{:^100s}'.format(input3) + "|")
        print("" + '{:-^100s}'.format("-"))
        choice = input("\n")
        return choice

    def print_start():
        choice = input("Is this your first time playing Heroes of Might and Magic - Terminal Edition? Y/N\n").capitalize()
        if choice == "Y":
            print("Maximize this window until you've seen the map. Then adjust accordingly.\n")
            input("Press Enter to continue.\n")
            Gamecore.clear_window()

# GAME START
    dialogue_display("Welcome to Heroes of Might and Magic - Terminal Edition!")
    number_of_players = dialogue_return("How many human players?", "", "2-4:")
    while number_of_players not in ("2", "3", "4"):
        number_of_players = dialogue_return("Choose the number of players by typing 2, 3 or 4:")
    number_of_players = int(number_of_players)
    list_of_players = []

    for i in range(number_of_players):
        p = None
        if i == 0:
            p = Player(dialogue_return("Player 1: What is your name?").capitalize(), 1, "\033[1;31;40m")
        elif i == 1:
            p = Player(dialogue_return("Player 2: And what is your name?").capitalize(), 2, "\033[1;34;40m")
        elif i == 2:
            p = Player(dialogue_return("Player 3: And you?").capitalize(), 3)
        elif i == 3:
            p = Player(dialogue_return("Player 4: Always last eh?").capitalize(), 4)
        list_of_players.append(p)

    clear_window()

    map = Gameboard(num_rows, num_cols)
    map.beautifier(num_rows, num_cols)

    for i in range(number_of_players):
        list_of_players[i].choose_kingdom(available_kingdoms)
        list_of_players[i].create_heroes()
        list_of_players[i].heroes[0].create_starting_army()
        list_of_players[i].create_castles()
        list_of_players[i].set_locations(number_of_players, num_rows, num_cols, map)
        list_of_players[i].update_discovery(map)

    map.populator(num_rows, num_cols, number_of_players)

    while len(list_of_players) > 1:
        for i in range(len(list_of_players)):
            player = list_of_players[i]
            clear_window()
            dialogue_return(player.name, "'s turn!", "Press Enter.")
            player.new_turn()
            map.view_board(player)
            choice = dialogue_return("What do you want to do?", "", "")
            player.interpretor(choice, map, list_of_players)

            # TURN ENDS NOW
    dialogue_display(list_of_players[0].name, " has won the game!!!")

