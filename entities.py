import random
import os
import time
import sys
from renderer import Renderer
# This program is a hobby project. Its goal is to simulate the game 'Heroes of Might and Magic 3' in the terminal.
# The code is written by Alex Stråe, from Sweden, aka Dr-Wojtek @ Git Hub. Creatures, heroes and town attributes and
# names, are, where copied correctly, copied from the original game 'Heroes of Might and Magic 3'.


class Player:
    def __init__(self, input_name, input_no, input_color):
        self.name = input_name
        self.number = input_no
        self.color = input_color
        self.hasLost = False
        self.hasWon = False
        self.heroes = []
        self.heroes_left = 0
        self.towns = []
        self.kingdom = ""
        self.hero_ticker = 0
        self.num_towns = 0
        self.gold = 4000
        self.wood = 10
        self.stone = 10
        self.crystal = 4
        self.sulfur = 4
        self.mercury = 4
        self.gems = 4
        self.dailyg = 500
        self.dailyw = 0
        self.dailys = 0
        self.dailyc = 0
        self.dailysu = 0
        self.dailym = 0
        self.dailyge = 0
        self.weekday = 0

    def __str__(self):
        return f'{self.name}'

    def clear_window():
        os.system('cls' if os.name == 'nt' else 'clear')

    def dialogue_display(self, input1="", input2="", input3="", input4=""):
        print("" +'{:-^140s}'.format("-"))
        print("|" + '{:^140s}'.format(input1 + input2) + "|")
        print("|" + '{:^140}'.format(input3 + input4) + "|")
        print("" + '{:-^140s}'.format("-"))
        input("\n")

    def dialogue_return(self, input1 = "", input2="", input3="", input4=""):
        print("" +'{:-^140s}'.format("-"))
        print("|" + '{:^140s}'.format(input1 + input2) + "|")
        print("|" + '{:^140s}'.format(input3 + input4) + "|")
        print("" + '{:-^140s}'.format("-"))
        choice = input("\n")
        return choice

    def update_life(self, change):
        self.heroes_left += change
        if self.heroes_left == 0:
            self.hasLost = True

    def new_turn(self):
        self.gold += self.dailyg
        self.wood += self.dailyw
        self.stone += self.dailys
        self.crystal += self.dailyc
        self.sulfur += self.dailysu
        self.mercury += self.dailym
        self.gems += self.dailyge
        if self.towns != []:
            for i in range(len(self.towns)):
                self.towns[i].has_built = False
        self.has_hired = False
        if self.heroes != []:
            for i in range(len(self.heroes)):
                self.heroes[i].speed_left = self.heroes[i].new_speed
        self.weekday += 1
        if self.weekday == 7:
            self.weekday = 0
            if self.towns != []:
                for i in range(len(self.towns)):
                    self.towns[i].new_week()


    def choose_kingdom(self, available_kingdoms):
        chosen_kingdom = self.dialogue_return(str(available_kingdoms),"",
                "These kingdoms are available. Choose your kingdom, ", self.name + "!").capitalize()
        while chosen_kingdom not in available_kingdoms:
            chosen_kingdom = input("Try again " + self.name + ".\n").capitalize()
        self.kingdom = chosen_kingdom
        available_kingdoms.remove(chosen_kingdom)

    def create_heroes(self, new_loc = None, map = None):
        new_hero = None
        if self.kingdom == "Castle":
            match self.hero_ticker:
                case 0:
                    new_hero = Hero("Orrin", "Knight", 2, 1, 1, 1, self)
                case 1:
                    new_hero = Hero("Adelaide", "Cleric", 1, 1, 2, 1, self)
                case 2:
                    new_hero = Hero("Tyris", "Knight", 2, 2, 0, 1, self)
        elif self.kingdom == "Inferno":
            match self.hero_ticker:
                case 0:
                    new_hero = Hero("Zydar", "Heretic", 1, 1, 2, 1, self)
                case 1:
                    new_hero = Hero("Calh", "Demoniac", 2, 2, 1, 0, self)
                case 2:
                    new_hero = Hero("Pyre", "Demoniac", 3, 0, 1, 1, self)
        elif self.kingdom == "Rampart":
            match self.hero_ticker:
                case 0:
                    new_hero = Hero("Kyrre", "Ranger", 1, 2, 1, 1, self)
                case 1:
                    new_hero = Hero("Ryland", "Ranger", 2, 1, 1, 1, self)
                case 2:
                    new_hero = Hero("Elleshar", "Druid", 1, 1, 1, 2, self)
        elif self.kingdom == "Tower":
            match self.hero_ticker:
                case 0:
                    new_hero = Hero("Solmyr", "Wizard", 0, 1, 2, 2, self)
                case 1:
                    new_hero = Hero("Fafner", "Alchemist", 1, 1, 2, 1, self)
                case 2:
                    new_hero = Hero("Josephine", "Alchemist", 1, 1, 2, 1, self)

        if new_loc != None:
            new_hero.location = new_loc
            map.square[new_loc[0]][new_loc[1]].has_hero = True
            map.square[new_loc[0]][new_loc[1]].hero = new_hero
        self.heroes.append(new_hero)
        self.heroes[-1].location = new_loc
        self.hero_ticker += 1
        self.heroes_left += 1
        new_hero.create_starting_army()

    def create_towns(self):
        new_town = None
        if self.kingdom == "Castle":
            new_town = Town("Valetta", self.kingdom, self, 1, 1)
        elif self.kingdom == "Inferno":
            new_town = Town("Styx", self.kingdom, self, 1, 1)
        elif self.kingdom == "Rampart":
            new_town = Town("Goldenglade", self.kingdom, self, 1, 1)
        elif self.kingdom == "Tower":
            new_town = Town("Celeste", self.kingdom, self, 1, 1)
        self.towns.append(new_town)

    def set_locations(self, number_of_players, input_rows, input_cols, map):
        start_row = 0
        end_row = 0
        start_col = 0
        end_col = 0
        if self.number == 1:
            start_row = 4
            end_row = int(input_rows / 2 - 4)
            start_col = 4
            end_col = int(input_cols / 2 - 4)
        elif self.number == 2:
            start_row = int(input_rows / 2 + 4)
            end_row = input_rows - 4
            start_col = 4
            end_col = int(input_cols / 2 - 4)
        elif self.number == 3:
            start_row = 4
            end_row = int(input_rows / 2 - 4)
            start_col = int(input_cols / 2 + 4)
            end_col = input_cols - 4
        elif self.number == 4:
            start_row = int(input_rows / 2 + 4)
            end_row = input_rows - 4
            start_col = int(input_cols / 2 + 4)
            end_col = input_cols - 4

        if number_of_players < 3:
            end_col = input_cols - 4

        dice_row = random.randrange(start_row, end_row)
        dice_col = random.randrange(start_col, end_col)
        while map.square[dice_row][dice_col].kind == "mountain" or map.square[dice_row][dice_col].kind == "water":
            dice_row = random.randrange(start_row, end_row)
            dice_col = random.randrange(start_col, end_col)

        self.towns[0].location[0], self.towns[0].location[1] = dice_row, dice_col
        self.heroes[0].location = self.towns[0].location
        map.square[dice_row][dice_col].has_object = True
        map.square[dice_row][dice_col].object_name = "Town"
        map.square[dice_row][dice_col].town = self.towns[0]
        map.square[dice_row][dice_col].has_hero = True
        map.square[dice_row][dice_col].hero = self.heroes[0]

    def update_discovery(self, map):
        rows = len(map.square)
        cols = len(map.square[0])
        for i in range(len(self.heroes)):
            pn = int(self.heroes[i].location[0])
            pl = int(self.heroes[i].location[1])
            for c in range(-2, 3):
                for d in range(-2, 3):
                    if pn == 0 and c < 0:
                        c = 0
                    elif pn == 1 and c < 0:
                        c = -1
                    elif pn == (rows - 1) and c > 0:
                        c = 0
                    elif pn == (rows - 2) and c > 1:
                        c = 1
                    if pl == 0 and d < 0:
                        d = 0
                    elif pl == 1 and d < 0:
                        d = -1
                    elif pl == (cols - 1) and d > 0:
                        d = 0
                    elif pl == (cols - 2) and d > 1:
                        d = 1
                    map.square[pn+c][pl+d].seen[self.number-1] = 1


    def view_info(self):
        print("")
        print("" + '{:^40s}'.format("Player: " + self.name))
        for town in self.towns:
            print("|" + '{:-^40s}'.format("  " + town.name + ", Kingdom: " + town.kingdom + "  ") + "|")
            if town.army:
                for unit in town.army:
                    print("|" + '{:^40s}'.format(unit.name + ", " + str(unit.amount) + " units") + "|")
            else:
                print("|" + '{:^40s}'.format("No army.") + "|")
            print("|" + '{:-^40s}'.format("") + "|")
        for hero in self.heroes:
            print("|" + '{:-^40s}'.format("  " + hero.name + ", " + hero.kind + " level: " + str(hero.level) + "  ") + "|")
            print("|" + '{:^40}'.format("Daily movement points: " + str(hero.new_speed) + ".") + "|")
            print("|" + '{:^40}'.format("Attack: " + str(hero.attack) + "   Defense: " + str(hero.defense)) + "|")
            print("|" + '{:^40}'.format("Knowledge: " + str(hero.knowledge) + " Spell Power: " + str(hero.spell_power)) + "|")
            print("|" + '{:-^40}'.format("  Army  ") + "|")
            for unit in hero.army:
                print("|" + '{:^40s}'.format(unit.name + ", " + str(unit.amount) + " units") + "|")
            print("|" + '{:-^40s}'.format("") + "|")
        input("\n")

    def interpretor(self, choice, map, list_of_players):
        if choice.lower() == "view":
            self.view_info()

        elif choice.lower() == "move":
            if len(self.heroes) == 1:
                hero_choice = self.heroes[0].name
            else:
                hero_choice = input("Move which hero?\n")
            self.move_obj(hero_choice, map)

        elif choice.lower() == "town":
            if self.towns != []:
                if len(self.towns) > 1:
                    town_choice = input("Enter which town? Number:\n")
                    while town_choice not in ("1", "2", "3"):
                        town_choice = input("Type town to enter. 1 = First town. 2 = Second town.\n")
                    if town_choice == "1":
                        self.enter_town(self.towns[0], map)
                    elif town_choice == "2":
                        self.enter_town(self.towns[1], map)
                else:
                    self.enter_town(self.towns[0], map)
            else:
                self.dialogue_display("You have lost all your towns!")

        elif choice.lower() == "end turn":
            return

        else:
            print("Use commands listed in the action bar above the map to play the game.\n")
        for i in range(len(list_of_players)):
            if list_of_players[i].heroes_left == 0 and list_of_players[i].towns == []:
                list_of_players[i].hasLost = True
                self.dialogue_display(list_of_players[i].name, " has been defeated!")
                list_of_players.pop(i)
            if len(list_of_players) == 1:
                return
        map.view_board(self)
        choice = self.dialogue_return("What do you want to do?", "", "")
        self.interpretor(choice, map, list_of_players)

    def has_hero_name(self, input):
        for i in range(len(self.heroes)):
            if self.heroes[i].name[0:4] == input[0:4].title() and self.heroes[i].alive:
                return True

        print("Found no hero with that name.")
        time.sleep(1)
        return False

    def get_hero(self, input):
        for i in range(len(self.heroes)):
            if self.heroes[i].name[0:4] == input[0:4].title():
                return self.heroes[i]

        print("Found no hero with that name. (GET_HERO)")
        time.sleep(1)
        return ""

    def move_obj(self, input_hero, input_board):
        if self.has_hero_name(input_hero):
            hero = self.get_hero(input_hero)
            while True:
                input_board.view_board(self, True)
                direction = input("Use keys WASD to move straight, QEZX to move diagonally."
                                  "See the top action bar for other commands.\n").lower()
                if direction == "devmode":
                    hero.speed_left = 100
                    hero.new_speed = 100
                    direction = ""
                while direction == "" or direction[0] not in ("q", "w", "e", "a", "s", "d", "z", "x", "o"):
                    direction = input("     Move with QWEASDZX or type ""o"" to exit movement.\n")
                for i in range(len(direction)):
                    old_pos = hero.location
                    new_pos = [0, 0]
                    match direction[i]:
                        case "q":
                            new_pos[0] = old_pos[0] - 1
                            new_pos[1] = old_pos[1] - 1
                        case "w":
                            new_pos[0] = old_pos[0] - 1
                            new_pos[1] = old_pos[1]
                        case "e":
                            new_pos[0] = old_pos[0] - 1
                            new_pos[1] = old_pos[1] + 1
                        case "a":
                            new_pos[0] = old_pos[0]
                            new_pos[1] = old_pos[1] - 1
                        case "s":
                            new_pos[0] = old_pos[0] + 1
                            new_pos[1] = old_pos[1]
                        case "d":
                            new_pos[0] = old_pos[0]
                            new_pos[1] = old_pos[1] + 1
                        case "z":
                            new_pos[0] = old_pos[0] + 1
                            new_pos[1] = old_pos[1] - 1
                        case "x":
                            new_pos[0] = old_pos[0] + 1
                            new_pos[1] = old_pos[1] + 1
                        case "o":
                            print("Exiting.")
                            time.sleep(0.5)
                            return
                    if new_pos[0] < 0:
                        new_pos[0] = 0
                    elif new_pos[0] == len(input_board.square):
                        new_pos[0] = len(input_board.square) - 1
                    if new_pos[1] < 0:
                        new_pos[1] = 0
                    elif new_pos[1] == len(input_board.square[0]):
                        new_pos[1] = len(input_board.square[0]) - 1
                    old_loc = input_board.square[old_pos[0]][old_pos[1]]
                    new_loc = input_board.square[new_pos[0]][new_pos[1]]
                    if new_loc.speed_drain <= hero.speed_left:
                        hero.speed_left -= new_loc.speed_drain
                        if new_loc.has_hero and new_loc.hero.operating_player != self:
                            self.start_war(hero, new_loc.hero, new_loc, old_loc)
                            if hero.army:
                                for i in range(len(hero.army)):
                                    hero.army[i].location[0] -= 1
                                    hero.army[i].location[1] = 0
                            else:
                                for i in range(len(new_loc.hero.army)):
                                    new_loc.hero.army[i].location[0] -= 1
                                    new_loc.hero.army[i].location[1] = 0

                        elif new_loc.has_object and new_loc.object_name == "Town" and \
                                new_loc.town.operating_player != self:
                            if new_loc.town.army != []:
                                self.start_war(hero, new_loc.town, new_loc, old_loc)
                                if hero.army:
                                    for i in range(len(hero.army)):
                                        hero.army[i].location[0] -= 1
                                        hero.army[i].location[1] = 0
                                else:
                                    for i in range(len(new_loc.town.army)):
                                        new_loc.town.army[i].turn_left = True
                                        new_loc.town.army[i].location[0] -= 1
                                        new_loc.town.army[i].location[1] = 0
                                new_loc.town.alive = True
                            else:
                                self.towns.append(new_loc.town)
                                for i in range(len(new_loc.town.operating_player.towns)):
                                    if new_loc.town.operating_player.towns[i].name == new_loc.town.name:
                                        new_loc.town.operating_player.towns.pop(i)
                                self.towns[-1].operating_player = self
                                if self.towns[-1].hall_lvl == 4:
                                    self.towns[-1].hall_lvl = 3
                                self.dialogue_display("You have conquered a town!")
                        elif new_loc.has_object:
                            hero.confront_object(new_loc)
                            old_loc.has_hero = False
                            old_loc.hero = None
                            new_loc.has_hero = True
                            new_loc.hero = hero
                            hero.location = new_pos
                        elif new_loc.has_hero == False:
                            new_loc.has_hero = True
                            new_loc.hero = hero
                            old_loc.has_hero = False
                            old_loc.hero = None
                            hero.location = new_pos
                        self.update_discovery(input_board)

                        if hero.speed_left == 0:
                            print("You don't have enough speed to leave current location. Exiting movement now.")
                            time.sleep(0.5)
                            return
                        elif hero.alive == False:
                            self.dialogue_display("Your forces suffer a bitter defeat, and " + hero.name + " leaves your cause.")
                            return
                    else:
                        print("You don't have enough speed to leave current location. Exiting movement now.")
                        time.sleep(0.5)
                        return

    def start_war(self, attacker, defender, battle_loc, old_loc):
        battlefield = Gameboard(10, 13, False)
        for u in attacker.army:
            if u.amount > 0:
                u.location[0] = u.start_location[0] + 1
                battlefield.square[u.location[0]][0].has_hero = True
                battlefield.square[u.location[0]][0].hero = u

        for u in defender.army:
            if u.amount > 0:
                u.location[0] = u.start_location[0] + 1
                u.location[1] = 12
                battlefield.square[u.location[0]][12].has_hero = True
                battlefield.square[u.location[0]][12].hero = u

        while attacker.alive and defender.alive:
            for u in attacker.army:
                u.has_retaliated = False
            for u in defender.army:
                u.has_retaliated = False
            for i in range(7):
                if i < len(attacker.army):
                    if attacker.army[i].amount > 0:
                        attacker.army[i].speed_left = attacker.army[i].new_speed
                        attacker.operating_player.war_move_obj(attacker.army[i], defender, battlefield)
                        attacker.army[i].turn_left = False

                if i < len(defender.army):
                    if defender.army[i].amount > 0:
                        defender.army[i].speed_left = defender.army[i].new_speed
                        defender.operating_player.war_move_obj(defender.army[i], attacker, battlefield)
                        defender.army[i].turn_left = False

                counter = 0
                for u in attacker.army:
                    if u.amount <= 0:
                        counter += 1
                if counter == len(attacker.army):
                    attacker.alive = False
                    attacker.army = []
                    old_loc.has_hero = False
                    old_loc.hero = None
                    self.heroes_left -= 1
                    for unit in defender.army:
                        unit.turn_left = True
                    break
                counter = 0
                for u in defender.army:
                    if u.amount <= 0:
                        counter += 1
                if counter == len(defender.army):
                    defender.alive = False
                    battle_loc.has_hero = False
                    battle_loc.hero = None
                    if type(defender) == Hero:
                        defender.operating_player.heroes_left -= 1
                        for i in range(len(defender.operating_player.heroes)):
                            if defender.operating_player.heroes[i].name == defender.name:
                                defender.operating_player.heroes.pop(i)
                    elif type(defender) == Town:
                        defender.army = []
                        self.towns.append(defender)
                        for i in range(len(defender.operating_player.towns)):
                            if defender.operating_player.towns[i].name == battle_loc.town.name:
                                defender.operating_player.towns.pop(i)
                        self.towns[-1].operating_player = self
                        if self.towns[-1].hall_lvl == 4:
                            self.towns[-1].hall_lvl = 3
                        print("You have conquered a town!")
                    for unit in attacker.army:
                        unit.turn_left = True
                    break
        return

    def war_move_obj(self, attacker, defending_hero, battlefield):
        while True:
            battlefield.view_battlefield(self, attacker)
            choice = input("Move with QWEASDZX or use commands in the action bar.\n").lower()
            while choice == "" or choice[0] not in ("q", "w", "e", "a", "s", "d", "z", "x", "o", "r"):
                choice = input("     Move with QWEASDZX or use commands in the action bar.\n")

            if choice == "r" and attacker.isranged:
                while True:
                    choice = input("Type unit to range attack:\n").capitalize()
                    for i in range(len(defending_hero.army)):
                        if choice == defending_hero.army[i].name:
                            defender = defending_hero.army[i]
                            new_loc = battlefield.square[defender.location[0]][defender.location[1]]
                            original_health = defender.health
                            total_damage_attack = attacker.amount * attacker.damage
                            original_attack_damage = total_damage_attack
                            defender.health -= total_damage_attack
                            total_damage_attack -= original_health
                            while defender.health <= 0:
                                defender.amount -= 1
                                defender.health = original_health
                                if total_damage_attack > 0:
                                    defender.health -= total_damage_attack
                                    total_damage_attack -= original_health
                            if defender.amount < 1:
                                new_loc.has_hero = False
                                new_loc.hero = None
                            self.dialogue_display(attacker.name + " shoots " + defending_hero.army[i].name, " with " +
                                                  str(original_attack_damage) + " damage!")
                            return
                    print("         Found no unit with that name.")
                    time.sleep(1)
            elif choice == "r" and attacker.isranged == False:
                print("         This unit does not have a ranged attack!.")
                time.sleep(1)
            else:
                for i in range(len(choice)):
                    old_pos = attacker.location
                    new_pos = [0, 0]
                    match choice[i]:
                        case "q":
                            new_pos[0] = old_pos[0] - 1
                            new_pos[1] = old_pos[1] - 1
                        case "w":
                            new_pos[0] = old_pos[0] - 1
                            new_pos[1] = old_pos[1]
                        case "e":
                            new_pos[0] = old_pos[0] - 1
                            new_pos[1] = old_pos[1] + 1
                        case "a":
                            new_pos[0] = old_pos[0]
                            new_pos[1] = old_pos[1] - 1
                        case "s":
                            new_pos[0] = old_pos[0] + 1
                            new_pos[1] = old_pos[1]
                        case "d":
                            new_pos[0] = old_pos[0]
                            new_pos[1] = old_pos[1] + 1
                        case "z":
                            new_pos[0] = old_pos[0] + 1
                            new_pos[1] = old_pos[1] - 1
                        case "x":
                            new_pos[0] = old_pos[0] + 1
                            new_pos[1] = old_pos[1] + 1
                        case "o":
                            print("Ending turn.")
                            time.sleep(1)
                            return
                    if new_pos[0] < 0:
                        new_pos[0] = 0
                    elif new_pos[0] == len(battlefield.square):
                        new_pos[0] = len(battlefield.square) - 1
                    if new_pos[1] < 0:
                        new_pos[1] = 0
                    elif new_pos[1] == len(battlefield.square[0]):
                        new_pos[1] = len(battlefield.square[0]) - 1
                    old_loc = battlefield.square[old_pos[0]][old_pos[1]]
                    new_loc = battlefield.square[new_pos[0]][new_pos[1]]
                    if new_loc.speed_drain <= attacker.speed_left:
                        if new_loc.has_hero == False:
                            attacker.speed_left -= new_loc.speed_drain
                            new_loc.has_hero = True
                            new_loc.hero = attacker
                            attacker.location = new_pos
                            old_loc.has_hero = False
                            old_loc.hero = None
                            if attacker.speed_left == 0:
                                print("No more speed left. Ending turn now.")
                                time.sleep(0.5)
                                return
                        elif new_loc.has_hero and new_loc.hero.operating_hero == attacker.operating_hero:
                            print("You already have a Unit standing there.")
                            time.sleep(0.5)
                        elif new_loc.has_hero and new_loc.hero.operating_hero != attacker.operating_hero:
                            attacker.speed_left -= new_loc.speed_drain
                            defender = new_loc.hero
                            original_health = defender.health
                            total_damage_attack = attacker.amount * attacker.damage
                            original_attack_damage = total_damage_attack
                            defender.health -= total_damage_attack
                            total_damage_attack -= original_health
                            while defender.health <= 0:
                                defender.amount -= 1
                                defender.health = original_health
                                if total_damage_attack > 0:
                                    defender.health -= total_damage_attack
                                    total_damage_attack -= original_health
                            if defender.amount < 1:
                                new_loc.has_hero = False
                                new_loc.hero = None
                            if defender.has_retaliated == False and new_loc.has_hero:
                                total_damage_defend = defender.amount * defender.damage
                                original_defend_damage = total_damage_defend
                                original_health = attacker.health
                                attacker.health -= total_damage_defend
                                total_damage_defend -= original_health
                                while attacker.health <= 0:
                                    attacker.amount -= 1
                                    attacker.health = original_health
                                    if total_damage_defend > 0:
                                        attacker.health -= total_damage_defend
                                        total_damage_defend -= original_health
                                if attacker.amount < 1:
                                    old_loc.has_hero = False
                                    old_loc.hero = None
                                defender.has_retaliated = True
                                self.dialogue_display(attacker.name + " attacks " + defender.name, " with " +
                                    str(original_attack_damage) + " damage!", defender.name + " retaliates with ",
                                                      str(original_defend_damage) + " damage!")

                            else:
                                self.dialogue_display(attacker.name + " attacks " + defender.name, " with " +
                                                  str(original_attack_damage) + "!")

                            return

    def enter_town(self, town, map):
        if town.render == None:
            town.render = Gameboard(10, 12, False)
        while True:
            Renderer.renderer(town)
            town.render.view_town(town, self)
            choice = self.dialogue_return("What do you want to do?").lower()
            while choice not in("build", "recruit", "mage guild", "tavern", "exit"):
                choice = self.dialogue_return("See the upper action bar for available commands.").lower()
            if choice == "build":
                if town.has_built:
                    self.dialogue_display("You can only build once per turn.")
                else:
                    see_price = self.dialogue_return(str(town.buildings_available),"",
                                                     "Type a building to see its price.").lower()
                    while see_price.title() not in town.buildings_available:
                        see_price = self.dialogue_return(str(town.buildings_available), "",
                                                         "Type a building to see its price.").lower()
                    if see_price == "upgrade hall":
                        if town.hall_lvl == 1:
                            choice = self.dialogue_return("Town Hall", " Requirements: None. Price: 2500 Gold",
                                "Press Enter to construct this building.","Type ""C"" to cancel.").lower()
                            if choice != "c":
                                if self.gold >= 2500:
                                    self.gold -= 2500
                                    town.hall_lvl = 2
                                    self.dailyg += 500
                                    town.has_built = True
                                else:
                                    self.dialogue_display("You lack the necessary funds.")
                        elif town.hall_lvl == 2:
                            choice = self.dialogue_return("City Hall",
                                                          " Requirements: None. Price: 5000 Gold",
                                                          "Press Enter to construct this building.",
                                                          "Type ""C"" to cancel.").lower()
                            if choice != "c":
                                if self.gold >= 5000 and town.town_lvl == 2:
                                    self.gold -= 5000
                                    town.hall_lvl = 3
                                    self.dailyg += 1000
                                    town.has_built = True
                                else:
                                    self.dialogue_display("You lack the necessary funds and/or requirements.")
                        elif town.hall_lvl == 3:
                            choice = self.dialogue_return("Capitol",
                                                          " Requirements: Castle. Price: 10.000 Gold",
                                                          "Press Enter to construct this building.",
                                                          "Type ""C"" to cancel.").lower()
                            if choice != "c":
                                if self.gold >= 10000 and town.town_lvl == 3:
                                    town.buildings_available.remove("Upgrade Hall")
                                    self.gold -= 10000
                                    town.hall_lvl = 4
                                    self.dailyg += 2000
                                    town.has_built = True
                                else:
                                    self.dialogue_display("You lack the necessary funds and/or requirements.")
                    elif see_price == "upgrade mage guild":
                        if town.guild_lvl == 1:
                            choice = self.dialogue_return("Mage Guild Lvl 2 ", "Price: 2000 Gold, 5 Wood, 5 Stone,"
                                "4 Mercury, 4 Crystal, 4 Gems, 4 Sulfur", "Press Enter to construct this building.",
                                "Type ""C"" to cancel.").lower()
                            if choice != "c":
                                if self.gold >= 2000 and self.wood > 4 and self.stone > 4 and self.mercury > 3 and\
                                        self.crystal > 3 and self.gems > 3 and self.sulfur > 3:
                                    self.gold -= 2000
                                    self.wood -= 5
                                    self.stone -= 5
                                    self.mercury -= 4
                                    self.gems -= 4
                                    self.crystal -= 4
                                    self.sulfur -= 4
                                    town.guild_lvl = 2
                                    town.has_built = True
                                else:
                                    self.dialogue_display("You lack the necessary funds.")
                        elif town.guild_lvl == 2:
                            choice = self.dialogue_return("Mage Guild Lvl 3 ",
                                "Req: Citadel. Price: 2000 Gold, 5 Wood, 5 Stone, 6 Mercury, 6 Crystal, 6 Gems, 6 Sulfur",
                                "Press Enter to construct this building.", "Type ""C"" to cancel.").lower()
                            if choice != "c":
                                if town.town_lvl== 2 and self.gold >= 2000 and self.wood > 4 and self.stone > 4 and\
                                        self.mercury > 5 and self.crystal > 5 and self.gems > 5 and self.sulfur > 5:
                                    self.gold -= 2000
                                    self.wood -= 5
                                    self.stone -= 5
                                    self.mercury -= 6
                                    self.gems -= 6
                                    self.crystal -= 6
                                    self.sulfur -= 6
                                    town.guild_lvl = 3
                                    town.has_built = True
                                else:
                                    self.dialogue_display("You lack the necessary funds and/or requirements.")
                        elif town.guild_lvl == 3:
                            choice = self.dialogue_return("Mage Guild Lvl 4", " Price: 2000 Gold, 5 Wood, 5 Stone,"
                                  "8 Mercury, 8 Crystal, 8 Gems, 8 Sulfur",
                                   "Press Enter to construct this building.", "Type ""C"" to cancel.").lower()
                            if choice != "c":
                                if self.gold >= 2000 and self.wood > 4 and self.stone > 4 and self.mercury > 7 and \
                                        self.crystal > 7 and self.gems > 7 and self.sulfur > 7:
                                    if town.kingdom == "Castle":
                                        town.buildings_available.remove("Upgrade Mage Guild")
                                    self.gold -= 2000
                                    self.wood -= 5
                                    self.stone -= 5
                                    self.mercury -= 8
                                    self.gems -= 8
                                    self.crystal -= 8
                                    self.sulfur -= 8
                                    town.guild_lvl = 4
                                    town.has_built = True
                                else:
                                    self.dialogue_display("You lack the necessary funds and/or requirements.")
                        elif town.guild_lvl == 4 and town.kingdom != "Castle":
                            choice = self.dialogue_return("Mage Guild Lvl 5", " Requirements: Castle. "
                                  "Price: 5000 Gold, 5 Wood, 5 Stone, 10 Mercury, 10 Crystal, 10 Gems, 10 Sulfur",
                                   "Press Enter to construct this building.", "Type ""C"" to cancel.").lower()
                            if choice != "c":
                                if town.town_lvl == 3 and self.gold >= 2000 and self.wood > 9 and self.stone > 9 \
                                        and self.mercury > 9 and self.crystal > 9 and self.gems > 9 and self.sulfur > 9:
                                    town.buildings_available.remove("Upgrade Mage Guild")
                                    self.gold -= 2000
                                    self.wood -= 10
                                    self.stone -= 10
                                    self.mercury -= 10
                                    self.gems -= 10
                                    self.crystal -= 10
                                    self.sulfur -= 10
                                    town.guild_lvl = 5
                                    town.has_built = True
                                else:
                                    self.dialogue_display("You lack the necessary funds and/or requirements.")

                    elif see_price == "upgrade fortification":
                        if town.town_lvl == 1:
                            choice = self.dialogue_return("Citadel", " Price: 5000 Gold, 10 Wood, 10 Stone",
                                "Press Enter to construct this building.", "Type ""C"" to cancel.").lower()
                            if choice != "c":
                                if self.gold >= 5000 and self.wood > 9 and self.stone > 9:
                                    self.gold -= 5000
                                    self.wood -= 10
                                    self.stone -= 10
                                    town.town_lvl = 2
                                    town.has_built = True
                                else:
                                    self.dialogue_display("You lack the necessary funds.")
                        elif town.hall_lvl == 2:
                            choice = self.dialogue_return("town", " Price: 10.000 Gold, 20 Wood, 20 Stone",
                                 "Press Enter to construct this building.", "Type ""C"" to cancel.").lower()
                            if choice != "c":
                                if self.gold >= 10000 and self.wood > 9 and self.stone > 9:
                                    self.gold -= 10000
                                    self.wood -= 20
                                    self.stone -= 20
                                    town.town_lvl = 3
                                    town.has_built = True
                                    town.buildings_available.remove("Upgrade Fortification")
                                else:
                                    self.dialogue_display("You lack the necessary funds and/or requirements.")
                    elif see_price == town.dw_names[2].lower():
                        choice = self.dialogue_return(town.dw_names[2], " Requirements: None. Price: 1000 Gold, 5 Stone",
                                "Press Enter to construct this building.", "Type ""C"" to cancel.").lower()
                        if choice != "c":
                            if self.gold >= 1000 and self.stone > 4:
                                self.gold -= 1000
                                self.stone -= 5
                                town.hasdw3 = True
                                town.dw3amount = 6
                                town.has_built = True
                                town.buildings_available.remove(town.dw_names[2])
                            else:
                                self.dialogue_display("You lack the necessary funds.")
                    elif see_price == town.dw_names[3].lower():
                        choice = self.dialogue_return(town.dw_names[3], " Requirements: " + town.dw_names[2] + ". "
                            "Price: 2000 Gold, 5 Stone", "Press Enter to construct this building.",
                            "Type ""C"" to cancel.").lower()
                        if choice != "c":
                            if self.gold >= 2000 and self.stone > 4 and town.hasdw3:
                                self.gold -= 2000
                                self.stone -= 5
                                town.hasdw4 = True
                                town.dw4amount = 4
                                town.has_built = True
                                town.buildings_available.remove(town.dw_names[3])
                            else:
                                self.dialogue_display("You lack the necessary funds and/or requirements.")
                    elif see_price == town.dw_names[4].lower():
                        choice = self.dialogue_return(town.dw_names[4], " Requirements: Mage Guild Lvl 2, "
                            + town.dw_names[3] + ". Price: 3000 Gold, 5 Wood, 5 Stone, 2 Mercury, 2 Crystal, 2 Gems,"
                            "2 Sulfur", "Press Enter to construct this building.", "Type ""C"" to cancel.").lower()

                        if choice != "c":
                            if self.gold >= 3000 and self.stone > 4 and self.wood > 4 and self.mercury > 1 and \
                                    self.crystal > 1 and self.gems > 1 and self.sulfur > 1 and town.hasdw4 and \
                                    town.guild_lvl >= 2:
                                self.gold -= 3000
                                self.stone -= 5
                                self.wood -= 5
                                self.mercury -= 2
                                self.gems -= 2
                                self.crystal -= 2
                                self.sulfur -= 2
                                town.hasdw5 = True
                                town.dw5amount = 3
                                town.has_built = True
                                town.buildings_available.remove(town.dw_names[4])
                            else:
                                self.dialogue_display("You lack the necessary funds and/or requirements.")

                    elif see_price == town.dw_names[5].lower():
                        choice = self.dialogue_return(town.dw_names[5], " Requirements: " + town.dw_names[3] +
                                ". Price: 5000 Gold, 20 Wood, 20 Stone",
                                    "Press Enter to construct this building.", "Type ""C"" to cancel.").lower()

                        if choice != "c":
                            if self.gold >= 5000 and self.wood > 19 and self.stone > 19 and town.hasdw4:
                                self.gold -= 5000
                                self.wood -= 20
                                self.stone -= 20
                                town.hasdw6 = True
                                town.dw6amount = 2
                                town.has_built = True
                                town.buildings_available.remove(town.dw_names[5])
                            else:
                                self.dialogue_display("You lack the necessary funds.")

                    elif see_price == town.dw_names[6].lower():
                        choice = self.dialogue_return(town.dw_names[6], " Requirements: " + town.dw_names[4] +
                                ". Price: 20000 Gold, 10 Mercury, 10 Sulfur, 10 Crystal, 10 Gems",
                                    "Press Enter to construct this building.", "Type ""C"" to cancel.").lower()

                        if choice != "c":
                            if self.gold >= 20000 and self.mercury > 9 and self.crystal > 9 and self.gems > 9 and\
                                    self.sulfur > 9 and town.hasdw5:
                                self.gold -= 20000
                                self.mercury -= 10
                                self.gems -= 10
                                self.crystal -= 10
                                self.sulfur -= 10
                                town.hasdw7 = True
                                town.dw7amount = 1
                                town.has_built = True
                                town.buildings_available.remove(town.dw_names[6])
                            else:
                                self.dialogue_display("You lack the necessary funds.")
                    else:
                        print("         There is no such building option.")
                        time.sleep(1)
            elif choice == "tavern":
                if map.square[town.location[0]][town.location[1]].has_hero:
                    self.dialogue_display("You cannot hire a new hero while your town is occupied by another hero.")
                elif self.has_hired == True:
                    self.dialogue_display("You have already hired a hero this turn.")
                else:
                    choice = self.dialogue_return("Hiring a new hero costs 2500 gold.", "", "Press Enter to hire. Press C to cancel.").lower()
                    if self.hero_ticker == 3:
                        self.dialogue_display("Unfortunately there are only three heroes to hire per player.")
                    elif choice != "c" and self.gold >= 2500:
                        self.create_heroes(town.location, map)
                        self.gold -= 2500
                        self.has_hired = True
                        self.dialogue_display("Hero hired! Press Enter to return to map.")
                        return
                    elif choice != "c" and self.gold < 2500:
                        self.dialogue_display("You lack the necessary funds.")

            elif choice == "recruit":
                visiting_hero = map.square[town.location[0]][town.location[1]].hero
                if visiting_hero == None:
                    choice = "not yet"
                    while choice not in ("", "c"):
                        choice = self.dialogue_return("You have no hero in town. Purchase army for fortification defense?",
                                                      "",
                                                      "\"Enter\" to purchase units. \"C\" to cancel.").lower()
                    if choice == "":
                        visiting_hero = town
                    else:
                        break

                while True:
                    see_price = ""
                    while see_price not in town.unit_names and see_price != "C":
                        see_price = self.dialogue_return("Type a unit to see its price.", "",
                                                         "Type \"C\" to cancel.").capitalize()
                    if see_price == "C":
                        break
                    else:
                        for i in range(7):
                            if see_price == list(town.unit_names)[i]:
                                available_stack = None
                                dw = None
                                if i == 0:
                                    available_stack = town.dw1amount
                                elif i == 1:
                                    available_stack = town.dw2amount
                                elif i == 2:
                                    available_stack = town.dw3amount
                                elif i == 3:
                                    available_stack = town.dw4amount
                                elif i == 4:
                                    available_stack = town.dw5amount
                                elif i == 5:
                                    available_stack = town.dw6amount
                                elif i == 6:
                                    available_stack = town.dw7amount
                                amount = "not yet"
                                while len(amount) > 2 or amount[0] not in (
                                "1", "2", "3", "4", "5", "6", "7", "8", "9", "C", "c"):
                                    amount = self.dialogue_return(see_price + ".",
                                                                  " Price: " + str(
                                                                      town.unit_names.get(see_price)) + " gold.",
                                                                  str(available_stack) + " available.",
                                                                  " Type the amount to recruit or C to cancel.")
                                if amount == "C" or amount == "c":
                                    break
                                else:
                                    amount = int(amount)
                                    if amount * town.unit_names.get(
                                            see_price) <= self.gold and amount <= available_stack:
                                        if len(visiting_hero.army) > 7:
                                            for i in visiting_hero.army:
                                                if i.name == see_price:
                                                    self.dialogue_display(
                                                        "Your army has run out of space. Recruited units will "
                                                        "be added to existing stack.")
                                                    visiting_hero.create_unit(town.kingdom, see_price, amount, True)
                                                    self.gold -= amount * town.unit_names.get(see_price)
                                                    if i == 0:
                                                        town.dw1amount -= amount
                                                    elif i == 1:
                                                        town.dw2amount -= amount
                                                    elif i == 2:
                                                        town.dw3amount -= amount
                                                    elif i == 3:
                                                        town.dw4amount -= amount
                                                    elif i == 4:
                                                        town.dw5amount -= amount
                                                    elif i == 5:
                                                        town.dw6amount -= amount
                                                    elif i == 6:
                                                        town.dw7amount -= amount
                                                    break
                                            self.dialogue_display("Your army is full! Press Enter to exit.")
                                            break
                                        else:
                                            visiting_hero.create_unit(town.kingdom, see_price, amount)
                                        self.gold -= amount * town.unit_names.get(see_price)
                                        if i == 0:
                                            town.dw1amount -= amount
                                        elif i == 1:
                                            town.dw2amount -= amount
                                        elif i == 2:
                                            town.dw3amount -= amount
                                        elif i == 3:
                                            town.dw4amount -= amount
                                        elif i == 4:
                                            town.dw5amount -= amount
                                        elif i == 5:
                                            town.dw6amount -= amount
                                        elif i == 6:
                                            town.dw7amount -= amount
                                        self.dialogue_return(str(amount) + " " + see_price + " recruited!")
                                    else:
                                        self.dialogue_display("You either do not have the gold", "",
                                                              "or lack available units.")

            elif choice == "exit":
                break


class Town:
    def __init__(self, input_name, input_kingdom, input_operating_player, input_hall_lvl, input_guild_lvl):
        self.name = input_name
        self.location = [0, 0]
        self.kingdom = input_kingdom
        self.operating_player = input_operating_player
        self.army = []
        self.alive = True
        self.town_lvl = 1
        self.hall_lvl = input_hall_lvl
        self.guild_lvl = input_guild_lvl
        self.hasdw1 = True
        self.hasdw2 = True
        self.hasdw3 = False
        self.hasdw4 = False
        self.hasdw5 = False
        self.hasdw6 = False
        self.hasdw7 = False
        self.dw1amount = 12
        self.dw2amount = 8
        self.dw3amount = 0
        self.dw4amount = 0
        self.dw5amount = 0
        self.dw6amount = 0
        self.dw7amount = 0
        self.render = None
        self.buildings_available = ["Upgrade Hall", "Upgrade Fortification", "Upgrade Mage Guild"]
        self.has_built = False
        self.dw_names = []
        self.unit_names_and_price = {}
        self.dw_color = ""

        if self.kingdom == "Castle":
            self.dw_names = ["Guardhouse", "Archery", "Griffin Tower", "Barracks", "Monastery", "Training Grounds", "Portal Of Glory"]
            self.unit_names = {"Pikeman":60, "Archer":100, "Griffin":200, "Swordsman":300, "Monk":400,
                               "Cavalier":1000, "Angel":1000}
            self.buildings_available.extend(self.dw_names[2:7])
            self.dw_color = '\033[93m'

        elif self.kingdom == "Inferno":
            self.dw_names = ["Imp Crucible", "Hall Of Sins", "Kennels", "Demon Gate", "Hell Hole", "Fire Lake",
                             "Forsaken Palace"]
            self.unit_names = {"Imp":60, "Gog":125, "Hellhound":200, "Demon":250, "Pit Fiend":500, "Efreet":900, "Devil":2700}
            self.buildings_available.extend(self.dw_names[2:7])
            self.dw_color = '\033[31m'

        elif self.kingdom == "Rampart":
            self.dw_names = ["Centaur Stables", "Dwarf Cottage", "Homestead", "Enchanted Spring", "Dendroid Arches", "Unicorn Glade",
                             "Dragon Cliffs"]
            self.unit_names = {"Centaur":70, "Dwarf":120, "Wood Elf":200, "Pegasus":250, "Dendroid Guard":350, "Unicorn":850, "Green Dragon":2400}
            self.buildings_available.extend(self.dw_names[2:7])
            self.dw_color = '\033[92m'

        elif self.kingdom == "Tower":
            self.dw_names = ["Workshop", "Parapet", "Golem Factory", "Mage Tower", "Altar of Wishes", "Golden Pavilion",
                             "Cloud Temple"]
            self.unit_names = {"Gremlin": 30, "Stone Gargoyle": 130, "Stone Golem": 150, "Mage": 350, "Genie": 850, "Naga": 1100,
                               "Giant": 2000}
            self.buildings_available.extend(self.dw_names[2:7])
            self.dw_color = '\033[94m'

    def new_week(self):
        if self.hasdw1:
            self.dw1amount += 14 * self.town_lvl
        if self.hasdw2:
            self.dw2amount += 9 * self.town_lvl
        if self.hasdw3:
            self.dw3amount += 7 * self.town_lvl
        if self.hasdw4:
            self.dw4amount += 4 * self.town_lvl
        if self.hasdw5:
            self.dw5amount += 3 * self.town_lvl
        if self.hasdw6:
            self.dw6amount += 2 * self.town_lvl
        if self.hasdw7:
            self.dw7amount += 1 * self.town_lvl

    def create_unit(self, kingdom, unit, amount, add_to_same_stack = False):
        if kingdom == "Castle":
            if unit == "Pikeman":
                new_unit = Unit("Pikeman", 1, amount, 4, 5, 2, 10, 4, 60, self)
            elif unit == "Archer":
                new_unit = Unit("Archer", 2, amount, 6, 3, 2, 10, 4, 100, self, True)
            elif unit == "Griffin":
                new_unit = Unit("Griffin", 3, amount, 8, 8, 5, 25, 6, 200, self)
            elif unit == "Swordsman":
                new_unit = Unit("Swordsman", 4, amount, 10, 12, 8, 35, 5, 300, self)
            elif unit == "Monk":
                new_unit = Unit("Monk", 5, amount, 12, 7, 10, 30, 5, 400, self, True)
            elif unit == "Cavalier":
                new_unit = Unit("Cavalier", 6, amount, 15, 15, 20, 100, 7, 1000, self)
            elif unit == "Angel":
                new_unit = Unit("Angel", 7, amount, 20, 20, 50, 200, 12, 3000, self)
        elif kingdom == "Inferno":
            if unit == "Imp":
                new_unit = Unit("Imp", 1, amount, 3, 3, 2, 4, 5, 60, self)
            elif unit == "Gog":
                new_unit = Unit("Gog", 2, amount, 6, 4, 3, 13, 4, 125, self, True)
            elif unit == "Hellhound":
                new_unit = Unit("Hellhound", 3, amount, 10, 6, 5, 25, 7, 200, self)
            elif unit == "Demon":
                new_unit = Unit("Demon", 4, amount, 10, 10, 8, 35, 5, 250, self)
            elif unit == "Pit Fiend":
                new_unit = Unit("Pit Fiend", 5, amount, 13, 13, 15, 45, 6, 500, self)
            elif unit == "Efreet":
                new_unit = Unit("Efreet", 6, amount, 16, 12, 20, 90, 9, 900, self)
            elif unit == "Devil":
                new_unit = Unit("Devil", 7, amount, 19, 21, 35, 160, 11, 2700, self)
        elif kingdom == "Rampart":
            if unit == "Centaur":
                new_unit = Unit("Centaur", 1, amount, 5, 3, 3, 8, 6, 70, self)
            elif unit == "Dwarf":
                new_unit = Unit("Dwarf", 2, amount, 6, 7, 3, 20, 3, 120, self)
            elif unit == "Wood Elf":
                new_unit = Unit("Wood Elf", 3, amount, 9, 5, 4, 15, 6, 200, self, True)
            elif unit == "Pegasus":
                new_unit = Unit("Pegasus", 4, amount, 9, 8, 7, 30, 8, 250, self)
            elif unit == "Dendroid Guard":
                new_unit = Unit("Dendroid Guard", 5, amount, 9, 12, 13, 55, 3, 350, self)
            elif unit == "Unicorn":
                new_unit = Unit("Unicorn", 6, amount, 15, 14, 20, 90, 7, 850, self)
            elif unit == "Green Dragon":
                new_unit = Unit("Green Dragon", 7, amount, 18, 18, 45, 180, 10, 2400, self)
        elif kingdom == "Tower":
            if unit == "Gremlin":
                new_unit = Unit("Gremlin", 1, amount, 3, 3, 2, 4, 4, 30, self)
            elif unit == "Stone Gargoyle":
                new_unit = Unit("Stone Gargoyle", 2, amount, 6, 6, 3, 16, 6, 130, self)
            elif unit == "Stone Golem":
                new_unit = Unit("Stone Golem", 3, amount, 7, 10, 4, 30, 3, 150, self)
            elif unit == "Mage":
                new_unit = Unit("Mage", 4, amount, 11, 8, 8, 25, 5, 350, self, True)
            elif unit == "Genie":
                new_unit = Unit("Genie", 5, amount, 12, 12, 14, 40, 7, 550, self)
            elif unit == "Naga":
                new_unit = Unit("Naga", 6, amount, 16, 13, 20, 110, 5, 1100, self)
            elif unit == "Giant":
                new_unit = Unit("Giant", 7, amount, 19, 16, 50, 150, 7, 2000, self)

        if add_to_same_stack:
            for u in self.army:
                if u.name == new_unit.name:
                    u.amount += new_unit.amount
                    break
        else:
            self.army.append(new_unit)
            placement = len(self.army)
            self.army[-1].start_location[0] = placement
class Unit:
    def __init__(self, input_name, input_rank, input_amount, input_attack, input_defense, input_damage, input_health,
                 input_speed, input_cost, input_hero, input_ranger = False):
        self.name = input_name
        self.rank = input_rank
        self.amount = input_amount
        self.attack = input_attack
        self.defense = input_defense
        self.damage = input_damage
        self.health = input_health
        self.speed_left = 0
        self.new_speed = input_speed
        self.start_location = [input_rank, 0]
        self.location = [0,0]
        self.operating_hero = input_hero
        self.isranged = input_ranger
        self.has_retaliated = False
        self.turn_left = True
        self.price = input_cost

    def __str__(self):
        return self.name

class Hero:
    def __init__(self, input_name, input_kind, input_attack, input_defense, input_knowledge, input_spellpower,
                 input_player):
        self.name = input_name
        self.kind = input_kind
        self.level = 1
        self.attack = input_attack
        self.defense = input_defense
        self.knowledge = input_knowledge
        self.spell_power = input_spellpower
        self.operating_player = input_player
        self.alive = True
        self.location = [0, 0]
        self.army = []
        self.artefacts = []
        self.speed_left = 10
        self.new_speed = 10

    def __str__(self):
        if self.alive:
            return f'{self.name}'

    def create_starting_army(self):
        if self.operating_player.kingdom == "Castle":
            unit1 = Unit("Pikeman", 1, 12, 4, 5, 2, 10, 4, 60, self)
            unit2 = Unit("Archer", 2, 5, 6, 3, 2, 10, 4, 100, self, True)
            unit3 = Unit("Griffin", 3, 2, 8, 8, 5, 25, 6, 200, self)
        elif self.operating_player.kingdom == "Inferno":
            unit1 = Unit("Imp", 1, 12, 3, 3, 2, 4, 5, 60, self)
            unit2 = Unit("Gog", 2, 5, 6, 4, 2, 13, 4, 125, self, True)
            unit3 = Unit("Hellhound", 3, 2, 10, 6, 5, 25, 7, 200, self)
        elif self.operating_player.kingdom == "Rampart":
            unit1 = Unit("Centaur", 1, 12, 5, 3, 3, 8, 6, 70, self)
            unit2 = Unit("Dwarf", 2, 5, 6, 7, 3, 20, 3, 120, self)
            unit3 = Unit("Wood Elf", 3, 2, 9, 5, 4, 15, 6, 200, self, True)
        elif self.operating_player.kingdom == "Tower":
            unit1 = Unit("Gremlin", 1, 12, 3, 3, 2, 4, 4, 30, self)
            unit2 = Unit("Stone Gargoyle", 2, 6, 6, 6, 3, 16, 6, 130, self)
            unit3 = Unit("Stone Golem", 3, 3, 7, 10, 4, 30, 3, 150, self)
        self.army.extend([unit1, unit2, unit3])

    def create_unit(self, kingdom, unit, amount, add_to_same_stack = False):
        if kingdom == "Castle":
            if unit == "Pikeman":
                new_unit = Unit("Pikeman", 1, amount, 4, 5, 2, 10, 4, 60, self)
            elif unit == "Archer":
                new_unit = Unit("Archer", 2, amount, 6, 3, 2, 10, 4, 100, self, True)
            elif unit == "Griffin":
                new_unit = Unit("Griffin", 3, amount, 8, 8, 5, 25, 6, 200, self)
            elif unit == "Swordsman":
                new_unit = Unit("Swordsman", 4, amount, 10, 12, 8, 35, 5, 300, self)
            elif unit == "Monk":
                new_unit = Unit("Monk", 5, amount, 12, 7, 10, 30, 5, 400, self, True)
            elif unit == "Cavalier":
                new_unit = Unit("Cavalier", 6, amount, 15, 15, 20, 100, 7, 1000, self)
            elif unit == "Angel":
                new_unit = Unit("Angel", 7, amount, 20, 20, 50, 200, 12, 3000, self)
        elif kingdom == "Inferno":
            if unit == "Imp":
                new_unit = Unit("Imp", 1, amount, 3, 3, 2, 4, 5, 60, self)
            elif unit == "Gog":
                new_unit = Unit("Gog", 2, amount, 6, 4, 2, 13, 4, 125, self, True)
            elif unit == "Hellhound":
                new_unit = Unit("Hellhound", 3, amount, 10, 6, 5, 25, 7, 200, self)
            elif unit == "Demon":
                new_unit = Unit("Demon", 4, amount, 10, 10, 8, 35, 5, 250, self)
            elif unit == "Pit Fiend":
                new_unit = Unit("Pit Fiend", 5, amount, 13, 13, 15, 45, 6, 500, self)
            elif unit == "Efreet":
                new_unit = Unit("Efreet", 6, amount, 16, 12, 20, 90, 9, 900, self)
            elif unit == "Devil":
                new_unit = Unit("Devil", 7, amount, 19, 21, 35, 160, 11, 2700, self)
        elif kingdom == "Rampart":
            if unit == "Centaur":
                new_unit = Unit("Centaur", 1, amount, 5, 3, 3, 8, 6, 70, self)
            elif unit == "Dwarf":
                new_unit = Unit("Dwarf", 2, amount, 6, 7, 3, 20, 3, 120, self)
            elif unit == "Wood Elf":
                new_unit = Unit("Wood Elf", 3, amount, 9, 5, 4, 15, 6, 200, self, True)
            elif unit == "Pegasus":
                new_unit = Unit("Pegasus", 4, amount, 9, 8, 7, 30, 8, 250, self)
            elif unit == "Dendroid Guard":
                new_unit = Unit("Dendroid Guard", 5, amount, 9, 12, 13, 55, 3, 350, self)
            elif unit == "Unicorn":
                new_unit = Unit("Unicorn", 6, amount, 15, 14, 20, 90, 7, 850, self)
            elif unit == "Green Dragon":
                new_unit = Unit("Green Dragon", 7, amount, 18, 18, 45, 180, 10, 2400, self)
        elif kingdom == "Tower":
            if unit == "Gremlin":
                new_unit = Unit("Gremlin", 1, amount, 3, 3, 2, 4, 4, 30, self)
            elif unit == "Stone Gargoyle":
                new_unit = Unit("Stone Gargoyle", 2, amount, 6, 6, 3, 16, 6, 130, self)
            elif unit == "Stone Golem":
                new_unit = Unit("Stone Golem", 3, amount, 7, 10, 4, 30, 3, 150, self)
            elif unit == "Mage":
                new_unit = Unit("Mage", 4, amount, 11, 8, 8, 25, 5, 350, self, True)
            elif unit == "Genie":
                new_unit = Unit("Genie", 5, amount, 12, 12, 14, 40, 7, 550, self)
            elif unit == "Naga":
                new_unit = Unit("Naga", 6, amount, 16, 13, 20, 110, 5, 1100, self)
            elif unit == "Giant":
                new_unit = Unit("Giant", 7, amount, 19, 16, 50, 150, 7, 2000, self)
        if add_to_same_stack:
            for u in self.army:
                if u.name == new_unit.name:
                    u.amount += new_unit.amount
                    break
        else:
            self.army.append(new_unit)
            placement = len(self.army)
            self.army[-1].start_location[0] = placement

    def confront_object(self, location):
        player = self.operating_player
        other_player = None
        if location.operated_by != None and location.operated_by != player:
            other_player = location.operated_by

        if location.object_name in ("wood", "stone", "crystal", "gems", "gold", "sulfur", "mercury") and \
                location.operated_by == None:
            player.dialogue_display("You gain operation of a ", "", location.object_name, " mine!")
            location.operated_by = player
        match location.object_name:
            case "wood":
                if other_player != None:
                    other_player.dailyw -= 2
                player.dailyw += 2
            case "stone":
                if other_player != None:
                    other_player.dailys -= 2
                player.dailys += 2
            case "crystal":
                if other_player != None:
                    other_player.dailyc -= 1
                player.dailyc += 1
            case "mercury":
                if other_player != None:
                    other_player.dailym -= 1
                player.dailym += 1
            case "gems":
                if other_player != None:
                    other_player.dailyge -= 1
                player.dailyge += 1
            case "gold":
                if other_player != None:
                    other_player.dailyg -= 1000
                player.dailyg += 1000
            case "sulfur":
                if other_player != None:
                    other_player.dailysu -= 1
                player.dailysu += 1
            case "XP_stone":
                if self.name not in location.met_heroes:
                    self.level += 1
                    location.met_heroes.append(self.name)
                    choice = ""
                    while choice not in("Attack", "Defense", "Knowledge", "Spell Power"):
                        choice = player.dialogue_return("You have gained a level!", "",
                                                        "Type the skill you want to increase.").capitalize()
                    match choice:
                        case "Attack":
                            self.attack += 1
                        case "Defense":
                            self.defense += 1
                        case "Knowledge":
                            self.knowledge += 1
                        case "Spell Power":
                            self.spell_power += 1
                else:
                    player.dialogue_display("You have already visited this stone of wisdom.")

            case "Pool":
                if self.name not in location.met_heroes:
                    location.met_heroes.append(self.name)
                    player.dialogue_display("You enter a pool of spring water. It's refreshing to you and your troops.",
                                            "", "Your speed has permanently increased with 1.")
                    self.new_speed += 1

                else:
                    player.dialogue_display("You have already visited this fountain.")
            case "Sword":
                    player.dialogue_display("You have found a legendary old sword ", player.name, " attack increased by 2.")
                    self.attack += 2
                    self.artefacts.append("sword")
                    location.has_object = False
                    location.object_name = ""

            case "Shield":
                player.dialogue_display("You have found a shield of power ", player.name, " defense increased by 3.")
                self.defense += 3
                self.artefacts.append("shield")
                location.has_object = False
                location.object_name = ""

            case "Boots":
                player.dialogue_display("You have found the Boots of Speed ", player.name, " speed increased by 3.")
                self.new_speed += 3
                self.artefacts.append("boots")
                location.has_object = False
                location.object_name = ""

            case "Treasure":
                location.has_object = False
                location.object_name = ""
                choice = ""
                while choice not in ("xp", "gold"):
                    choice = player.dialogue_return("You have found treasure. Do you want to keep the 2000 gold", "",
                                                    "or distribute it for experience (1 level?)", "     XP / Gold").lower()
                    if choice == "xp":
                        self.level += 1
                        choice2 = ""
                        while choice2 not in ("Attack", "Defense", "Knowledge", "Spell Power"):
                            choice2 = player.dialogue_return("You have gained a level!", "",
                                                            "Type the skill you want to increase.").capitalize()
                        match choice2:
                            case "Attack":
                                self.attack += 1
                            case "Defense":
                                self.defense += 1
                            case "Knowledge":
                                self.knowledge += 1
                            case "Spell Power":
                                self.spell_power += 1
                    else:
                        player.gold += 2000

class Gameboard:
    COORDINATES = '\030[47m'
    END = '\033[0m'
    def __init__(self, input_rows, input_cols, map = True):
        self.square = []
        rows, cols = input_rows, input_cols
        self.watercounter = 0
        self.mountaincounter = 0

        for i in range(rows):
            col = []
            for j in range(cols):
                kind = ""
                speed_drain = 0
                dice = 0
                if map == True:
                    while dice == 0:
                        dice = random.randrange(1, 14)
                        if i > 0 and j > 0:
                            if self.square[(i-1)][j].kind == "mountain" or self.square[(i-1)][(j-1)].kind == "mountain":
                                dice = random.randrange(1, 3)
                                if dice != 1:
                                    dice = random.randrange(2, 9)

                            elif self.square[(i-1)][j].kind == "water" or self.square[(i-1)][(j-1)].kind == "water":
                                dice = random.randrange(12, 14)
                                if dice != 13:
                                    dice = random.randrange(2, 13)
                        if i in (0, 1):
                            dice = random.randrange(2, 13)

                        if dice == 1 and self.mountaincounter < input_cols * 3:
                            self.mountaincounter += 1
                            kind = "mountain"
                            speed_drain = 8
                        elif dice in (2, 3, 4, 5):
                            kind = "forest"
                            speed_drain = 2
                        elif dice in (6, 7, 8, 9):
                            kind = "plains"
                            speed_drain = 1
                        elif dice in (10, 11, 12):
                            kind = "hills"
                            speed_drain = 1
                        elif dice == 13 and self.watercounter < input_cols * 3:
                            self.watercounter += 1
                            kind = "water"
                            speed_drain = 10
                        else:
                            dice = 0
                elif cols == 12:
                    kind = ""
                else:
                    kind = "battlefield"
                    speed_drain = 1

                landscape = Landscape(kind, str(i) + str(j), speed_drain)
                col.append(landscape)
            self.square.append(col)

    def beautifier(self, rows, cols):
        for i in range(rows):
            for j in range(cols):
                if (i > 0 and j > 0) and (i < rows-1 and j < cols-1):
                    if self.square[i][j].kind == "mountain":
                        counter = 0
                        for c in range(-1, 2):
                            for d in range(-1, 2):
                                if self.square[i+c][j+d].kind == "mountain":
                                    counter += 1
                        if counter < 3:
                            self.square[i][j].kind = "forest"
                            self.square[i][j].color = '\033[102m'
                            self.square[i][j].speed_drain = 2
                    elif self.square[i][j].kind == "water":
                        counter = 0
                        for c in range(-1, 2):
                            for d in range(-1, 2):
                                if self.square[i+c][j+d].kind == "water":
                                    counter += 1
                        if counter < 3:
                            self.square[i][j].kind = "forest"
                            self.square[i][j].color = '\033[102m'
                            self.square[i][j].speed_drain = 2

    def populator(self, input_rows, input_cols, number_of_players):
        for i in range(number_of_players):
            start_row = 0
            end_row = 0
            start_col = 0
            end_col = 0
            mines = ["wood", "stone", "mercury", "crystal", "gems", "sulfur", "gold"]
            chests = ["Treasure", "Treasure", "Treasure", "Treasure", "Treasure", "Treasure"]
            buildings = ["XP_stone", "Pool", "Shrine1", "Shrine2"]
            artefacts = ["Sword", "Shield", "Boots"]
            if i == 0:
                start_row = 1
                end_row = int(input_rows / 2 - 1)
                start_col = 1
                if number_of_players < 3:
                    end_col = input_cols - 1
                else:
                    end_col = int(input_cols / 2 - 1)
            elif i == 1:
                start_row = int(input_rows / 2 + 1)
                end_row = input_rows - 1
                start_col = 1
                if number_of_players < 3:
                    end_col = input_cols - 1
                else:
                    end_col = int(input_cols / 2 - 1)
            elif i == 2:
                start_row = 1
                end_row = int(input_rows / 2 - 1)
                start_col = int(input_cols / 2 + 1)
                end_col = input_cols - 1
            elif i == 3:
                start_row = int(input_rows / 2 + 1)
                end_row = input_rows - 1
                start_col = int(input_cols / 2 + 1)
                end_col = input_cols - 1

            self.populate(mines, start_row, end_row, start_col, end_col)
            self.populate(chests, start_row, end_row, start_col, end_col)
            self.populate(buildings, start_row, end_row, start_col, end_col)
            self.populate(artefacts, start_row, end_row, start_col, end_col)

    def populate(self, lst, start_row, end_row, start_col, end_col):
        while len(lst) > 0:
            dice_row = random.randrange(start_row, end_row)
            dice_col = random.randrange(start_col, end_col)
            while self.square[dice_row][dice_col].kind == "mountain" or self.square[dice_row][dice_col].kind == "water"\
                    or self.square[dice_row][dice_col].has_object:
                dice_row = random.randrange(start_row, end_row)
                dice_col = random.randrange(start_col, end_col)
            dice = random.randrange(0, len(lst))
            self.square[dice_row][dice_col].has_object = True
            self.square[dice_row][dice_col].object_name = lst.pop(dice)

    def view_board(self, p, moving = False):
        rows = len(self.square)
        cols = len(self.square[0])
        if moving == True:
            print(f"{p.color}Commands:         Move with \"QWE ASD ZX\"          Exit moving with \"o\"                "
                  f"                                                                                                   "
                  f"                                            \033[0m")
        else:
            print(f"{p.color}Commands:         \"View\"          \"Move\"          \"Town\"          \"Spells\"        "
                  f"  \"End turn\"                                                                                     "
                  f"                                                  \033[0m")
        for i in range(rows):
            for j in range(cols):
                sys.stdout.write(str(self.square[i][j].print_structure(p)))
            print("")
            for j in range(cols):
                sys.stdout.write(self.square[i][j].print_hero(p))
            print("")
        print(f"{p.color} Wood:{p.wood}      Stone:{p.stone}      Crystal:{p.crystal}       Gems:{p.gems}        "
              f"Sulfur:{p.sulfur}        Mercury:{p.mercury}        Gold:{p.gold}                                      "
              f"                                                                                           \033[0m")

    def view_battlefield(self, p, attacker):
        rows = len(self.square)
        cols = len(self.square[0])
        print(f"{p.color} Commands:         \"r\" for ranged attack          \"Spells\" for spellbook           "
              f"\"o\" to stop moving (skip turn)                                             \033[0m ")
        print("|---------------------------------------------------------------------------------------------------"
              "-------------------------------------------------------|")
        for i in range(rows):
            for j in range(cols):
                sys.stdout.write(self.square[i][j].print_war1row(p))
            print("")
            for j in range(cols):
                sys.stdout.write(self.square[i][j].print_war2row(p, attacker))
            print("")
            for j in range(cols):
                sys.stdout.write(self.square[i][j].print_war3row(p))
            print("")
            for j in range(cols):
                sys.stdout.write("|-----------")
            print("")

    def view_town(self, c, p):
        rows = len(self.square)
        cols = len(self.square[0])
        print(f"{p.color}Commands:         \"Build\"          \"Recruit\"          \"Mage Guild\"          \"Tavern\"  "
              f"       \"Exit\"                                              \033[0m\n")
        for i in range(rows):
            for j in range(cols):
                sys.stdout.write(str(self.square[i][j].print_town1row(c)))
            print("")
            for j in range(cols):
                sys.stdout.write(self.square[i][j].print_town2row(c))
            print("")
            for j in range(cols):
                sys.stdout.write(self.square[i][j].print_town3row(c))
            print("")
        print(
            f"{p.color}Wood:{p.wood} Stone:{p.stone} Crystal:{p.crystal} Gems:{p.gems} Sulfur:{p.sulfur} Mercury:"
            f"{p.mercury} Gold:{p.gold} {c.dw_color}     |      {list(c.unit_names)[0]}:{c.dw1amount} | "
            f"{list(c.unit_names)[1]}:{c.dw2amount} | {list(c.unit_names)[2]}:{c.dw3amount} | {list(c.unit_names)[3]}:"
            f"{c.dw4amount} | {list(c.unit_names)[4]}:{c.dw5amount} | {list(c.unit_names)[5]}:{c.dw6amount} |"
            f" {list(c.unit_names)[6]}:{c.dw7amount} \033[0m")

class Landscape:
    #os.system('color')
    HILLS = '\033[42m'
    WATER = '\033[44m'
    MOUNTAIN = '\033[100m'
    PLAINS = '\033[43m'
    FOREST = '\033[102m'
    RED = '\033[31m'
    DW = '\033[93m'
    BOLD = '\033[1m'
    END = '\033[0m'

    def __init__(self, input_kind, input_coord, input_speed):
        self.kind = input_kind
        self.coord = input_coord
        self.placement = [0,0]
        self.met_heroes = []
        self.speed_drain = input_speed
        self.has_hero = False
        self.hero = None
        self.color = ""
        self.has_object = False
        self.town = None
        self.operated_by = None
        self.object_name = ""
        self.seen = [0, 0, 0, 0,]

        if self.kind == "plains":
            self.color = Landscape.PLAINS

        if self.kind == "hills":
            self.color = Landscape.HILLS

        if self.kind == "mountain":
            self.color = Landscape.MOUNTAIN

        if self.kind == "water":
            self.color = Landscape.WATER

        if self.kind == "forest":
            self.color = Landscape.FOREST

    # 0 = 1/2/3/4: botten, mitt, tak, singelvåning | 1 = 1/2/3/4/5: vänster, mitt, höger, center, special
    def print_town1row(self, c):
        if self.placement[0] in (3, 4) and self.placement[1] == 4:
            return f'////^^^^\\\\\\\\'
        elif self.placement[0] in (3, 4) and self.placement[1] == 1:
            return f'\\__#        '
        elif self.placement[0] in (3, 4) and self.placement[1] == 2:
            return f'     /\     '
        elif self.placement[0] in (3, 4) and self.placement[1] == 3:
            return f'        #__/'
        elif self.placement[0] in (1, 2):
            return f'|##########|'
        else:
            return f'            '

    def print_town2row(self, c):
        if self.placement[0] in (1, 4) and self.placement[1] in (4, 5):
            return f'|{c.dw_color}' + '{: ^10s}'.format(self.kind[:10]) + f'{Landscape.END}|'
        elif self.placement[0] == 1 and self.placement[1] == 1:
            return f'|#####     |'
        elif self.placement[0] == 1 and self.placement[1] == 2:
            return f'|    ###   |'
        elif self.placement[0] == 1 and self.placement[1] == 3:
            return f'|     #####|'
        elif self.placement[0] == 2 and self.placement[1] == 1:
            return f'|##        |'
        elif self.placement[0] == 2 and self.placement[1] == 2:
            return f'|    XX    |'
        elif self.placement[0] == 2 and self.placement[1] == 3:
            return f'|        ##|'
        elif self.placement[0] == 2 and self.placement[1] == 4:
            return f'|##  ##  ##|'
        elif self.placement[0] in (3, 4) and self.placement[1] == 1:
            return f'/  |       #'
        elif self.placement[0] in (3, 4) and self.placement[1] == 2:
            return f'#    ##    #'
        elif self.placement[0] in (3, 4) and self.placement[1] == 3:
            return f'#       #  \\'
        elif self.placement[0] in (3, 4) and self.placement[1] == 4:
            return f'|#   ##   #|'
        else:
            return f'            '

    def print_town3row(self, c):
        if self.kind != "":
            return f'|##########|'
        else:
            return f'            '

    def __str__(self):
        return f'{self.color}' + '{: ^11s}'.format(self.kind[:8]) + f'{Landscape.END}'

    def print_structure(self, input_player):
        if self.has_object and self.seen[input_player.number-1] == 1:
            return f'{self.color}{Landscape.DW}' +'{: ^6s}'.format(self.object_name[:6]) + f'{Landscape.END}'
        elif self.seen[input_player.number-1] == 1:
            return f'{self.color}      {Landscape.END}'
        else:
            return f'      '

    def print_hero(self, input_player):
        if self.has_hero and self.seen[input_player.number-1] == 1:
            return f'{self.color}{Landscape.RED}' + '{: ^6s}'.format(self.hero.name[:4] +","+ str(self.hero.level)) + \
                   f'{Landscape.END}'
        elif self.seen[input_player.number-1] == 1:
            return f'{self.color}      {Landscape.END}'
        else:
            return f'      '

    def print_war1row(self, current_player):
        self.color = Landscape.END
        if self.has_hero and self.hero.operating_hero.operating_player != current_player:
            return f'|           '
        elif self.has_hero:
            return f'|           '
        else:
            return f'|           '

    def print_war2row(self, current_player, attacker):
        self.color = Landscape.END
        if self.has_hero and self.hero.operating_hero.operating_player != current_player and self.hero.amount > 0:
            return f'|{Landscape.RED}' + '{: ^11s}'.format(
                self.hero.name[:7].upper() + ", " + str(self.hero.amount)) + f'{Landscape.END}'

        elif self.has_hero and self.hero.amount > 0:
            if attacker.location == self.hero.location:
                self.color = '\033[33m'
            return f'|{self.color}' + '{: ^11s}'.format(
                self.hero.name[:7].upper() + ", " + str(self.hero.amount)) + f'{Landscape.END}'
        else:
            return f'|           '

    def print_war3row(self, current_player):
        self.color = Landscape.END
        if self.has_hero and self.hero.operating_hero.operating_player != current_player and self.hero.amount > 0:
            return f'|{Landscape.RED}' + '{: ^11s}'.format(str(self.hero.health) + "hp|" + str(self.hero.new_speed)
                                                           + "sp") + f'{Landscape.END}'
        elif self.has_hero and self.hero.amount > 0:
            return f'|' + '{: ^11s}'.format(str(self.hero.health) + "hp"
                                                                    "|" + str(self.hero.new_speed) + "sp")
        else:
            return f'|           '