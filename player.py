from entities import Hero, Town, Gameboard, cur
from dataclasses import dataclass, fields
import os, time, random, itertools

# Code written by Alex Stråe from Sweden. Creatures, heroes and town attributes and
# names are, where copied correctly, copied from the original game 'Heroes of Might and Magic 3'.

class Dialogues:
    def line(width):
        return ("-" + '{:-^'  + str(width) + 's}').format("-") + "-\n"

    def box(text: str, width, box, lines)->str:
        result=""
        separator = "" if not lines else "-"
        if box:
            result = Dialogues.line(width)
        for row in text.split("\n"):
            result += ("|" + '{:'+separator+'^' + str(width) + 's}').format(row) + "|"
            if box:
                result += "\n"
        if box:
            result += Dialogues.line(width)
        return result

@dataclass
class Resources:
    wood:int = 0
    mercury:int = 0
    stone:int = 0
    sulfur: int = 0
    crystal:int = 0
    gems:int = 0
    gold:int = 0

    def __add__(self, other):
        return Resources(*(getattr(self, dim.name) + getattr(other, dim.name) for dim in fields(self)))

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
        self.hero_ticker = 1
        self.has_hired = False
        self.num_towns = 0
        self.resources = Resources(10, 4, 10, 4, 4, 4, 4000)
        self.daily = Resources(0, 0, 0, 0, 0, 0, 500)
        self.weekday = 1
        self.week = 1

    def __str__(self):
        return f'{self.name}'

    def clear_window(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def dialogue_display(self, input1="", input2="", input3="", input4="", width=140, box=True, lines=False):
        print(Dialogues.box(input1+input2+"\n"+input3+input4, width, box, lines))
        input("\n")

    def box_display(self, input, width=140, box=True, lines=False):
        print(Dialogues.box(input, width, box, lines))

    def dialogue_return(self, input1="", input2="", input3="", input4="", width=140, box=True, lines=False):
        print(Dialogues.box(input1+input2+"\n"+input3+input4, width, box, lines))
        choice = input("\n")
        return choice

    def view_info(self):
        print("")
        self.box_display("Player: " + self.name, 40, False, False)
        self.box_display("Towns", 40, False, True)
        for town in self.towns:
            self.box_display(town.name +", Kingdom: " + town.kingdom, 40, False, True)
            if town.army:
                for unit in town.army:
                    self.box_display(unit.name+ ", " + str(unit.amount) + " units",40, False, False)
            else:
                self.box_display("No army.", 40, False, False)
        self.box_display("Heroes", 40, False, True)
        for hero in self.heroes:
            self.box_display(hero.name + ", " + hero.kind + " level: " + str(hero.level), 40, False, True)
            self.box_display("Daily movement points: " + str(hero.new_speed),40, False, False)
            self.box_display("Attack: " + str(hero.attack) + "   Defense: " + str(hero.defense), 40, False, False)
            self.box_display("Knowledge: " + str(hero.knowledge) + " Spell Power: " + str(hero.spell_power), 40, False, False)
            self.box_display("Army:", 40, False, False)
            for unit in hero.army:
                self.box_display(unit.name + ", " + str(unit.amount) + " units", 40, False, False)
        self.box_display("", 40, False, True)
        input("\n")

    def new_turn(self):
        self.resources += self.daily
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
            if hero.spell_points < hero.knowledge*10:
                hero.spell_points += 5

    def choose_kingdom(self, available_kingdoms):
        chosen_kingdom = self.dialogue_return(str(available_kingdoms), "",
                            "These kingdoms are available. Choose your kingdom, ", self.name + "!").capitalize()
        while chosen_kingdom not in available_kingdoms:
            chosen_kingdom = input("Try again " + self.name + ".\n").capitalize()
        self.kingdom = chosen_kingdom
        available_kingdoms.remove(chosen_kingdom)

    def create_heroes(self, new_loc=None, map=None):
        new_hero = None
        for name, type, attack, defense, knowledge, spell_power in cur.execute("SELECT name, type, attack, " \
             "defense, knowledge, spell_power FROM heroes WHERE kingdom = '" + self.kingdom.lower() +
                "' AND id = " + str(self.hero_ticker)):
            new_hero = Hero(name, type, attack, defense, knowledge, spell_power, self)
        if new_loc != None:
            new_hero.location = new_loc
            map.square[new_loc[0]][new_loc[1]].has_hero = True
            map.square[new_loc[0]][new_loc[1]].hero = new_hero
        self.heroes.append(new_hero)
        self.hero_ticker += 1
        self.heroes_left += 1
        new_hero.location = new_loc
        new_hero.create_starting_army()

    def create_towns(self):
        new_town = None
        if self.kingdom == "Castle": new_town = Town("Valetta", self.kingdom, self)
        elif self.kingdom == "Dungeon": new_town = Town("Deepwarren", self.kingdom, self)
        elif self.kingdom == "Inferno": new_town = Town("Styx", self.kingdom, self)
        elif self.kingdom == "Necropolis": new_town = Town("Blighttown", self.kingdom, self)
        elif self.kingdom == "Rampart": new_town = Town("Goldenglade", self.kingdom, self)
        elif self.kingdom == "Tower": new_town = Town("Celeste", self.kingdom, self)
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
                    if pn == 0 and c < 0: c = 0
                    elif pn == 1 and c < 0: c = -1
                    elif pn == (rows - 1) and c > 0: c = 0
                    elif pn == (rows - 2) and c > 1: c = 1
                    if pl == 0 and d < 0: d = 0
                    elif pl == 1 and d < 0: d = -1
                    elif pl == (cols - 1) and d > 0: d = 0
                    elif pl == (cols - 2) and d > 1: d = 1
                    map.square[pn + c][pl + d].seen[self.number - 1] = 1

    def interpretor(self, choice, map, list_of_players):
        if choice.lower() == "view":
            self.view_info()

        elif choice.lower() == "move":
            if len(self.heroes) == 1:
                hero_choice = self.heroes[0].name
                self.move_obj(hero_choice, map)
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
                    self.dialogue_display("No hero with that name found.")
                    return
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
                self.dialogue_display(hero.name + " does not have a spellbook.")

        elif choice.lower() == "town":
            if self.towns != []:
                if len(self.towns) > 1:
                    town_choice = input("Enter which town? Number:\n")
                    while town_choice not in ("1", "2", "3"):
                        town_choice = input("Type town to enter. 1 = First town. 2 = Second town. 3 = Third town.\n")
                    if town_choice == "1":
                        self.enter_town(self.towns[0], map)
                    elif town_choice == "2":
                        self.enter_town(self.towns[1], map)
                    elif town_choice == "3":
                        self.enter_town(self.towns[2], map)
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
        self.clear_window()
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
        return ""

    def new_pos_calculator(self, choice, old_pos):
        new_pos = [0,0]
        if choice == 'q': new_pos[0], new_pos[1] = old_pos[0] - 1, old_pos[1] - 1
        elif choice == 'w': new_pos[0], new_pos[1] = old_pos[0] - 1, old_pos[1]
        elif choice == 'e': new_pos[0], new_pos[1] = old_pos[0] - 1, old_pos[1] + 1
        elif choice == 'a': new_pos[0], new_pos[1] = old_pos[0], old_pos[1] - 1
        elif choice == 's': new_pos[0], new_pos[1] = old_pos[0] + 1, old_pos[1]
        elif choice == 'd': new_pos[0], new_pos[1] = old_pos[0], old_pos[1] + 1
        elif choice == 'z': new_pos[0], new_pos[1] = old_pos[0] + 1, old_pos[1] - 1
        elif choice == 'x': new_pos[0], new_pos[1] = old_pos[0] + 1, old_pos[1] + 1
        return new_pos

    def by_speed(self, unit):
        return unit.speed_left

    def move_obj(self, input_hero, input_board):
        if self.has_hero_name(input_hero):
            hero = self.get_hero(input_hero)
            while True:
                self.clear_window()
                input_board.view_board(self, True)
                choice = ""
                while choice == "" or choice[0] not in ("q", "w", "e", "a", "s", "d", "z", "x", "o", "-"):
                    choice = input(hero.speed_bar()).lower()
                old_pos = hero.location
                new_pos = [0, 0]
                if choice[0] == '-':
                    hero.speed_left += 1000
                    hero.new_speed += 1000
                    break
                elif choice[0] == "o":
                    print("Exiting.")
                    time.sleep(0.5)
                    return
                new_pos = self.new_pos_calculator(choice[0], old_pos)
                if new_pos[0] < 0: new_pos[0] = 0
                elif new_pos[0] == len(input_board.square): new_pos[0] = len(input_board.square) - 1
                if new_pos[1] < 0: new_pos[1] = 0
                elif new_pos[1] == len(input_board.square[0]): new_pos[1] = len(input_board.square[0]) - 1
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
                        elif new_loc.has_object and new_loc.object_name == "Town" and \
                                new_loc.town.operating_player != self:
                            if new_loc.town.army != []:
                                self.start_war(hero, new_loc.town, new_loc, old_loc)
                                new_loc.town.alive = True
                            else:
                                self.towns.append(new_loc.town)
                                new_loc.operated_by = self
                                for town in new_loc.town.operating_player.towns:
                                    if town.name == new_loc.town.name:
                                        new_loc.town.operating_player.towns.remove(town)
                                self.towns[-1].operating_player = self
                                if self.towns[-1].buildings.hall_lvl == 4:
                                    self.towns[-1].buildings.hall_lvl = 3
                                self.dialogue_display("You have conquered a town!")

                        elif new_loc.has_hero == False:
                            old_loc.has_hero = False
                            old_loc.hero = None
                            new_loc.has_hero = True
                            new_loc.hero = hero
                            hero.location = new_pos
                            if new_loc.has_object and new_loc.object_name == "Town" and new_loc.town.operating_player == self:
                                self.enter_town(new_loc.town, input_board)
                                return
                            elif new_loc.has_object:
                                hero.confront_object(new_loc)
                        self.update_discovery(input_board)

                        if hero.speed_left == 0:
                            self.dialogue_display("You have run out of movement points. Exiting movement.")
                            return
                        elif hero.alive == False:
                            self.dialogue_display("Your forces suffer a bitter defeat, and " + hero.name + " leaves your cause.")
                            return
                    else:
                        self.dialogue_display("You have run out of movement points. Exiting movement.")
                        return

    def start_war(self, attacker, defender, battle_loc, old_loc):
        # Setting up battlefield:
        battlefield = Gameboard(10, 13, False)
        for u in attacker.army:
            u.location[0] = u.start_location[0] + 1
            u.location[1] = 0
            battlefield.square[u.location[0]][0].has_hero = True
            battlefield.square[u.location[0]][0].hero = u
            u.health = u.orig_health
        for u in defender.army:
            u.location[0] = u.start_location[0] + 1
            u.location[1] = 12
            battlefield.square[u.location[0]][12].has_hero = True
            battlefield.square[u.location[0]][12].hero = u
            u.health = u.orig_health
        # Battle starts:
        # First: Reset standard attributes and apply active spell effects if any:
        while attacker.alive and defender.alive:
            for u in attacker.army:
                u.battle_attributes_handler()
            attacker.army.sort(key=self.by_speed, reverse=True)
            for u in defender.army:
                u.battle_attributes_handler()
            defender.army.sort(key=self.by_speed, reverse=True)
            attacker.can_throw_spell = True
            defender.can_throw_spell = True
            # Each has their turn, then restart
            for (a_unit, d_unit) in itertools.zip_longest(attacker.army, defender.army):
                if a_unit and defender.alive:
                    if a_unit.amount > 0 and a_unit.turn_left is True:
                        self.war_move_obj(a_unit, defender, battlefield)
                    if a_unit.battle_actions:
                        a_unit.battle_attributes_handler(True)
                attacker.alive = attacker.check_alive()
                if d_unit and attacker.alive:
                    if d_unit.amount > 0 and d_unit.turn_left is True:
                        defender.operating_player.war_move_obj(d_unit, attacker, battlefield)
                    if d_unit.battle_actions:
                        d_unit.battle_attributes_handler(True)
                attacker.alive = attacker.check_alive()
                defender.alive = defender.check_alive()
        # Now at least one is dead. Let's wrap up and return
        if not attacker.alive:
            for unit in defender.army:
                if unit.amount < 1:
                    defender.army.remove(unit)
            old_loc.has_hero = False
            old_loc.hero = None
            self.heroes_left -= 1
            self.heroes.remove(attacker)

        if not defender.alive:
            for unit in attacker.army:
                if unit.amount < 1:
                    attacker.army.remove(unit)
            battle_loc.has_hero = False
            battle_loc.hero = None
            if type(battle_loc.object_name) == Hero:
                battle_loc.object_name = ""
            elif type(defender) == Hero:
                defender.operating_player.heroes_left -= 1
                defender.operating_player.heroes.remove(defender)
            elif type(defender) == Town and attacker.alive:
                self.towns.append(defender)
                self.towns[-1].operating_player = self
                if self.towns[-1].buildings.hall_lvl == 4:
                    self.towns[-1].buildings.hall_lvl = 3
                battle_loc.operated_by = self
                defender.operating_player.towns.remove(defender)
                self.dialogue_display("You have conquered a town!")

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

        # For AI control / Computer Player:
        if a.operating_hero.operating_player.number == 9:
            self.clear_window()
            battlefield.view_battlefield(self, a)
            # ACQUIRING TARGET:
            diff_damage_health = 100000
            for unit in defending_hero.army:
                if unit.amount > 0:
                    if abs((unit.health * unit.amount) - total_damage_attacker) < diff_damage_health:
                        if d:
                            if unit.isranged:
                                diff_damage_health = abs((unit.health * unit.amount) - total_damage_attacker)
                                d = unit
                        else:
                            diff_damage_health = abs((unit.health * unit.amount) - total_damage_attacker)
                            d = unit
            # Moving closer to target, if melee unit:
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
                    while prospect == None or (prospect.has_hero and prospect.hero != d and move_around < 2) or (
                            prospect.has_hero and move_around >= 2 and prospect.hero.operating_hero == a.operating_hero):
                        total_counter += 1
                        if total_counter > 30:
                            self.clear_window()
                            battlefield.view_battlefield(self, attacker)
                            print("AI failed to find matching movement prospect after too many tries.")
                            print(a.name + " targeted " + d.name)
                            if prospect == None:
                                print("Prospect was None!")
                            else:
                                print("Prospect was " + str(prospect.coord))
                            print("Returning in 10 seconds...")
                            time.sleep(10)
                            return
                        if prospect != None and prospect.has_hero and prospect.hero != d:
                            move_around += 1
                            if move_around == 3:
                                counter = 0
                            counter += 1
                            if counter == 1: ss = -1
                            elif counter == 2: ss = 1
                        if diff_col == 0:
                            if direction_row > 0: prospect = battlefield.square[a.location[0] - 1][a.location[1] + ss]
                            elif direction_row < 0: prospect = battlefield.square[a.location[0] + 1][a.location[1] + ss]
                        elif diff_row == 0:
                            if direction_col > 0: prospect = battlefield.square[a.location[0] + ss][a.location[1] - 1]
                            elif direction_col < 0: prospect = battlefield.square[a.location[0] + ss][a.location[1] + 1]
                        else:
                            if diff_col > diff_row:
                                if direction_col > 0: prospect = battlefield.square[a.location[0] + ss][a.location[1] - 1]
                                elif direction_col < 0: prospect = battlefield.square[a.location[0] + ss][a.location[1] + 1]
                            elif diff_row >= diff_col:
                                if diff_row == 1 and diff_col == 1: prospect = battlefield.square[d.location[0]][d.location[1]]
                                elif direction_row > 0: prospect = battlefield.square[a.location[0] - 1][a.location[1] + ss]
                                elif direction_row < 0: prospect = battlefield.square[a.location[0] + 1][a.location[1] + ss]

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
        # For human players:
        else:
            while True:
                self.clear_window()
                battlefield.view_battlefield(self, attacker)
                choice = input("Enter commands.\n").lower()
                while choice == "" or choice[0] not in ("q", "w", "e", "a", "s", "d", "z", "x", "o", "r"):
                    choice = input("     Move with QWEASDZX or use commands in the action bar.\n").lower()

                if choice == "r":
                    if attacker.isranged:
                        while True:
                            choice = input("Type unit to range attack:\n").title()
                            for unit in defending_hero.army:
                                if choice[:6] == unit.name[:6] and unit.amount > 0:
                                    d = unit
                                    break
                            if d:
                                break
                            else:
                                print("         Found no unit with that name.")
                                time.sleep(1)
                    else:
                        print("         This unit does not have a ranged attack!")
                        time.sleep(1)

                elif choice == "spells":
                    spell_damage = None
                    original_spell_damage = None
                    spell_effect = None
                    spell_cost = None
                    spell_color = None
                    if attacker.operating_hero.can_throw_spell:
                        while True:
                            if not attacker.operating_hero.spellbook:
                                self.dialogue_display(attacker.operating_hero.name + " does not have a spellbook!")
                                break
                            attacker.operating_hero.view_spells()
                            spell = ""
                            while spell == "":
                                spell = self.dialogue_return(
                                    "Name the spell you want to throw or ""C"" to cancel.").title()
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
                                    spell_effect = spell_in_book.get("effect")
                                    spell_cost = spell_in_book.get("cost")
                                    if "color" in spell_in_book:
                                        spell_color = spell_in_book.get("color")
                            if spell_cost == None:
                                self.dialogue_display("No such spell found.")
                            elif spell_cost > attacker.operating_hero.spell_points:
                                self.dialogue_display("You don't have the spell points.")
                            elif spell_color != "ADV":
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
                                    a.operating_hero.spell_points -= spell_cost
                                    a.operating_hero.can_throw_spell = False
                                    if spell_damage:
                                        original_spell_damage = spell_damage * a.operating_hero.spell_power
                                        original_health_defender = d.health
                                        new_loc = battlefield.square[d.location[0]][d.location[1]]
                                        d.health -= spell_damage * a.operating_hero.spell_power
                                        d.health = int(d.health)
                                        spell_damage -= original_health_defender
                                        while d.health <= 0:
                                            d.amount -= 1
                                            d.health = d.orig_health
                                            if spell_damage > 0:
                                                d.health -= spell_damage
                                                spell_damage -= d.orig_health
                                        if d.amount < 1:
                                            new_loc.has_hero = False
                                            new_loc.hero = None
                                        self.dialogue_display(a.operating_hero.name + " throws  " + spell + " at " +
                                                              d.name, "", "for " + str(original_spell_damage) + " damage!")
                                        d = None
                                        break
                                    else:
                                        if spell_effect in d.battle_actions:
                                            for spell in d.battle_actions:
                                                if spell[0] is spell_effect:
                                                    spell[1] = a.operating_hero.spell_power
                                        else:
                                            attacker.operating_hero.effect_thrower(spell_effect, d)
                                            if spell_color:
                                                d.affected_color = spell_color
                                            d.spells_affected_by.append(spell.title())
                                            d.battle_actions.append([spell_effect, a.operating_hero.spell_power, spell])
                                            self.dialogue_display(a.operating_hero.name + " throws  " + spell + " at " +
                                                                  d.name + "!")
                                        d = None
                                        break
                    else:
                        print("         You have already thrown a spell this cycle.")
                        time.sleep(2)
                # With ranged units and spells out of the way, time for movement:
                else:
                    for i in range(len(choice)):
                        old_pos = a.location
                        new_pos = [0, 0]
                        if choice[i] in ("q", "w", "e", "a", "s", "d", "z", "x"):
                            new_pos = self.new_pos_calculator(choice[i], old_pos)
                        elif choice[i] == "o": return
                        else:
                            print("     Invalid input.")
                            time.sleep(1)
                            break
                        if new_pos[0] < 0: new_pos[0] = 0
                        elif new_pos[0] == len(battlefield.square): new_pos[0] = len(battlefield.square) - 1
                        if new_pos[1] < 0: new_pos[1] = 0
                        elif new_pos[1] == len(battlefield.square[0]): new_pos[1] = len(battlefield.square[0]) - 1
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
                                time.sleep(1)
                            elif new_loc.has_hero and new_loc.hero.operating_hero != a.operating_hero:
                                d = new_loc.hero
                                break
                    if d:
                        break
                if d:
                    break
        # Executing damage from all units, human or AI:
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
            d.health = d.orig_health
            if total_damage_attacker > 0:
                d.health -= total_damage_attacker
                total_damage_attacker -= d.orig_health
        if d.amount < 1:
            defender_loc.has_hero = False
            defender_loc.hero = None
        # If target is still alive they may retaliate:
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
                a.health = a.orig_health
                if total_damage_defender > 0:
                    a.health -= total_damage_defender
                    total_damage_defender -= a.orig_health
            if a.amount < 1:
                attacker_loc.has_hero = False
                attacker_loc.hero = None
            d.has_retaliated = True
        self.clear_window()
        battlefield.view_battlefield(self, a)
        # Display results:
        if a.isranged:
            self.dialogue_display(a.name + " shoots " + d.name, " with " + str(original_damage_attacker) + " damage!")

        elif d.has_retaliated == True and original_damage_defender is not None:
            self.dialogue_display(a.name + " attacks " + d.name, " with " + str(original_damage_attacker) +
                                  " damage!", d.name + " retaliates with ", str(original_damage_defender) + " damage!")
        else:
            self.dialogue_display(a.name + " attacks " + d.name, " with " + str(original_damage_attacker) + "!")

    def enter_town(self, town, map):
        if town.render == None:
            town.render = Gameboard(10, 12, False)
        while True:
            self.clear_window()
            town.renderer()
            town.render.view_town(town, self)
            visiting_hero = map.square[town.location[0]][town.location[1]].hero
            if visiting_hero and visiting_hero.spellbook != [] and town.buildings.mageGuildLvl > 0:
                    for spell in town.spellbook:
                        if spell not in visiting_hero.spellbook:
                            visiting_hero.spellbook.append(spell)
            choice = self.dialogue_return("What do you want to do?").lower()
            while choice not in ("build", "recruit", "mage guild", "tavern", "view", "exit"):
                choice = self.dialogue_return("See the upper action bar for available commands.").lower()

            if choice == "mage guild":
                if town.buildings.mageGuildLvl > 0:
                    if visiting_hero and visiting_hero.spellbook == []:
                        choice9 = "not yet"
                        while choice9 != "":
                            choice9 = self.dialogue_return(visiting_hero.name +
                                " does not own a spellbook. ", "Do you wish to purchase one for 500 gold?",
                                                           "Enter to purchase, ""C"" to cancel")
                            if choice9 == "" and self.resources.gold > 499:
                                self.resources.gold -= 500
                                self.dialogue_display("You purchased a spellbook!")
                                visiting_hero.can_throw_spell = True
                                for spell in town.spellbook:
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
                    self.townbuilder(town)

            elif choice == "tavern":
                if map.square[town.location[0]][town.location[1]].has_hero:
                    self.dialogue_display("You cannot hire a new hero while your town is occupied by another hero.")
                elif self.has_hired:
                    self.dialogue_display("You have already hired a hero this week.")
                else:
                    choice = self.dialogue_return("Hiring a new hero costs 2500 gold.", "",
                                                  "Press Enter to hire. Press C to cancel.").lower()
                    if self.hero_ticker == 3:
                        self.dialogue_display("Unfortunately there are only three heroes per player.")
                    elif choice != "c" and self.resources.gold >= 2500:
                        self.create_heroes(town.location, map)
                        self.resources.gold -= 2500
                        self.has_hired = True
                        self.dialogue_display("Hero hired! Press Enter to return to map.")
                        return
                    elif choice != "c" and self.resources.gold < 2500:
                        self.dialogue_display("You lack the necessary funds.")

            elif choice == "recruit":
                if visiting_hero == None:
                    choice = "not yet"
                    while choice not in ("", "c"):
                        choice = self.dialogue_return(
                            "You have no hero in town. Purchase army for fortification defense?", "",
                            "\"Enter\" to purchase units. \"C\" to cancel.").lower()
                    if choice == "":
                        visiting_hero = town
                    else:
                        break
                while True:
                    see_price = ""
                    while see_price not in town.unit_names and see_price != "C":
                        see_price = self.dialogue_return("Type a unit to see its price.", "", "Type \"C\" to cancel.").title()
                    if see_price == "C":
                        break
                    else:
                        for i in range(7):
                            if see_price == list(town.unit_names)[i]:
                                available_stack = town.available_units[i]
                                amount = ""
                                while amount == "":
                                    amount = self.dialogue_return(see_price + ".", " Price: " + \
                                        str(town.unit_names.get(see_price)) + " gold.", str(available_stack) \
                                        + " available.", " Type the amount to recruit or C to cancel.")
                                if amount == "C" or amount == "c":
                                    break
                                else:
                                    try:
                                        amount = int(amount)
                                    except ValueError:
                                        print("Numbers only, or C to exit.")
                                        break
                                found = False
                                if amount * town.unit_names.get(
                                        see_price) <= self.resources.gold and amount <= available_stack:
                                    if len(visiting_hero.army) == 7:
                                        for unit in visiting_hero.army:
                                            if unit.name == see_price:
                                                found = True
                                                self.dialogue_display("Your army has run out of space.", "",
                                                                    "The unit will recruit to first existing stack.")
                                                break
                                        if not found:
                                            self.dialogue_display("Your army is full! Press Enter to exit.")
                                            break
                                    if found:
                                        visiting_hero.create_unit(town.kingdom, see_price, amount, True)
                                    else:
                                        visiting_hero.create_unit(town.kingdom, see_price, amount)
                                    town.available_units[i] -= amount
                                    self.resources.gold -= amount * town.unit_names.get(see_price)
                                    self.dialogue_return(str(amount) + " " + see_price + " recruited!")
                                else:
                                    self.dialogue_display("You either do not have the gold", "",
                                                          "or lack available units.")
                                break
            elif choice == "view":
                self.view_info()
            elif choice == "exit":
                break

    def townbuilder(self, town):
        see_price = ""
        prices = None
        req = None
        prices_string = ""
        type = None
        while see_price not in town.buildings_available:
            see_price = self.dialogue_return(str(town.buildings_available), "",
                                             "Type a building to see its price.").title()
        for entry in town.buildings_prices:
            if see_price == entry.get("name"):
                prices = entry.get("price")
                req = entry.get("req")
                type = entry.get("type")
                break
        for resource, price in prices.items():
            if price > 0:
                prices_string = prices_string + str(price) + " "
                prices_string = prices_string + resource + ", "
        choice = self.dialogue_return(see_price, " Requirements: " + req + ". Price: "
                                      + prices_string[:-2], "Press Enter to construct this building. ",
                                      "Type ""C"" to cancel.").lower()
        if choice == "c":
            return
        list_req = req.split(", ")
        funds = True
        for resource in prices.keys():
            if resource in vars(self.resources):
                if vars(self.resources).get(resource) < int(prices.get(resource)):
                    funds = False
                    self.dialogue_display("You lack the necessary funds.")
                    return
        req_fulfilled = True
        for requirement in list_req:
            if "=" in requirement:
                building_and_level = requirement.split("=")
                if building_and_level[0] in vars(town.buildings):
                    if vars(town.buildings).get(building_and_level[0]) < int(building_and_level[1]):
                        req_fulfilled = False
                        self.dialogue_display("You lack the necessary requirements.")
                        return
            elif requirement in vars(town.buildings):
                if vars(town.buildings).get(requirement) == False:
                    req_fulfilled = False
                    self.dialogue_display("You lack the necessary requirements.")
                    return
        if funds and req_fulfilled:
            if see_price == "Capitol":
                town.buildings.hall_lvl = 4
                self.daily.gold += 2000
                town.buildings_available[0] = ""
            elif see_price == "City Hall":
                town.buildings.hall_lvl = 3
                self.daily.gold += 1000
                town.buildings_available[0] = "Capitol"
            elif see_price == "Town Hall":
                town.buildings.hall_lvl = 2
                self.daily.gold += 500
                town.buildings_available[0] = "City Hall"
            elif see_price == "Citadel":
                town.buildings.fort_lvl = 2
                town.buildings_available[1] = "Castle"
            elif see_price == "Castle":
                town.buildings.fort_lvl = 3
                town.buildings_available[1] = ""
            elif see_price[:10] == "Mage Guild":
                town.buildings.mageGuildLvl = int(see_price[11])
                for spell_ids in cur.execute("SELECT spell_ids FROM kingdom_spells WHERE level = " \
                    + str(town.buildings.mageGuildLvl) + " AND kingdom = '" + town.kingdom.lower() + "'"):
                    ids = spell_ids[0].split(",")
                    for id in ids:
                        for level, element, name, cost, damage, effect, color in cur.execute(
                            "SELECT level, element, name, cost, damage, effect, color FROM spells WHERE id = " + id):
                            town.spellbook.append({"level": level, "element": element, "name": name,
                                "cost": cost, "damage": damage, "effect": effect, "color": color})
                if town.buildings.mageGuildLvl < 5:
                    if town.buildings.mageGuildLvl == 4 and town.kingdom == "Castle":
                        town.buildings_available[2] = ""
                    else:
                        town.buildings_available[2] = see_price[:11].title() + str(town.buildings.mageGuildLvl + 1)
                else:
                    town.buildings_available[2] = ""
            elif type[:2] == "dw":
                for building in vars(town.buildings):
                    if building == type:
                        exec('town.buildings.' + building + ' = True')
                        id = int(type[2])
                        town.buildings_available.remove(town.dw_names[id - 1])
                        if type == "dw3": town.available_units[2] = 6
                        elif type == "dw4": town.available_units[3] = 4
                        elif type == "dw5": town.available_units[4] = 3
                        elif type == "dw6": town.available_units[5] = 2
                        elif type == "dw7": town.available_units[6] = 1
                        break
            for resource in prices.keys():
                if resource in vars(self.resources):
                    vars(self.resources)[resource] -= int(prices.get(resource))
            town.has_built = True
