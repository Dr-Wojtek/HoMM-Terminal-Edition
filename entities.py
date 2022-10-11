import random
import os
import time
import sys
from renderer import Renderer

# This program is a hobby project. Its goal is to simulate the game 'Heroes of Might and Magic 3' in the terminal.
# The code is written by Alex Stråe, from Sweden, aka Dr-Wojtek @ GitHub. Creatures, heroes and town attributes and
# names are, where copied correctly, copied from the original game 'Heroes of Might and Magic 3'.


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
        self.has_hired = False
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
        self.weekday = 1
        self.week = 1

    def __str__(self):
        return f'{self.name}'

    def clear_window():
        os.system('cls' if os.name == 'nt' else 'clear')

    def dialogue_display(self, input1="", input2="", input3="", input4=""):
        print("-" +'{:-^140s}'.format("-") + "-")
        print("|" + '{:^140s}'.format(input1 + input2) + "|")
        print("|" + '{:^140}'.format(input3 + input4) + "|")
        print("-" + '{:-^140s}'.format("-") + "-")
        input("\n")

    def dialogue_return(self, input1 = "", input2="", input3="", input4=""):
        print("-" +'{:-^140s}'.format("-") + "-")
        print("|" + '{:^140s}'.format(input1 + input2) + "|")
        print("|" + '{:^140s}'.format(input3 + input4) + "|")
        print("-" + '{:-^140s}'.format("-") + "-")
        choice = input("\n")
        return choice

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
        if self.heroes != []:
            for hero in self.heroes:
                hero.speed_left = hero.new_speed
        self.weekday += 1
        if self.weekday == 8:
            self.has_hired = False
            self.weekday = 1
            self.week += 1
            if self.towns != []:
                for town in self.towns:
                    town.new_week()
        for hero in self.heroes:
            if hero.spell_points < hero.knowledge:
                hero.spell_points += 4

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
                    new_hero = Hero("Adelaide", "Cleric", 1, 1, 2, 1, self, [{"name": "Magic Arrow", "cost": 4,
                        "damage": 10, "effect": ""}, {"name": "Shield", "cost": 4, "damage": 0, "effect": "shield", "color": "green"}])
                case 2:
                    new_hero = Hero("Tyris", "Knight", 2, 2, 0, 1, self)
        elif self.kingdom == "Inferno":
            match self.hero_ticker:
                case 0:
                    new_hero = Hero("Zydar", "Heretic", 1, 1, 2, 1, self, [{"name": "Magic Arrow", "cost": 4,
                        "damage": 10, "effect": ""}, {"name": "Slow", "cost": 4, "damage": 0, "effect": "slow", "color": "red"}])
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
                    new_hero = Hero("Elleshar", "Druid", 1, 1, 1, 2, self, [{"name": "Magic Arrow", "cost": 4,
                        "damage": 10, "effect": ""}, {"name": "Slow", "cost": 4, "damage": 0, "effect": "slow", "color": "red"}])
        elif self.kingdom == "Tower":
            match self.hero_ticker:
                case 0:
                    new_hero = Hero("Solmyr", "Wizard", 0, 1, 2, 2, self, [{"name": "Magic Arrow", "cost": 4,
                        "damage": 10, "effect": ""}, {"name": "Haste", "cost": 4, "damage": 0, "effect": "haste", "color": "green"}])
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
            new_town = Town("Valetta", self.kingdom, self, 1, 0)
        elif self.kingdom == "Inferno":
            new_town = Town("Styx", self.kingdom, self, 1, 0)
        elif self.kingdom == "Rampart":
            new_town = Town("Goldenglade", self.kingdom, self, 1, 0)
        elif self.kingdom == "Tower":
            new_town = Town("Celeste", self.kingdom, self, 1, 0)
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
        map.square[dice_row][dice_col].operated_by = self
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

    def interpretor(self, choice, map, list_of_players):
        if choice.lower() == "view":
            self.view_info()

        elif choice.lower() == "move":
            if len(self.heroes) == 1:
                hero_choice = self.heroes[0].name
            elif self.heroes == []:
                self.dialogue_display("You have no heroes left! Recruit new ones in a tavern, in a town.")
            else:
                hero_choice = input("Move which hero?\n")
            self.move_obj(hero_choice, map)

        elif choice.lower() == "spells":
            if len(self.heroes) == 1:
                hero = self.heroes[0]
            else:
                hero = input("Spells for which hero?\n")
                if self.has_hero_name(hero):
                    hero = self.get_hero(hero)
                else:
                    self.dialogue_display("No hero found.")
            if hero.spellbook != []:
                hero.view_spells()
                spell = ""
                while spell == "":
                    spell = self.dialogue_return("Name the spell you want to throw or ""C"" to cancel.").title()
                if spell != "C":
                    spell_cost = None
                    for spell_in_book in hero.spellbook:
                        if spell == spell_in_book.get("name"):
                            spell_cost = spell_in_book.get("cost")
                    if spell_cost == None:
                        self.dialogue_display("Could not find that spell.")
                    elif spell != "Summon Boat":
                        self.dialogue_display(hero.name + " cannot throw that spell outside of combat.")
                    else:
                        hero.has_boat = True
                        hero.spell_points -= spell_cost
                        self.dialogue_display(hero.name + " has a boat until they step on ground!")
            else:
                print(hero.name + " does not have a spellbook.")

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
        Player.clear_window()
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
                Player.clear_window()
                input_board.view_board(self, True)
                choice = ""
                while choice == "" or choice[0] not in ("q", "w", "e", "a", "s", "d", "z", "x", "o", "-"):
                    choice = input(hero.speed_bar()).lower()
                old_pos = hero.location
                new_pos = [0, 0]
                if choice[0] == 'q':
                    new_pos[0], new_pos[1] = old_pos[0] - 1, old_pos[1] - 1
                elif choice[0] == 'w':
                    new_pos[0], new_pos[1] = old_pos[0] - 1, old_pos[1]
                elif choice[0] == 'e':
                    new_pos[0], new_pos[1] = old_pos[0] - 1, old_pos[1] + 1
                elif choice[0] == 'a':
                    new_pos[0], new_pos[1] = old_pos[0], old_pos[1] - 1
                elif choice[0] == 's':
                    new_pos[0], new_pos[1] = old_pos[0] + 1, old_pos[1]
                elif choice[0] == 'd':
                    new_pos[0], new_pos[1] = old_pos[0], old_pos[1] + 1
                elif choice[0] == 'z':
                    new_pos[0], new_pos[1] = old_pos[0] + 1, old_pos[1] - 1
                elif choice[0] == 'x':
                    new_pos[0], new_pos[1] = old_pos[0] + 1, old_pos[1] + 1
                elif choice[0] == '-':
                    hero.speed_left += 1000
                    hero.new_speed += 1000
                    break
                elif choice[0] == "o":
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
                if new_loc.kind == "water" and hero.has_boat is False:
                    continue
                else:
                    if old_loc.kind == "water" and new_loc.kind != "water":
                        hero.has_boat = False
                    if new_loc.speed_drain <= hero.speed_left:
                        hero.speed_left -= new_loc.speed_drain
                        if new_loc.has_hero and new_loc.hero.operating_player != self:
                            self.start_war(hero, new_loc.hero, new_loc, old_loc)
                            if hero.army:
                                for unit in hero.army:
                                    if unit.amount <= 0:
                                        hero.army.remove(unit)
                                    if type(new_loc.object_name) == Hero:
                                        new_loc.object_name = ""
                            else:
                                for unit in new_loc.hero.army:
                                    if unit.amount <= 0:
                                        new_loc.hero.army.remove(unit)

                        elif new_loc.has_object and new_loc.object_name == "Town" and \
                                new_loc.town.operating_player != self:
                            if new_loc.town.army != []:
                                self.start_war(hero, new_loc.town, new_loc, old_loc)
                                if hero.army:
                                    for unit in hero.army:
                                        if unit.amount <= 0:
                                            hero.army.remove(unit)
                                else:
                                    for unit in new_loc.town.army:
                                        if unit.amount <= 0:
                                            new_loc.town.army.remove(unit)
                                new_loc.town.alive = True
                            else:
                                self.towns.append(new_loc.town)
                                new_loc.operated_by = self
                                for i in range(len(new_loc.town.operating_player.towns)):
                                    if new_loc.town.operating_player.towns[i].name == new_loc.town.name:
                                        new_loc.town.operating_player.towns.pop(i)
                                self.towns[-1].operating_player = self
                                if self.towns[-1].hall_lvl == 4:
                                    self.towns[-1].hall_lvl = 3
                                self.dialogue_display("You have conquered a town!")
                        elif new_loc.has_object and new_loc.object_name == "Town" and \
                                new_loc.town.operating_player == self:
                            old_loc.has_hero = False
                            old_loc.hero = None
                            new_loc.has_hero = True
                            new_loc.hero = hero
                            hero.location = new_pos
                            self.enter_town(new_loc.town, input_board)
                            return

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
                            time.sleep(1)
                            return
                        elif hero.alive == False:
                            self.dialogue_display("Your forces suffer a bitter defeat, and " + hero.name + " leaves your cause.")
                            return
                    else:
                        print("You don't have enough speed to leave current location. Exiting movement now.")
                        time.sleep(2)
                        return

    def start_war(self, attacker, defender, battle_loc, old_loc):
        battlefield = Gameboard(10, 13, False)
        for u in attacker.army:
            if u.amount > 0:
                u.location[0] = u.start_location[0] + 1
                battlefield.square[u.location[0]][0].has_hero = True
                battlefield.square[u.location[0]][0].hero = u
                u.health = u.orig_health

        for u in defender.army:
            if u.amount > 0:
                u.location[0] = u.start_location[0] + 1
                u.location[1] = 12
                battlefield.square[u.location[0]][12].has_hero = True
                battlefield.square[u.location[0]][12].hero = u
                u.health = u.orig_health

        while attacker.alive and defender.alive:
            for u in attacker.army:
                u.has_retaliated = False
                u.speed_left = u.new_speed
                u.attack = u.orig_attack
                u.defense = u.orig_defense
                u.damage = u.orig_damage
            for u in defender.army:
                u.has_retaliated = False
                u.speed_left = u.new_speed
                u.attack = u.orig_attack
                u.defense = u.orig_defense
                u.damage = u.orig_damage
            attacker.can_throw_spell = True
            defender.can_throw_spell = True
            for i in range(7):
                if i < len(attacker.army):
                    if attacker.army[i].amount > 0:
                        attacker.operating_player.war_move_obj(attacker.army[i], defender, battlefield)
                        attacker.army[i].speed_left = attacker.army[i].new_speed
                        attacker.army[i].turn_left = False
                        if attacker.army[i].battle_actions:
                            for action in attacker.army[i].battle_actions:
                                if action[1] == 0:
                                    attacker.army[i].spells_affected_by.remove(action[0])
                                    attacker.army[i].battle_actions.remove(action)
                                    attacker.army[i].affected_color = ""

                if i < len(defender.army):
                    if defender.army[i].amount > 0:
                        defender.operating_player.war_move_obj(defender.army[i], attacker, battlefield)
                        defender.army[i].turn_left = False
                        defender.army[i].speed_left = defender.army[i].new_speed
                        if defender.army[i].battle_actions:
                            for action in defender.army[i].battle_actions:
                                if action[1] == 0:
                                    defender.army[i].spells_affected_by.remove(action[0])
                                    defender.army[i].battle_actions.remove(action)
                                    defender.army[i].affected_color = ""

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
                    self.heroes.remove(attacker)
                    if type(defender) == Hero:
                        defender.can_throw_spell = True
                    break
                counter = 0
                for u in defender.army:
                    if u.amount <= 0:
                        counter += 1
                if counter == len(defender.army):
                    defender.alive = False
                    battle_loc.has_hero = False
                    battle_loc.hero = None
                    defender.army = []
                    if type(defender) == Hero:
                        defender.operating_player.heroes_left -= 1
                        if defender.operating_player.number != 9:
                            defender.operating_player.heroes.remove(defender)
                    elif type(defender) == Town:
                        self.towns.append(defender)
                        battle_loc.operated_by = self
                        for i in range(len(defender.operating_player.towns)):
                            if defender.operating_player.towns[i].name == battle_loc.town.name:
                                defender.operating_player.towns.pop(i)
                        self.towns[-1].operating_player = self
                        if self.towns[-1].hall_lvl == 4:
                            self.towns[-1].hall_lvl = 3
                        print("You have conquered a town!")
                    attacker.can_throw_spell = True
                    break
        return

    def war_move_obj(self, attacker, defending_hero, battlefield):
        a = attacker
        total_damage_attacker = int(a.amount * a.damage * (a.attack * a.operating_hero.attack * 2 / 100 + 1))
        original_damage_attacker = total_damage_attacker
        original_health_attacker = a.health
        d = None
        defender_loc = None
        total_damage_defender = None
        original_damage_defender = None
        original_health_defender = None
        if a.battle_actions:
            for action in a.battle_actions:
                if action[0] == "slow":
                    a.speed_left -= 2
                    action[1] -= 1
                elif action[0] == "blind":
                    action[1] -= 1
                    time.sleep(0.5)
                    return
                elif action[0] == "haste":
                    a.speed_left += 3
                    action[1] -= 1
                elif action[0] == "bless":
                    a.attack += 10
                    a.speed_left += 1
                    action[1] -= 1
                elif action[0] == "shield":
                    a.defense += 13
                    action[1] -= 1
                elif action[0] == "weakness":
                    a.defense = 0
                    a.damage -= 1
                    action[1] -= 1
                elif action[0] == "curse":
                    a.attack = 0
                    a.damage -= 1
                    action[1] -= 1
                elif action[0] == "bloodlust":
                    a.attack += 7
                    a.damage += 2
                    action[1] -= 1
                elif action[0] == "precision":
                    if a.isranged:
                        a.damage += 4
                    action[1] -= 1
                elif action[0] == "fortune":
                    dice = random.randrange(1, 4)
                    if dice > 1:
                        print(attacker.name + " is lucky this turn!")
                        a.attack += 5
                        a.defense += 5
                        a.damage += 2
                        a.speed_left += 1
                        action[1] -= 1
                elif action[0] == "stoneskin":
                    a.defense += 13
                    action[1] -= 1
        if a.operating_hero.operating_player.number == 9:
            Player.clear_window()
            battlefield.view_battlefield(self, a)
            diff_damage_health = 10000
            for unit in defending_hero.army:
                if unit.health * unit.amount >= total_damage_attacker and \
                        abs(unit.health * unit.amount - total_damage_attacker) < diff_damage_health:
                    if d:
                        if d.isranged:
                            break
                    diff_damage_health = abs(unit.health * unit.amount - total_damage_attacker)
                    d = unit
            if d == None:
                diff_damage_health = 10000
                for unit in defending_hero.army:
                    if abs(unit.health * unit.amount - total_damage_attacker) < diff_damage_health:
                        if d:
                            if d.isranged:
                                break
                        diff_damage_health = abs(unit.health * unit.amount - total_damage_attacker)
                        d = unit
            if d == None:
                input("Could not ID target!")
            if a.isranged == False:
                while a.speed_left > 0:
                    current = battlefield.square[a.location[0]][a.location[1]]
                    prospect = None
                    direction_row = a.location[0] - d.location[0]
                    direction_col = a.location[1] - d.location[1]
                    diff_row = abs(a.location[0] - d.location[0])
                    diff_col = abs(a.location[1] - d.location[1])
                    ss = 0
                    counter = 0
                    move_around = 0
                    total_counter = 0
                    while prospect == None or (prospect.has_hero and prospect.hero != d and move_around < 2) or (prospect.has_hero and move_around >= 2 and prospect.hero.operating_hero == a.operating_hero):
                        total_counter += 1
                        if total_counter > 30:
                            Player.clear_window()
                            battlefield.view_battlefield(self, attacker)
                            print("AI failed to find matching prospect after too many tries.")
                            print(a.name + " targeted " + d.name)
                            if prospect == None:
                                print("Prospect was None!")
                            else:
                                print("Prospect was " + str(prospect.coord))
                            print("Returning in 15 seconds...")
                            time.sleep(15)
                            return
                        if prospect != None and prospect.has_hero and prospect.hero != d:
                            move_around += 1
                            if move_around == 3:
                                counter = 0
                            counter += 1
                            if counter == 1:
                                ss = -1
                            elif counter == 2:
                                ss = 1
                        if diff_col == 0:
                            if direction_row > 0:
                                prospect = battlefield.square[a.location[0]-1][a.location[1]+ss]
                            elif direction_row < 0:
                                prospect = battlefield.square[a.location[0]+1][a.location[1]+ss]
                        elif diff_row == 0:
                            if direction_col > 0:
                                prospect = battlefield.square[a.location[0]+ss][a.location[1]-1]
                            elif direction_col < 0:
                                prospect = battlefield.square[a.location[0]+ss][a.location[1]+1]
                        else:
                            if diff_col > diff_row:
                                if direction_col > 0:
                                    prospect = battlefield.square[a.location[0] + ss][a.location[1] - 1]
                                elif direction_col < 0:
                                    prospect = battlefield.square[a.location[0] + ss][a.location[1] + 1]
                            elif diff_row >= diff_col:
                                if diff_row == 1 and diff_col == 1:
                                    prospect = battlefield.square[d.location[0]][d.location[1]]
                                elif direction_row > 0:
                                    prospect = battlefield.square[a.location[0] - 1][a.location[1] + ss]
                                elif direction_row < 0:
                                    prospect = battlefield.square[a.location[0] + 1][a.location[1] + ss]

                    if prospect.has_hero == False:
                        current.has_hero = False
                        current.hero = None
                        a.location[0], a.location[1] = prospect.coord[0], prospect.coord[1]
                        prospect.has_hero = True
                        prospect.hero = attacker
                        a.speed_left -= 1
                        if a.speed_left == 0:
                            return
                    elif prospect.has_hero and prospect.hero.operating_hero != a.operating_hero:
                        d = prospect.hero
                        break
                    elif prospect.has_hero and prospect.hero.operating_hero == a.operating_hero:
                        print("AI failed to calculate move around own unit.")
                        time.sleep(3)
                        return
        else:
            while True:
                Player.clear_window()
                battlefield.view_battlefield(self, attacker)
                choice = input("Enter commands.\n").lower()
                while choice == "" or choice[0] not in ("q", "w", "e", "a", "s", "d", "z", "x", "o", "r"):
                    choice = input("     Move with QWEASDZX or use commands in the action bar.\n").lower()

                if choice == "r" and attacker.isranged:
                    while True:
                        choice = input("Type unit to range attack:\n").title()
                        for unit in defending_hero.army:
                            if choice[:6] == unit.name[:6] and unit.amount > 0:
                                d = unit
                        if d:
                            break
                        else:
                            print("         Found no unit with that name.")
                            time.sleep(1)

                elif choice == "r" and attacker.isranged == False:
                    print("         This unit does not have a ranged attack!.")
                    time.sleep(1)
                elif choice == "spells":
                    spell_damage = None
                    original_spell_damage = None
                    spell_effect = None
                    spell_cost = None
                    spell_color = None
                    if attacker.operating_hero.can_throw_spell:
                        while True:
                            attacker.operating_hero.view_spells()
                            spell = ""
                            while spell == "":
                                spell = self.dialogue_return("Name the spell you want to throw or ""C"" to cancel.").title()
                            if spell == "C":
                                break
                            target = ""
                            while target == "":
                                target = self.dialogue_return("Name your target or ""C"" to cancel.").title()
                            if target == "C":
                                break
                            for spell_in_book in attacker.operating_hero.spellbook:
                                if spell == spell_in_book.get("name"):
                                    spell_damage = spell_in_book.get("damage")
                                    spell_effect = spell_in_book.get("effect").lower()
                                    spell_cost = spell_in_book.get("cost")
                                    if "color" in spell_in_book:
                                        spell_color = spell_in_book.get("color")
                            if spell_cost == None:
                                self.dialogue_display("No such spell found.")
                            elif spell_cost > attacker.operating_hero.spell_points:
                                self.dialogue_display("You don't have the spell points.")
                            elif spell_effect != "quicksand" and spell != "Summon Boat":
                                if spell_effect:
                                    if spell_color == "red":
                                        for unit in defending_hero.army:
                                            if target[:7] == unit.name[:7]:
                                                d = unit
                                    elif spell_color == "green":
                                        for unit in a.operating_hero.army:
                                            if target[:7] == unit.name[:7]:
                                                d = unit
                                else:
                                    for unit in defending_hero.army:
                                        if target[:7] == unit.name[:7]:
                                            d = unit
                                if d == None:
                                    print("         Found no unit with that name.")
                                else:
                                    if spell_effect == "cure":
                                        a.operating_hero.spell_points -= spell_cost
                                        a.operating_hero.can_throw_spell = False
                                        d.health = d.orig_health
                                        self.dialogue_display(a.operating_hero.name + " throws  " + spell + " at " +
                                                              d.name, "", "healing all hit points!")
                                        d = None
                                        break
                                    elif spell_damage:
                                        a.operating_hero.spell_points -= spell_cost
                                        a.operating_hero.can_throw_spell = False
                                        original_spell_damage = spell_damage * a.operating_hero.spell_power
                                        original_health_defender = d.health
                                        new_loc = battlefield.square[d.location[0]][d.location[1]]
                                        d.health -= spell_damage * a.operating_hero.spell_power
                                        d.health = int(d.health)
                                        spell_damage -= original_health_defender
                                        while d.health <= 0:
                                            d.amount -= 1
                                            d.health = original_health_defender
                                            if spell_damage > 0:
                                                d.health -= spell_damage
                                                spell_damage -= original_health_defender
                                        if d.amount < 1:
                                            new_loc.has_hero = False
                                            new_loc.hero = None
                                        self.dialogue_display(a.operating_hero.name + " throws  " + spell + " at " +
                                                            d.name, "", "for " + str(original_spell_damage) + " damage!")
                                        d = None
                                        break
                                    else:
                                        if spell_effect not in d.spells_affected_by:
                                            a.operating_hero.spell_points -= spell_cost
                                            a.operating_hero.can_throw_spell = False
                                            if spell_color:
                                                d.affected_color = spell_color
                                            d.spells_affected_by.append(spell_effect)
                                            d.battle_actions.append([spell_effect, a.operating_hero.spell_power])
                                            self.dialogue_display(a.operating_hero.name + " throws  " + spell + " at " +
                                                        d.name + "!")
                                            d = None
                                            break
                                        else:
                                            print("         Unit already affected by " + spell_effect + ".")
                                            time.sleep(1)
                    else:
                        print("         You have already thrown a spell this cycle.")
                        time.sleep(1)
                else:
                    for i in range(len(choice)):
                        old_pos = a.location
                        new_pos = [0, 0]
                        if choice[i] == "q":
                            new_pos[0], new_pos[1] = old_pos[0] - 1, old_pos[1] - 1
                        elif choice[i] == "w":
                            new_pos[0], new_pos[1] = old_pos[0] - 1, old_pos[1]
                        elif choice[i] == "e":
                            new_pos[0], new_pos[1] = old_pos[0] - 1, old_pos[1] + 1
                        elif choice[i] == "a":
                            new_pos[0], new_pos[1] = old_pos[0], old_pos[1] - 1
                        elif choice[i] == "s":
                            new_pos[0], new_pos[1] = old_pos[0] + 1, old_pos[1]
                        elif choice[i] == "d":
                            new_pos[0], new_pos[1] = old_pos[0], old_pos[1] + 1
                        elif choice[i] == "z":
                            new_pos[0], new_pos[1] = old_pos[0] + 1, old_pos[1] - 1
                        elif choice[i] == "x":
                            new_pos[0], new_pos[1] = old_pos[0] + 1, old_pos[1] + 1
                        elif choice[i] == "o":
                            print("     Ending turn.")
                            time.sleep(1)
                            return
                        else:
                            print("     Invalid input.")
                            time.sleep(1)
                            break
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
                        if new_loc.speed_drain <= a.speed_left:
                            if new_loc.has_hero == False:
                                a.speed_left -= new_loc.speed_drain
                                new_loc.has_hero = True
                                new_loc.hero = a
                                a.location = new_pos
                                old_loc.has_hero = False
                                old_loc.hero = None
                                if a.speed_left == 0:
                                    print("No more speed left. Ending turn now.")
                                    time.sleep(0.5)
                                    return
                            elif new_loc.has_hero and new_loc.hero.operating_hero == a.operating_hero:
                                print("You already have a Unit standing there.")
                                time.sleep(0.5)
                            elif new_loc.has_hero and new_loc.hero.operating_hero != a.operating_hero:
                                d = new_loc.hero
                                break
                    if d:
                        break
                if d:
                    break

        attacker_loc = battlefield.square[a.location[0]][a.location[1]]
        defender_loc = battlefield.square[d.location[0]][d.location[1]]
        if a.isranged == False:
            a.speed_left -= defender_loc.speed_drain
        original_health_defender = d.health
        if type(d.operating_hero) == Hero:
            d.health -= total_damage_attacker / ((d.defense + d.operating_hero.defense) * 2 / 100 + 1)
        else:
            d.health -= total_damage_attacker / (d.operating_hero.defense * 2 / 100 + 1)
        d.health = int(d.health)
        total_damage_attacker -= original_health_defender
        while d.health <= 0:
            d.amount -= 1
            d.health = original_health_defender
            if total_damage_attacker > 0:
                d.health -= total_damage_attacker
                total_damage_attacker -= original_health_defender
        if d.amount < 1:
            defender_loc.has_hero = False
            defender_loc.hero = None

        if a.isranged == False and defender_loc.has_hero and d.has_retaliated == False:
            if type(d.operating_hero) == Hero:
                total_damage_defender = d.amount * d.damage * ((d.attack + d.operating_hero.attack) * 2 / 100 + 1)
            else:
                total_damage_defender = d.amount * d.damage * (d.attack * 2 / 100 + 1)
            total_damage_defender = int(total_damage_defender)
            original_damage_defender = total_damage_defender
            if type(attacker.operating_hero) == Hero:
                a.health -= total_damage_defender / ((a.defense + a.operating_hero.defense) * 2 / 100 + 1)
            else:
                a.health -= total_damage_defender / (a.operating_hero.defense * 2 / 100 + 1)
            a.health = int(a.health)
            total_damage_defender -= original_health_attacker
            while a.health <= 0:
                a.amount -= 1
                a.health = original_health_attacker
                if total_damage_defender > 0:
                    a.health -= total_damage_defender
                    total_damage_defender -= original_health_attacker
            if a.amount < 1:
                attacker_loc.has_hero = False
                attacker_loc.hero = None
            d.has_retaliated = True

        if a.isranged:
            self.dialogue_display(a.name + " shoots " + d.name, " with " + str(original_damage_attacker) + " damage!")

        elif d.has_retaliated == True and original_damage_defender is not None:
            self.dialogue_display(a.name + " attacks " + d.name, " with " +  str(original_damage_attacker) +
                " damage!", d.name + " retaliates with ", str(original_damage_defender) + " damage!")
        else:
            self.dialogue_display(a.name + " attacks " + d.name, " with " + str(original_damage_attacker) + "!")

    def enter_town(self, town, map):
        if town.render == None:
            town.render = Gameboard(10, 12, False)
        while True:
            Player.clear_window()
            Renderer.renderer(town)
            town.render.view_town(town, self)
            visiting_hero = map.square[town.location[0]][town.location[1]].hero
            if visiting_hero and visiting_hero.spellbook != [] and town.guild_lvl > 0:
                for level in town.spellbook:
                    for spell in level:
                        if spell not in visiting_hero.spellbook:
                            visiting_hero.spellbook.append(spell)
            choice = self.dialogue_return("What do you want to do?").lower()
            while choice not in("build", "recruit", "mage guild", "tavern", "view", "exit"):
                choice = self.dialogue_return("See the upper action bar for available commands.").lower()
            if choice == "mage guild":
                if town.guild_lvl > 0:
                    if visiting_hero and visiting_hero.spellbook == []:
                        choice9 = "not yet"
                        while choice9 != "":
                            choice9 = self.dialogue_return(map.square[town.location[0]][town.location[1]].hero.name +
                                              " does not own a spellbook. ", "Do you wish to purchase one for 500 gold?",
                                              "Enter to purchase, ""C"" to cancel")
                            if choice9 == "" and self.gold > 499:
                                self.gold -= 500
                                self.dialogue_display("You purchased a spellbook!")
                                visiting_hero.can_throw_spell = True
                                for level in town.spellbook:
                                    for spell in level:
                                        if spell not in visiting_hero.spellbook:
                                            visiting_hero.spellbook.append(spell)
                            else:
                                self.dialogue_display("You lack the necessary funds!")
                    town.view_spells()
                else:
                    self.dialogue_display("This town does not have a Mage Guild.")
            elif choice == "build":
                if town.has_built:
                    self.dialogue_display("You can only build once per turn.")
                else:
                    see_price = ""
                    while see_price.title() not in town.buildings_available:
                        see_price = self.dialogue_return(str(town.buildings_available), "",
                                                         "Type a building to see its price.").lower()
                    for entry in town.buildings_prices:
                        if see_price.title() == entry.get("name"):
                            prices = entry.get("price")
                            prices_string = ""
                            for resource, price in prices.items():
                                prices_string = prices_string + price + " "
                                prices_string = prices_string + resource + ", "
                            choice = self.dialogue_return(entry.get("name"), " Requirements: " + entry.get("req") + ". Price: "
                                    + prices_string, "Press Enter to construct this building. ",
                                                          "Type ""C"" to cancel.").lower()
                            if choice != "c":
                                funds = True
                                for resource in prices.keys():
                                    if resource in vars(self):
                                        if vars(self).get(resource) < int(prices.get(resource)):
                                            funds = False
                                req_fulfilled = True
                                if funds:
                                    if see_price.title() == "Capitol":
                                        if town.town_lvl != 3:
                                            req_fulfilled = False
                                        else:
                                            town.hall_lvl = 4
                                            self.dailyg += 2000
                                            town.buildings_available[0] = ""
                                    elif see_price.title() == "City Hall":
                                        if town.guild_lvl != 1:
                                            req_fulfilled = False
                                        else:
                                            town.hall_lvl = 3
                                            self.dailyg += 1000
                                            town.buildings_available[0] = "Capitol"
                                    elif see_price.title() == "Town Hall":
                                        town.hall_lvl = 2
                                        self.dailyg += 500
                                        town.buildings_available[0] = "City Hall"
                                    elif see_price.title() == "Citadel":
                                        town.town_lvl = 2
                                        town.buildings_available[1] = "Castle"
                                    elif see_price.title() == "Castle":
                                        town.town_lvl = 3
                                        town.buildings_available[1] = ""
                                    elif see_price[:10].title() == "Mage Guild":
                                        town.guild_lvl = int(see_price[11:])
                                        town.spellbook.append(town.spells_to_gain[town.guild_lvl-1])
                                        if town.guild_lvl < 5:
                                            if town.guild_lvl == 4 and town.kingdom == "Castle":
                                                town.buildings_available[2] = ""
                                            else:
                                                town.buildings_available[2] = see_price[:11].title() + \
                                                                              str(town.guild_lvl+1)
                                        else:
                                            town.buildings_available[2] = ""
                                    elif entry.get("type") == "dw3":
                                            town.hasdw3 = True
                                            town.dw3amount = 6
                                            town.buildings_available.remove(town.dw_names[2])
                                    elif entry.get("type") == "dw4":
                                            town.hasdw4 = True
                                            town.dw4amount = 4
                                            town.buildings_available.remove(town.dw_names[3])
                                    elif entry.get("type") == "dw5":
                                        if town.guild_lvl < 2 or town.hasdw4 == False:
                                            req_fulfilled = False
                                        else:
                                            town.hasdw5 = True
                                            town.dw5amount = 3
                                            town.buildings_available.remove(town.dw_names[4])
                                    elif entry.get("type") == "dw6":
                                        if town.hasdw5 == False:
                                            req_fulfilled = False
                                        else:
                                            town.hasdw6 = True
                                            town.dw6amount = 2
                                            town.buildings_available.remove(town.dw_names[5])
                                    elif entry.get("type") == "dw7":
                                        if town.guild_lvl < 3 or town.hasdw5 == False:
                                            req_fulfilled = False
                                        else:
                                            town.hasdw7 = True
                                            town.dw7amount = 1
                                            town.buildings_available.remove(town.dw_names[6])
                                    if req_fulfilled:
                                        for resource in prices.keys():
                                            if resource in vars(self):
                                                vars(self)[resource] -= int(prices.get(resource))
                                        town.has_built = True
                                        break
                                    else:
                                        self.dialogue_display("You lack the necessary requirements.")
                                else:
                                    self.dialogue_display("You lack the necessary funds.")
                            else:
                                break
            elif choice == "tavern":
                if map.square[town.location[0]][town.location[1]].has_hero:
                    self.dialogue_display("You cannot hire a new hero while your town is occupied by another hero.")
                elif self.has_hired:
                    self.dialogue_display("You have already hired a hero this week.")
                else:
                    choice = self.dialogue_return("Hiring a new hero costs 2500 gold.", "", "Press Enter to hire. Press C to cancel.").lower()
                    if self.hero_ticker == 3:
                        self.dialogue_display("Unfortunately there are only three heroes per player.")
                    elif choice != "c" and self.gold >= 2500:
                        self.create_heroes(town.location, map)
                        self.gold -= 2500
                        self.has_hired = True
                        self.dialogue_display("Hero hired! Press Enter to return to map.")
                        return
                    elif choice != "c" and self.gold < 2500:
                        self.dialogue_display("You lack the necessary funds.")

            elif choice == "recruit":
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
                                                         "Type \"C\" to cancel.").title()
                    if see_price == "C":
                        break
                    else:
                        for i in range(7):
                            if see_price == list(town.unit_names)[i]:
                                available_stack = 0
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
                                while amount == "" or amount[0] not in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "C", "c"):
                                    amount = self.dialogue_return(see_price + ".",
                                                                  " Price: " + str(
                                                                      town.unit_names.get(see_price)) + " gold.",
                                                                  str(available_stack) + " available.",
                                                                  " Type the amount to recruit or C to cancel.")
                                if amount == "C" or amount == "c":
                                    break
                                else:
                                    amount = int(amount)
                                    found = False
                                    if amount * town.unit_names.get(
                                            see_price) <= self.gold and amount <= available_stack:
                                        if len(visiting_hero.army) == 7:
                                            for unit in visiting_hero.army:
                                                if unit.name == see_price:
                                                    found = True
                                                    self.dialogue_display(
                                                        "Your army has run out of space.", "",
                                                        "The unit will recruit to first existing stack.")
                                                    break
                                            if not found:
                                                self.dialogue_display("Your army is full! Press Enter to exit.")
                                                break
                                        if found:
                                            visiting_hero.create_unit(town.kingdom, see_price, amount, True)
                                        else:
                                            visiting_hero.create_unit(town.kingdom, see_price, amount)
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
                                        self.gold -= amount * town.unit_names.get(see_price)
                                        self.dialogue_return(str(amount) + " " + see_price + " recruited!")
                                    else:
                                        self.dialogue_display("You either do not have the gold", "",
                                                              "or lack available units.")
            elif choice == "view":
                self.view_info()
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
        self.buildings_available = ["Town Hall", "Citadel", "Mage Guild 1"]
        self.has_built = False
        self.dw_names = []
        self.unit_names = {}
        self.dw_color = ""
        self.spellbook = []
        self.spells_to_gain = []
        self.buildings_prices = [{"name":"Town Hall", "req": "None", "price":{"gold":"2500"}},
                                 {"name":"City Hall", "req": "Mage Guild Lvl 1", "price":{"gold":"5000"}},
                                 {"name":"Capitol", "req": "Castle", "price":{"gold":"10000"}},
                                 {"name":"Citadel", "req": "None", "price":{"gold":"2500", "stone": "5"}},
                                 {"name":"Castle", "req": "None", "price":{"gold":"5000", "wood": "10", "stone": "10"}},
                                 {"name":"Mage Guild 1", "req": "None", "price":{"gold":"2000", "wood": "5", "stone": "5"}},
                                 {"name":"Mage Guild 2", "req": "None", "price":{"gold":"1000", "wood": "5", "stone":
                                     "5", "mercury":"4", "crystal":"4", "gems":"4", "sulfur":"4"}},
                                 {"name":"Mage Guild 3", "req": "None", "price":{"gold":"1000", "wood": "5", "stone":
                                     "5", "mercury":"6", "crystal":"6", "gems":"6", "sulfur":"6"}},
                                 {"name":"Mage Guild 4", "req": "None", "price":{"gold":"1000", "wood": "5", "stone":
                                     "5", "mercury":"8", "crystal":"8", "gems":"8", "sulfur":"8"}},
                                 {"name":"Mage Guild 5", "req": "None", "price":{"gold":"1000", "wood": "5", "stone":
                                     "5", "mercury":"10", "crystal":"10", "gems":"10", "sulfur":"10"}},
                                 {"name": "dw3", "req": "None", "type": "dw3", "price": {}},
                                 {"name": "dw4", "req": "None", "type": "dw4", "price": {}},
                                 {"name": "dw5", "req": "", "type": "dw5", "price": {}},
                                 {"name": "dw6", "req": "", "type": "dw6", "price": {}},
                                 {"name": "dw7", "req": "", "type": "dw7", "price": {}}]

        if self.kingdom == "Castle":
            self.dw_names = ["Guardhouse", "Archery", "Griffin Tower", "Barracks", "Monastery", "Training Grounds", "Portal Of Glory"]
            self.unit_names = {"Pikeman":60, "Archer":100, "Griffin":200, "Swordsman":300, "Monk":400,
                               "Cavalier":1000, "Angel":1000}
            self.buildings_available.extend(self.dw_names[2:7])
            for i in range(len(self.dw_names) + 1):
                for entry in self.buildings_prices:
                    if "type" in entry:
                        if i == int(entry.get("type")[2:3]):
                            entry["name"] = self.dw_names[i-1]
                            if i == 3:
                                entry["price"] = {"gold" : "1000", "stone": "5"}
                            elif i == 4:
                                entry["price"] = {"gold" : "2000", "stone": "5"}
                            elif i == 5:
                                entry["price"] = {"gold": "3000", "wood": "5", "stone": "5", "mercury":"2", "crystal":"2", "gems":"2", "sulfur":"2"}
                                entry["req"] = "Mage Guild 2, " + self.dw_names[3]
                            elif i == 6:
                                entry["price"] = {"gold": "5000", "wood": "30"}
                                entry["req"] = self.dw_names[4]
                            elif i == 7:
                                entry["price"] = {"gold": "20000", "mercury":"10", "crystal":"10", "gems":"10", "sulfur":"10"}
                                entry["req"] = "Mage Guild 3, " + self.dw_names[4]
            self.spells_to_gain.append([{"name": "Magic Arrow", "cost": 4, "damage": 10, "effect": ""},
                                        {"name": "Haste", "cost": 4, "damage": "", "effect": "haste", "color":"green"},
                                        {"name": "Bless", "cost": 4, "damage": 0, "effect": "bless", "color":"green"},
                                        {"name": "Shield", "cost": 4, "damage": 0, "effect": "shield", "color":"green"},
                                        {"name": "Cure", "cost": 4, "damage": 0, "effect": "cure", "color":"green"}
                                        ])
            self.spells_to_gain.append([{"name": "Ice Bolt", "cost": 6, "damage": 15, "effect": ""},
                                        {"name": "Precision", "cost": 5, "damage": 0, "effect": "precision", "color": "green"},
                                        {"name": "Summon Boat", "cost": 7, "damage": 0, "effect": "Navigate water."},
                                        {"name": "Lightning Bolt", "cost": 8, "damage": 20, "effect": ""}
                                        ])
            self.dw_color = '\033[6;37;43m'

        elif self.kingdom == "Inferno":
            self.dw_names = ["Imp Crucible", "Hall Of Sins", "Kennels", "Demon Gate", "Hell Hole", "Fire Lake",
                             "Forsaken Palace"]
            self.unit_names = {"Imp":60, "Gog":125, "Hellhound":200, "Demon":250, "Pit Fiend":500, "Efreet":900, "Devil":2700}
            self.buildings_available.extend(self.dw_names[2:7])
            for i in range(len(self.dw_names) + 1):
                for entry in self.buildings_prices:
                    if "type" in entry:
                        if i == int(entry.get("type")[2:3]):
                            entry["name"] = self.dw_names[i-1]
                            if i == 3:
                                entry["price"] = {"gold" : "1500", "wood": "10"}
                            elif i == 4:
                                entry["price"] = {"gold" : "2000", "wood": "5", "stone": "5"}
                            elif i == 5:
                                entry["price"] = {"gold": "3000"}
                                entry["req"] = "Mage Guild 2, " + self.dw_names[3]
                            elif i == 6:
                                entry["price"] = {"gold": "4000", "stone": "10", "mercury":"3", "gems":"3", "sulfur":"3"}
                                entry["req"] = self.dw_names[4]
                            elif i == 7:
                                entry["price"] = {"gold": "15000", "wood": "10", "stone": "10", "mercury":"20"}
                                entry["req"] = "Mage Guild 3, " + self.dw_names[4]
            self.spells_to_gain.append([{"name": "Magic Arrow", "cost": 4, "damage": 10, "effect": ""},
                                        {"name": "Curse", "cost": 4, "damage": 0, "effect": "curse", "color": "red"},
                                        {"name": "Bloodlust", "cost": 4, "damage": 0, "effect": "bloodlust", "color": "green"},
                                        {"name": "Slow", "cost": 4, "damage": 0, "effect": "slow", "color": "red"},
                                        {"name": "Stone Skin", "cost": 4, "damage": 0, "effect": "stoneskin", "color": "green"}
                                        ])

            self.spells_to_gain.append([{"name": "Lightning Bolt", "cost": 8, "damage": 20, "effect": ""},
                                        {"name": "Blind", "cost": 5, "damage": 0, "effect": "blind", "color": "red"},
                                        {"name": "Summon Boat", "cost": 7, "damage": 0, "effect": "Navigate water."},
                                        {"name": "Weakness", "cost": 4, "damage": 20, "effect": "weakness", "color": "red"}
                                        ])
            self.dw_color = '\033[6;37;41m'

        elif self.kingdom == "Rampart":
            self.dw_names = ["Centaur Stables", "Dwarf Cottage", "Homestead", "Enchanted Spring", "Dendroid Arches", "Unicorn Glade",
                             "Dragon Cliffs"]
            self.unit_names = {"Centaur":70, "Dwarf":120, "Wood Elf":200, "Pegasus":250, "Dendroid Guard":350, "Unicorn":850, "Green Dragon":2400}
            self.buildings_available.extend(self.dw_names[2:7])
            for i in range(len(self.dw_names) + 1):
                for entry in self.buildings_prices:
                    if "type" in entry:
                        if i == int(entry.get("type")[2:3]):
                            entry["name"] = self.dw_names[i-1]
                            if i == 3:
                                entry["price"] = {"gold" : "1500", "wood": "10"}
                            elif i == 4:
                                entry["price"] = {"gold" : "2000", "crystal": "5"}
                            elif i == 5:
                                entry["price"] = {"gold": "2500"}
                                entry["req"] = "Mage Guild 2, " + self.dw_names[3]
                            elif i == 6:
                                entry["price"] = {"gold": "4000", "wood": "5", "stone": "5", "gems":"6"}
                                entry["req"] = self.dw_names[4]
                            elif i == 7:
                                entry["price"] = {"gold": "10000", "stone": "20", "crystal":"14"}
                                entry["req"] = "Mage Guild 3, " + self.dw_names[4]
            self.spells_to_gain.append([{"name": "Magic Arrow", "cost": 4, "damage": 10, "effect": ""},
                                        {"name": "Haste", "cost": 4, "damage": 0, "effect": "haste", "color": "green"},
                                        {"name": "Bless", "cost": 4, "damage": 0, "effect": "bless", "color": "green"},
                                        {"name": "Slow", "cost": 4, "damage": 0, "effect": "slow", "color": "red"},
                                        {"name": "Dispel", "cost": 4, "damage": 0, "effect": "dispel"}
                                        ])
            self.spells_to_gain.append([{"name": "Lightning Bolt", "cost": 8, "damage": 20, "effect": ""},
                                        {"name": "Fortune", "cost": 5, "damage": 0, "effect": "fortune", "color": "green"},
                                        {"name": "Summon Boat", "cost": 7, "damage": 0, "effect": "Navigate water."},
                                        {"name": "Quicksand", "cost": 4, "damage": 0, "effect": "quicksand"}
                                        ])
            self.dw_color = '\033[6;37;42m'

        elif self.kingdom == "Tower":
            self.dw_names = ["Workshop", "Parapet", "Golem Factory", "Mage Tower", "Altar Of Wishes", "Golden Pavilion",
                             "Cloud Temple"]
            self.unit_names = {"Gremlin": 30, "Stone Gargoyle": 130, "Stone Golem": 150, "Mage": 350, "Genie": 850, "Naga": 1100,
                               "Giant": 2000}
            self.buildings_available.extend(self.dw_names[2:7])
            for i in range(len(self.dw_names) + 1):
                for entry in self.buildings_prices:
                    if "type" in entry:
                        if i == int(entry.get("type")[2:3]):
                            entry["name"] = self.dw_names[i - 1]
                            if i == 3:
                                entry["price"] = {"gold": "2000", "wood": "5", "stone": "5"}
                            elif i == 4:
                                entry["price"] = {"gold": "2500", "wood": "5", "stone": "5", "mercury":"3", "crystal": "3", "gems":"3", "sulfur":"3"}
                            elif i == 5:
                                entry["price"] = {"gold": "3000", "wood": "5", "stone": "5", "crystal": "2", "gems":"2"}
                                entry["req"] = "Mage Guild 2, " + self.dw_names[3]
                            elif i == 6:
                                entry["price"] = {"gold": "4000", "wood": "5", "stone": "5", "mercury":"2", "crystal": "2", "gems":"2", "sulfur":"2"}
                                entry["req"] = self.dw_names[4]
                            elif i == 7:
                                entry["price"] = {"gold": "5000", "wood": "10", "stone": "10", "gems": "6"}
                                entry["req"] = "Mage Guild 3, " + self.dw_names[4]
            self.spells_to_gain.append([{"name": "Magic Arrow", "cost": 4, "damage": 10, "effect": ""},
                                        {"name": "Haste", "cost": 4, "damage": 0, "effect": "haste", "color": "green"},
                                        {"name": "Bless", "cost": 4, "damage": 0, "effect": "bless", "color": "green"},
                                        {"name": "Slow", "cost": 4, "damage": 0, "effect": "slow", "color": "red"},
                                        {"name": "Stone Skin", "cost": 4, "damage": 0, "effect": "stoneskin", "color": "green"}
                                        ])
            self.spells_to_gain.append([{"name": "Lightning Bolt", "cost": 8, "damage": 20, "effect": ""},
                                        {"name": "Fortune", "cost": 5, "damage": 0, "effect": "fortune", "color": "green"},
                                        {"name": "Summon Boat", "cost": 7, "damage": 0, "effect": "Navigate water."},
                                        {"name": "Quicksand", "cost": 4, "damage": 0, "effect": "quicksand"}
                                        ])
            self.dw_color = '\033[6;34;47m'

    def view_spells(self):
        print("")
        print("" + '{:^40s}'.format("Spells of: " + self.name))
        print("|" + '{:-^40s}'.format("") + "|")
        for level in range(len(self.spellbook)):
            print("|" + '{:-^40s}'.format(" Level " + str(level) + " ") + "|")
            for spell in self.spellbook[level]:
                print("|" + '{:-^40s}'.format("  " + spell.get("name") + ", Cost: " + str(spell.get("cost")) + " spell points.") + "|")
                print("|" + '{:-^40s}'.format(" Effect: " + spell.get("effect") + " Damage: " + str(spell.get("damage"))) + "|")
                print("|" + '{:-^40s}'.format("") + "|")
        input("\n")

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
        self.orig_attack = input_attack
        self.orig_defense = input_defense
        self.orig_damage = input_damage
        self.orig_health = input_health
        self.speed_left = 0
        self.new_speed = input_speed
        self.start_location = [input_rank, 0]
        self.location = [0,0]
        self.operating_hero = input_hero
        self.isranged = input_ranger
        self.has_retaliated = False
        self.turn_left = True
        self.spells_affected_by = []
        self.battle_actions = []
        self.price = input_cost
        self.affected_color = ""

    def __str__(self):
        return self.name

class Hero:
    def __init__(self, input_name, input_kind, input_attack, input_defense, input_knowledge, input_spellpower,
                 input_player, input_spellbook = []):
        self.name = input_name
        self.kind = input_kind
        self.level = 1
        self.attack = input_attack
        self.defense = input_defense
        self.knowledge = input_knowledge
        self.spell_points = self.knowledge * 10
        self.spell_power = input_spellpower
        self.operating_player = input_player
        self.alive = True
        self.location = [0, 0]
        self.army = []
        self.artefacts = []
        self.speed_left = 10
        self.new_speed = 10
        self.spellbook = input_spellbook
        self.can_throw_spell = False
        self.has_boat = False

        if self.kind == "monster":
            self.level == "0"

        if self.spellbook != []:
            self.can_throw_spell = True

    def __str__(self):
        if self.alive:
            return f'{self.name}'

    def speed_bar(self):
        speedbar = "    Hero speed left:    \033[102m"
        count = self.speed_left
        for i in range(20):
            if count > 0:
                speedbar += "  "
                count -= 1
        speedbar += "\033[0m Forest (\033[42m \033[0m) drain twice as many movement points as hills and plains " \
                    "(\033[102m \033[43m \033[0m). Mountain (\033[100m \033[0m) drain eight times points.\n"
        return speedbar

    def view_spells(self):
        print("")
        print("" + '{:^40s}'.format("Spells of: " + self.name + ", with " + str(self.spell_points) + " spell points."))
        print("|" + '{:-^40s}'.format("") + "|")
        for spell in self.spellbook:
            print("|" + '{:-^40s}'.format(
                "  " + spell.get("name") + ", Cost: " + str(spell.get("cost")) + " spell points.") + "|")
            print("|" + '{:-^40s}'.format(" Effect: " + spell.get("effect") + " Damage: " + str(spell.get("damage") * self.spell_power)) + "|")
            print("|" + '{:-^40s}'.format("") + "|")
        input("\n")

    def create_monster_army(self, amount, stacks):
        for i in range(stacks):
            self.create_unit("monster", self.name, amount)
        self.name = self.army[0].name

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
        elif kingdom == "monster":
            if unit == "dw1":
                new_unit = Unit("Gnoll", 1, amount, 3, 3, 2, 4, 4, 30, self)
            elif unit == "dw2 ranged":
                new_unit = Unit("Archer", 2, amount, 6, 3, 2, 10, 4, 100, self, True)
            elif unit == "dw2":
                new_unit = Unit("Wolf Raider", 2, amount, 5, 4, 2, 10, 5, 60, self)
            elif unit == "dw3":
                new_unit = Unit("Serpent Fly", 3, amount, 7, 9, 4, 20, 9, 220, self)
            elif unit == "dw4 ranged":
                new_unit = Unit("Mage", 4, amount, 11, 8, 8, 25, 5, 350, self, True)
            elif unit == "dw5":
                new_unit = Unit("Earth Elemental", 5, amount, 10, 10, 7, 40, 4, 400, self)
            elif unit == "dw6":
                new_unit = Unit("Psychic Elemental", 6, amount, 15, 13, 15, 75, 7, 750, self)
            elif unit == "dw7 good":
                new_unit = Unit("Angel", 7, amount, 20, 20, 50, 200, 12, 3000, self)
            elif unit == "dw7 evil":
                new_unit = Unit("Behemoth", 7, amount, 19, 16, 50, 150, 7, 2000, self)
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
                location.operated_by != player:
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
        match location.object_name:
            case "XP_stone":
                if self.name not in location.met_heroes:
                    self.level += 1
                    location.met_heroes.append(self.name)
                    choice = ""
                    while choice not in("Attack", "Defense", "Knowledge", "Spell Power"):
                        choice = player.dialogue_return("You have gained a level!", "",
                                                        "Type the skill you want to increase.").title()
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
                    player.dialogue_display(self.name + " finds an old sword. It's blade is still sharp.","", "Attack increased by 2!")
                    self.attack += 2
                    self.artefacts.append("sword")
                    location.has_object = False
                    location.object_name = ""
            case "Shield":
                player.dialogue_display(self.name + " finds a shield of power.", "", "Defense increased by 3.")
                self.defense += 3
                self.artefacts.append("shield")
                location.has_object = False
                location.object_name = ""
            case "Boots":
                player.dialogue_display(self.name + " finds Boots of Speed.", "", "Speed increased by 3.")
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
                                                            "Type the skill you want to increase.").title()
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
            case "Shrine1":
                if self.spellbook == []:
                    player.dialogue_display("This shrine has magic instructions for the spell ""Summon boat"", "
                                            "but " + self.name + " lacks a spellbook.")
                else:
                    player.dialogue_display("This shrine has magic instructions for the spell ""Summon boat"", "
                                            "and " + self.name + " scribbles it down.")
                    self.spellbook.append({"name": "Summon Boat", "cost": 7, "damage": 0, "effect": "Navigate water."})
            case "Shrine2":
                if self.spellbook == []:
                    player.dialogue_display("This shrine has magic instructions for the spell ""Implosion"", "
                                            "but " + self.name + " lacks a spellbook.")
                else:
                    player.dialogue_display("This shrine has magic instructions for the spell ""Implosion"", "
                                            "and " + self.name + " scribbles it down.")
                    self.spellbook.append({"name": "Implosion", "cost": 40, "damage": 60, "effect": ""})

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
                if map:
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
                            speed_drain = 2
                        else:
                            dice = 0
                elif cols == 12:
                    kind = ""
                else:
                    kind = "battlefield"
                    speed_drain = 1
                landscape = Landscape(kind, [i,j], speed_drain)
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
                            self.square[i][j].kind = "hills"
                            self.square[i][j].color = '\033[102m'
                            self.square[i][j].speed_drain = 1
                    elif self.square[i][j].kind == "water":
                        counter = 0
                        for c in range(-1, 2):
                            for d in range(-1, 2):
                                if self.square[i+c][j+d].kind == "water":
                                    counter += 1
                        if counter < 3:
                            self.square[i][j].kind = "hills"
                            self.square[i][j].color = '\033[102m'
                            self.square[i][j].speed_drain = 1

    def populator(self, input_rows, input_cols, number_of_players):
        for i in range(number_of_players):
            start_row = 0
            end_row = 0
            start_col = 0
            end_col = 0
            mines = ["wood", "stone", "mercury", "crystal", "gems", "sulfur", "gold"]
            chests = ["Treasure", "Treasure", "Treasure", "Treasure"]
            buildings = ["XP_stone", "Pool", "Shrine1", "Shrine2"]
            artefacts = ["Sword", "Shield", "Boots"]
            computer = Player("Computer", 9, "")
            archer = Hero("dw2 ranged", "monster", 1, 1, 1, 1, computer)
            archer2 = Hero("dw2 ranged", "monster", 1, 1, 1, 1, computer)
            archer.create_monster_army(5, 3)
            archer2.create_monster_army(5, 3)
            wolf_raider = Hero("dw2", "monster", 1, 1, 1, 1, computer)
            wolf_raider2 = Hero("dw2", "monster", 1, 1, 1, 1, computer)
            wolf_raider.create_monster_army(8, 3)
            wolf_raider2.create_monster_army(8, 3)
            angel = Hero("dw7 good", "monster", 1, 1, 1, 1, computer)
            angel.create_monster_army(1, 2)
            behemoth = Hero("Behemoth", "monster", 1, 1, 1, 1, computer)
            behemoth.create_unit("monster", "dw7 evil", 2)
            mage = Hero("dw4 ranged", "monster", 1, 1, 1, 1, computer)
            mage2 = Hero("dw4 ranged", "monster", 1, 1, 1, 1, computer)
            mage.create_monster_army(4, 4)
            mage2.create_monster_army(4, 4)
            serpent_fly = Hero("dw3", "monster", 1, 1, 1, 1, computer)
            serpent_fly2 = Hero("dw3", "monster", 1, 1, 1, 1, computer)
            serpent_fly.create_monster_army(4, 5)
            serpent_fly2.create_monster_army(4, 5)
            enemies = [archer, angel, mage, serpent_fly, archer2, wolf_raider, behemoth, serpent_fly2, wolf_raider2, mage2]
            if i == 0:
                start_row = 0
                end_row = int(input_rows / 2 - 1)
                start_col = 0
                if number_of_players < 3:
                    end_col = input_cols
                else:
                    end_col = int(input_cols / 2)
            elif i == 1:
                start_row = int(input_rows / 2)
                end_row = input_rows
                start_col = 0
                if number_of_players < 3:
                    end_col = input_cols
                else:
                    end_col = int(input_cols / 2)
            elif i == 2:
                start_row = 0
                end_row = int(input_rows / 2)
                start_col = int(input_cols / 2)
                end_col = input_cols
            elif i == 3:
                start_row = int(input_rows / 2)
                end_row = input_rows
                start_col = int(input_cols / 2)
                end_col = input_cols

            self.populate(mines, start_row, end_row, start_col, end_col)
            self.populate(chests, start_row, end_row, start_col, end_col)
            self.populate(buildings, start_row, end_row, start_col, end_col)
            self.populate(artefacts, start_row, end_row, start_col, end_col)
            self.populate(enemies, start_row, end_row, start_col, end_col)

    def populate(self, lst, start_row, end_row, start_col, end_col):
        while len(lst) > 0:
            dice_row = random.randrange(start_row, end_row)
            dice_col = random.randrange(start_col, end_col)
            location = self.square[dice_row][dice_col]
            while location.kind == "mountain" or location.kind == "water" or location.has_object:
                dice_row = random.randrange(start_row, end_row)
                dice_col = random.randrange(start_col, end_col)
                location = self.square[dice_row][dice_col]
            dice = random.randrange(0, len(lst))
            location.has_object = True
            location.object_name = lst.pop(dice)
            if type(location.object_name) == Hero:
                location.has_hero = True
                location.hero = location.object_name

    def view_board(self, p, moving = False):
        rows = len(self.square)
        cols = len(self.square[0])
        if moving:
            print(f"{p.color}\033[5mCommands:\033[0m{p.color}        Move with \"QWE ASD ZX\"          Exit moving with \"o\"                "
                  f"                                                                                                   "
                  f"                                            \033[0m")
        else:
            print(f"{p.color}\033[5mCommands:\033[0m{p.color}        \"View\"          \"Move\"          \"Town\"          \"Spells\"        "
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
              f"                                                                   Day: {p.weekday} Week: {p.week}         \033[0m")

    def view_battlefield(self, p, attacker):
        rows = len(self.square)
        cols = len(self.square[0])
        print(f"{p.color}Commands:    Move with \"QWEASDZX\"    \033[5m \"r\"\033[0m{p.color} for ranged attack          \"Spells\" for spellbook           "
              f"\"o\" to stop moving (end turn)                        \033[0m ")
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
        print(f"{p.color}\033[5mCommands:\033[0m{p.color}         \"Build\"          \"Recruit\"          \"Mage Guild\"          \"Tavern\"  "
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
            f"{p.mercury} Gold:{p.gold} {c.dw_color} {list(c.unit_names)[0]}:{c.dw1amount} | "
            f"{list(c.unit_names)[1]}:{c.dw2amount} | {list(c.unit_names)[2]}:{c.dw3amount} | {list(c.unit_names)[3]}:"
            f"{c.dw4amount} | {list(c.unit_names)[4]}:{c.dw5amount}  |  {list(c.unit_names)[5]}:{c.dw6amount} |"
            f" {list(c.unit_names)[6]}:{c.dw7amount} \033[0m")

class Landscape:
    #os.system('color')
    HILLS = '\033[102m'
    WATER = '\033[104m'
    MOUNTAIN = '\033[100m'
    PLAINS = '\033[43m'
    FOREST = '\033[42m'
    RED = '\033[91m'
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
            if self.operated_by:
                return f'{self.operated_by.color}' +'{: ^6s}'.format(self.object_name[:6]) + f'{Landscape.END}'
            elif type(self.object_name) == Hero:
                return f'{self.color}{Landscape.RED}' + '{: ^6s}'.format(self.object_name.name[:6].upper()) + f'{Landscape.END}'
            else:
                return f'{self.color}{Landscape.DW}' +'{: ^6s}'.format(self.object_name[:6]) + f'{Landscape.END}'
        elif self.seen[input_player.number-1] == 1:
            return f'{self.color}      {Landscape.END}'
        else:
            return f'      '

    def print_hero(self, input_player):
        if type(self.object_name) == Hero and self.seen[input_player.number-1] == 1:
            amount = 0
            for unit in self.object_name.army:
                amount += unit.amount
            if amount > 10:
                return f'{self.color}{Landscape.RED}' + '{: ^6s}'.format("Lots") + f'{Landscape.END}'
            elif amount < 10:
                return f'{self.color}{Landscape.RED}' + '{: ^6s}'.format("Severa") + f'{Landscape.END}'
            elif amount < 4:
                return f'{self.color}{Landscape.RED}' + '{: ^6s}'.format("Few") + f'{Landscape.END}'
        elif self.has_hero and self.seen[input_player.number-1] == 1:
            return f'{self.color}{Landscape.RED}' + '{: ^6s}'.format(self.hero.name[:4] +","+ str(self.hero.level)) + \
                   f'{Landscape.END}'
        elif self.seen[input_player.number-1] == 1:
            return f'{self.color}      {Landscape.END}'
        else:
            return f'      '

    def print_war1row(self, current_player):
        self.color = Landscape.END
        if self.has_hero and self.hero.amount > 0 and self.hero.affected_color != "":
            if self.hero.affected_color == "green":
                return f'|{Landscape.FOREST}' + '{: ^11s}'.format(self.hero.spells_affected_by[0][:9].capitalize()) + \
                   f'{Landscape.END}'
            elif self.hero.affected_color == "red":
                return f'|\033[41m' + '{: ^11s}'.format(self.hero.spells_affected_by[0][:9].capitalize()) + \
                       f'{Landscape.END}'
        elif self.has_hero and self.hero.amount > 0:
            return f'|           '
        else:
            return f'|           '

    def print_war2row(self, current_player, attacker):
        self.color = Landscape.END
        if self.has_hero and self.hero.operating_hero.operating_player != current_player and self.hero.amount > 0:
            return f'|{Landscape.RED}' + '{: ^11s}'.format(
                self.hero.name[:7].upper() + ", " + str(self.hero.amount)) + f'{Landscape.END}'

        elif self.has_hero and self.hero.amount > 0:
            if attacker.location == self.hero.location and attacker.isranged:
                self.color = '\033[5;30;103m'
            elif attacker.location == self.hero.location:
                self.color = '\033[6;30;103m'
            return f'|{self.color}' + '{: ^11s}'.format(
                self.hero.name[:7].upper() + ", " + str(self.hero.amount)) + f'{Landscape.END}'
        else:
            return f'|           '

    def print_war3row(self, current_player):
        self.color = Landscape.END
        if self.has_hero and self.hero.operating_hero.operating_player != current_player and self.hero.amount > 0:
            return f'|{Landscape.RED}' + '{: ^11s}'.format(str(self.hero.health) + "hp|" + str(self.hero.speed_left)
                                                           + "sp") + f'{Landscape.END}'
        elif self.has_hero and self.hero.amount > 0:
            return f'|' + '{: ^11s}'.format(str(self.hero.health) + "hp"
                                                                    "|" + str(self.hero.speed_left) + "sp")
        else:
            return f'|           '