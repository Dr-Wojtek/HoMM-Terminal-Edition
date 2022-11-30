import sys, random, time, operator
import sqlite3
from dataclasses import dataclass

# Code written by Alex Stråe from Sweden. Creatures, heroes and town attributes and
# names are, where copied correctly, copied from the original game 'Heroes of Might and Magic 3'.
con = sqlite3.connect("db/heroes3.db")
cur = con.cursor()

class Unit:
    def __init__(self, input_name, input_rank, input_amount, input_attack, input_defense, input_damage, input_health,
                 input_speed, input_cost, input_hero, input_ranger=False):
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
        self.location = [0, 0]
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

    def battle_attributes_handler(self, end_turn=False):
        if not end_turn:
            self.turn_left = True
            self.has_retaliated = False
            self.speed_left = self.new_speed
            self.attack = self.orig_attack
            self.defense = self.orig_defense
            self.damage = self.orig_damage
            if self.battle_actions:
                for action in self.battle_actions:
                    self.operating_hero.effect_thrower(action[0], self)
                    action[1] -= 1
        else:
            for action in self.battle_actions:
                if action[1] <= 0:
                    self.spells_affected_by.remove(action[2].title())
                    self.battle_actions.remove(action)
                    self.affected_color = ""

class Hero:
    def __init__(self, input_name, input_kind, input_attack, input_defense, input_knowledge, input_spellpower,
                 input_player):
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
        self.speed_left = 14
        self.new_speed = 14
        self.spellbook = []
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
        speedbar += "\033[0m Movement points cost depends on territory. Forest (\033[42m \033[0m): 2. Hills and plains " \
                    "(\033[102m \033[43m \033[0m): 1. Mountain (\033[100m \033[0m): 8. Water cannot be passed without the Summon Boat spell.\n"
        return speedbar

    def view_spells(self):
        print("")
        print("" + '{:^60s}'.format("Spells of: " + self.name + " with " + str(self.spell_points) + " spell points."))
        print("|" + '{:-^60s}'.format("") + "|")
        for spell in self.spellbook:
            print("|" + '{:-^60s}'.format(
                "  " + spell.get("name") + ", Cost: " + str(spell.get("cost")) + " spell points.") + "|")
            if spell.get("effect") != None:
                print("|" + '{:^60s}'.format(" Description: " + spell.get("effect")) + "|")
            elif spell.get("damage") != None:
                print("|" + '{:^60s}'.format(" Description: " + str(spell.get("damage"))) + "|")
            print("|" + '{:-^60s}'.format("") + "|")

    def create_monster_army(self, amount, stacks):
        for i in range(stacks):
            self.create_unit("monster", self.name, amount)
        self.name = self.army[0].name

    def create_starting_army(self):
        for i in range(3):
            for name, rank, attack, defense, damage, health, speed, cost, ranged in cur.execute(
                    "SELECT name, rank, attack, defense, damage, health, speed, cost, ranger FROM units " \
                    "WHERE kingdom = '" + self.operating_player.kingdom.lower() + "' AND rank = " + str(i+1) + ";"):
                new_unit = Unit(name, rank, int(13/(i+1))-1, attack, defense, damage, health, speed, cost, self, ranged)
                self.army.append(new_unit)

    def create_unit(self, kingdom, unit, amount, add_to_same_stack=False):
        for name, rank, attack, defense, damage, health, speed, cost, ranged in cur.execute(
                "SELECT name, rank, attack, defense, damage, health, speed, cost, ranger FROM units " \
            "WHERE kingdom = '" + kingdom.lower() + "' AND name = '" + unit + "'"):
            new_unit = Unit(name, rank, amount, attack, defense, damage, health, speed, cost, self, ranged)
            if add_to_same_stack:
                for u in self.army:
                    if u.name == new_unit.name:
                        u.amount += new_unit.amount
                        break
            else:
                self.army.append(new_unit)
                placement = len(self.army)
                self.army[-1].start_location[0] = placement

    def check_alive(self):
        for unit in self.army:
            if unit.amount > 0:
                return True
        return False

    def effect_thrower(self, spell, target):
        effects = spell.split(",")
        for effect in effects:
            if "+" in effect or "-" in effect or "." in effect:
                op = None
                factor = 0
                if effect[1] == "+":  op = operator.mul
                elif effect[1] == "-": op = operator.floordiv
                if effect[2] in ['1', '2', '3', '4', '5', '6', '7', '8', '9']: factor = 1.0+(int(effect[2:])/100)
                if effect[0] == 'A': target.attack = int(op(target.attack, factor))
                elif effect[0] == 'D': target.defense = int(op(target.defense, factor))
                elif effect[0] == 'X': target.damage = int(op(target.damage, factor))
                elif effect[0] == 'S': target.speed_left = int(op(target.speed_left, factor))
                elif effect[0] == 'H':
                    if effect[1] is ".": target.health = target.orig_health
                    else:
                        target.health = int(op(target.health, factor))
                        if target.health > target.orig_health:
                            target.health = target.orig_health
                elif effect[0] == 'R':
                    if target.isranged:
                        target.damage = int(op(target.damage,factor))
            elif effect == "LUCK":
                dice = random.randrange(1, 4)
                if dice > 1:
                    print(target.name + " is lucky this turn!")
                    time.sleep(1)
                    target.attack += 5
                    target.defense += 5
                    target.damage += 2
                    target.speed_left += 1
            elif effect == "BLIND":
                target.turn_left = False
                print(target.name + " is blind!")
                time.sleep(1)

    def confront_object(self, location):
        player = self.operating_player
        other_player = None
        if location.operated_by != None and location.operated_by != player:
            other_player = location.operated_by
        if location.object_name in ("wood", "stone", "crystal", "gems", "gold", "sulfur", "mercury") and \
                location.operated_by != player:
            amount = 0
            if location.object_name is "gold": amount = 1000
            elif location.object_name in ("wood", "stone"): amount = 2
            else: amount = 1
            player.dialogue_display("You gain operation of a ", "", location.object_name, " mine!")
            location.operated_by = player
            if other_player:
                current = getattr(other_player.daily, location.object_name)
                setattr(other_player.daily, location.object_name, current - amount)
            current = getattr(player.daily, location.object_name)
            setattr(player.daily, location.object_name, current + amount)
        match location.object_name:
            case "XP_stone":
                if self.name not in location.met_heroes:
                    self.level += 1
                    location.met_heroes.append(self.name)
                    choice = ""
                    while choice not in ("Attack", "Defense", "Knowledge", "Spell Power"):
                        choice = player.dialogue_return("You have gained a level!", " Type the skill you want to increase.",
                                "", "Attack / Defense / Knowledge / Spell Power").title()
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
                player.dialogue_display(self.name + " finds an old sword. It's blade is still sharp.", "",
                                        "Attack increased by 2!")
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
                                                    "or distribute it for experience (1 level?)",
                                                    "     XP / Gold").lower()
                    if choice == "xp":
                        self.level += 1
                        choice2 = ""
                        while choice2 not in ("Attack", "Defense", "Knowledge", "Spell Power"):
                            choice2 = player.dialogue_return("You have gained a level!",
                                                             " Type the skill you want to increase.",
                                                             "", "Attack / Defense / Knowledge / Spell Power").title()
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
                        player.resources.gold += 2000
            case "Shrine1":
                if not self.spellbook:
                    player.dialogue_display("This shrine has magic instructions for the spell ""Summon boat"", "
                                            "but " + self.name + " lacks a spellbook.")
                else:
                    player.dialogue_display("This shrine has magic instructions for the spell ""Summon boat"", "
                                            "and " + self.name + " scribbles it down.")
                    self.spellbook.append({"name": "Summon Boat", "cost": 7, "damage": 0, "effect": "Navigate water."})
            case "Shrine2":
                if not self.spellbook:
                    player.dialogue_display("This shrine has magic instructions for the spell ""Implosion"", "
                                            "but " + self.name + " lacks a spellbook.")
                else:
                    player.dialogue_display("This shrine has magic instructions for the spell ""Implosion"", "
                                            "and " + self.name + " scribbles it down.")
                    self.spellbook.append({"name": "Implosion", "cost": 40, "damage": 60, "effect": ""})

@dataclass
class Buildings:
    dw1: bool = False
    dw2: bool = False
    dw3: bool = False
    dw4: bool = False
    dw5: bool = False
    dw6: bool = False
    dw7: bool = False
    mageGuildLvl: int = 0
    fort_lvl : int = 1
    hall_lvl: int = 1

class Town:
    def __init__(self, input_name, input_kingdom, input_operating_player):
        self.name = input_name
        self.location = [0, 0]
        self.kingdom = input_kingdom
        self.operating_player = input_operating_player
        self.army = []
        self.alive = True
        self.buildings = Buildings(True, True)
        self.available_units = [12,8,0,0,0,0,0]
        self.render = None
        self.buildings_available = ["Town Hall", "Citadel", "Mage Guild 1"]
        self.has_built = False
        self.dw_names = []
        self.unit_names = {}
        self.dw_color = ""
        self.spellbook = []
        self.buildings_prices = []
        for name, req, gold, wood, mercury, stone, sulfur, crystal, gems in cur.execute("SELECT name, req, gold, wood," \
                 " mercury, stone, sulfur, crystal, gems FROM buildings WHERE kingdom = 'all'"):
            self.buildings_prices.append({"name":name, "req": req, "price" : {"gold": gold, "wood":wood,
                "mercury":mercury, "stone":stone, "sulfur":sulfur, "crystal": crystal, "gems":gems}})

        for name, req, type, gold, wood, mercury, stone, sulfur, crystal, gems in cur.execute("SELECT name, req, id, " \
                "gold, wood, mercury, stone, sulfur, crystal, gems FROM buildings WHERE kingdom = '" + self.kingdom.lower() +"'"):
            self.buildings_prices.append({"name":name, "req": req, "type": type, "price" : {"gold": gold, "wood":wood,
                "mercury":mercury, "stone":stone, "sulfur":sulfur, "crystal": crystal, "gems":gems}})
            self.dw_names.append(name)

        for name, price in cur.execute("SELECT name, cost FROM units WHERE kingdom = '" + self.kingdom.lower() + "'"):
            self.unit_names[name] = int(price)
        self.buildings_available.extend(self.dw_names[2:7])

        if self.kingdom == "Castle": self.dw_color = '\033[6;37;43m'
        elif self.kingdom == "Inferno": self.dw_color = '\033[6;33;41m'
        elif self.kingdom == "Rampart": self.dw_color = '\033[6;37;42m'
        elif self.kingdom == "Tower": self.dw_color = '\033[6;34;47m'
        elif self.kingdom == "Necropolis": self.dw_color = '\033[6;35;40m'
        elif self.kingdom == "Dungeon": self.dw_color = '\033[6;33;40m'

    def view_spells(self):
        print("")
        print("" + '{:^60s}'.format("Spells of: " + self.name))
        print("|" + '{:-^60s}'.format("") + "|")
        for spell in self.spellbook:
            print("|" + '{:-^60s}'.format("  " + spell.get("name") + ", Cost: " + str(spell.get("cost")) + " spell points.") + "|")
            if spell.get("effect") != None:
                print("|" + '{:^60s}'.format(" Description: " + spell.get("effect")) + "|")
            elif spell.get("damage") != None:
                print("|" + '{:^60s}'.format(" Description: " + str(spell.get("damage"))) + "|")
            print("|" + '{:-^60s}'.format("") + "|")
        input("\n")

    def new_week(self):
        if self.buildings.dw1:
            self.available_units[0] += 14 * self.buildings.fort_lvl
        if self.buildings.dw2:
            self.available_units[1] += 9 * self.buildings.fort_lvl
        if self.buildings.dw3:
            self.available_units[2] += 7 * self.buildings.fort_lvl
        if self.buildings.dw4:
            self.available_units[3] += 4 * self.buildings.fort_lvl
        if self.buildings.dw5:
            self.available_units[4] += 3 * self.buildings.fort_lvl
        if self.buildings.dw6:
            self.available_units[5] += 2 * self.buildings.fort_lvl
        if self.buildings.dw7:
            self.available_units[6] += 1 * self.buildings.fort_lvl

    def create_unit(self, kingdom, unit, amount, add_to_same_stack=False):
        for name, rank, attack, defense, damage, health, speed, cost, ranged in cur.execute("SELECT name, rank, " \
                    "attack, defense, damage, health, speed, cost, ranger FROM units " \
                    "WHERE kingdom = '" +kingdom.lower()+"' AND name = '"+unit+"'"):
            new_unit = Unit(name, rank, amount, attack, defense, damage, health, speed, cost, self, ranged)
            if add_to_same_stack:
                for u in self.army:
                    if u.name == new_unit.name:
                        u.amount += new_unit.amount
                        break
            else:
                self.army.append(new_unit)
                placement = len(self.army)
                self.army[-1].start_location[0] = placement

    def renderer(self):
        for i in range(8, 10):
            for j in range(5, 7):
                self.render.square[i][j].kind = "tavern"
                if i == 8: self.render.square[i][j].placement[0] = 3
                else: self.render.square[i][j].placement[0] = 1
                if j == 5: self.render.square[i][j].placement[1] = 4
                else: self.render.square[i][j].placement[1] = 3

        if self.buildings.dw1:
            for i in range(3, 5):
                for j in range(0, 1):
                    self.render.square[i][j].kind = self.dw_names[0]
            self.render.square[3][0].placement = [3, 4]
            self.render.square[4][0].placement = [1, 4]
        if self.buildings.dw2:
            for i in range(2, 5):
                for j in range(2, 3):
                    self.render.square[i][j].kind = self.dw_names[1]
            self.render.square[2][2].placement = [3, 4]
            self.render.square[3][2].placement = [2, 4]
            self.render.square[4][2].placement = [1, 4]
        if self.buildings.dw3:
            for i in range(0, 2):
                for j in range(0, 2):
                    self.render.square[i][j].kind = self.dw_names[2]
                    if i == 0: self.render.square[i][j].placement[0] = 3
                    else: self.render.square[i][j].placement[0] = 1
                    if j == 0: self.render.square[i][j].placement[1] = 1
                    else: self.render.square[i][j].placement[1] = 4
        if self.buildings.dw4:
            for i in range(3, 5):
                for j in range(3, 4):
                    self.render.square[i][j].kind = self.dw_names[3]
            self.render.square[3][3].placement = [3, 4]
            self.render.square[4][3].placement = [1, 4]
        if self.buildings.dw5:
            for i in range(8, 10):
                for j in range(1, 3):
                    self.render.square[i][j].kind = self.dw_names[4]
                    if i == 8: self.render.square[i][j].placement[0] = 3
                    else: self.render.square[i][j].placement[0] = 1
                    if j == 1: self.render.square[i][j].placement[1] = 2
                    else: self.render.square[i][j].placement[1] = 5
        if self.buildings.dw6:
            for i in range(6, 7):
                for j in range(2, 6):
                    self.render.square[i][j].kind = self.dw_names[5]
            self.render.square[6][2].placement = [4, 1]
            self.render.square[6][3].placement = [4, 2]
            self.render.square[6][4].placement = [4, 5]
            self.render.square[6][5].placement = [4, 3]
        if self.buildings.dw7:
            for i in range(0, 1):
                for j in range(4, 8):
                    self.render.square[i][j].kind = self.dw_names[6]
            self.render.square[0][4].placement = [4, 1]
            self.render.square[0][5].placement = [4, 4]
            self.render.square[0][6].placement = [4, 2]
            self.render.square[0][7].placement = [4, 3]

        if self.buildings.hall_lvl == 1:
            for i in range(9, 10):
                for j in range(8, 12):
                    self.render.square[i][j].kind = "VillageHll"
                    if i == 9: self.render.square[i][j].placement[0] = 4
                    if j == 8: self.render.square[i][j].placement[1] = 1
                    elif j == 9: self.render.square[i][j].placement[1] = 2
                    elif j == 10: self.render.square[i][j].placement[1] = 4
                    else: self.render.square[i][j].placement[1] = 3
        elif self.buildings.hall_lvl == 2:
            for i in range(8, 10):
                for j in range(8, 12):
                    self.render.square[i][j].kind = "Town Hall"
                    if i == 8: self.render.square[i][j].placement[0] = 3
                    else: self.render.square[i][j].placement[0] = 1
                    if j == 8: self.render.square[i][j].placement[1] = 1
                    elif j == 9: self.render.square[i][j].placement[1] = 2
                    elif j == 10: self.render.square[i][j].placement[1] = 4
                    else: self.render.square[i][j].placement[1] = 3
        elif self.buildings.hall_lvl == 3:
            for i in range(7, 10):
                for j in range(8, 12):
                    self.render.square[i][j].kind = "City Hall"
                    if i == 7: self.render.square[i][j].placement[0] = 3
                    elif i == 8: self.render.square[i][j].placement[0] = 2
                    else: self.render.square[i][j].placement[0] = 1
                    if j == 8: self.render.square[i][j].placement[1] = 1
                    elif j == 9: self.render.square[i][j].placement[1] = 2
                    elif j == 10: self.render.square[i][j].placement[1] = 4
                    else: self.render.square[i][j].placement[1] = 3
        elif self.buildings.hall_lvl == 4:
            for i in range(6, 10):
                for j in range(8, 12):
                    self.render.square[i][j].kind = "Capitol"
                    if i == 6: self.render.square[i][j].placement[0] = 3
                    elif i == 9: self.render.square[i][j].placement[0] = 1
                    else: self.render.square[i][j].placement[0] = 2
                    if j == 8: self.render.square[i][j].placement[1] = 1
                    elif j == 9: self.render.square[i][j].placement[1] = 2
                    elif j == 10: self.render.square[i][j].placement[1] = 4
                    else: self.render.square[i][j].placement[1] = 3

        if self.buildings.mageGuildLvl == 1:
            for i in range(4, 5):
                for j in range(11, 12):
                    self.render.square[i][j].kind = "MageGuild1"
            self.render.square[4][11].placement = [4, 4]
        elif self.buildings.mageGuildLvl == 2:
            for i in range(3, 5):
                for j in range(11, 12):
                    self.render.square[i][j].kind = "MageGuild2"
            self.render.square[3][11].placement = [3, 4]
            self.render.square[4][11].placement = [1, 4]
        elif self.buildings.mageGuildLvl == 3:
            for i in range(2, 5):
                for j in range(11, 12):
                    self.render.square[i][j].kind = "MageGuild3"
            self.render.square[2][11].placement = [3, 4]
            self.render.square[3][11].placement = [2, 4]
            self.render.square[4][11].placement = [1, 4]
        elif self.buildings.mageGuildLvl == 4:
            for i in range(1, 5):
                for j in range(11, 12):
                    self.render.square[i][j].kind = "MageGuild4"
            self.render.square[1][11].placement = [3, 4]
            self.render.square[2][11].placement = [2, 4]
            self.render.square[3][11].placement = [2, 4]
            self.render.square[4][11].placement = [1, 4]
        elif self.buildings.mageGuildLvl == 5:
            for i in range(0, 5):
                for j in range(11, 12):
                    self.render.square[i][j].kind = "MageGuild5"
            self.render.square[0][11].placement = [3, 4]
            self.render.square[1][11].placement = [2, 4]
            self.render.square[2][11].placement = [2, 4]
            self.render.square[3][11].placement = [2, 4]
            self.render.square[4][11].placement = [1, 4]

        if self.buildings.fort_lvl == 1:
            for i in range(4, 5):
                for j in range(5, 10):
                    self.render.square[i][j].kind = "Fort"
                    if i == 4: self.render.square[i][j].placement[0] = 4
                    if j == 5: self.render.square[i][j].placement[1] = 1
                    elif j == 7: self.render.square[i][j].placement[1] = 4
                    elif j == 9: self.render.square[i][j].placement[1] = 3
                    else: self.render.square[i][j].placement[1] = 2
        elif self.buildings.fort_lvl == 2:
            for i in range(3, 5):
                for j in range(5, 10):
                    self.render.square[i][j].kind = "Citadel"
                    if i == 3: self.render.square[i][j].placement[0] = 3
                    elif i == 4: self.render.square[i][j].placement[0] = 1
                    if j == 5: self.render.square[i][j].placement[1] = 1
                    elif j == 7: self.render.square[i][j].placement[1] = 4
                    elif j == 9: self.render.square[i][j].placement[1] = 3
                    else: self.render.square[i][j].placement[1] = 2
        elif self.buildings.fort_lvl == 3:
            for i in range(2, 5):
                for j in range(5, 10):
                    self.render.square[i][j].kind = "Castle"
                    if i == 2: self.render.square[i][j].placement[0] = 3
                    elif i == 4: self.render.square[i][j].placement[0] = 1
                    else: self.render.square[i][j].placement[0] = 2
                    if j == 5: self.render.square[i][j].placement[1] = 1
                    elif j == 7: self.render.square[i][j].placement[1] = 4
                    elif j == 9: self.render.square[i][j].placement[1] = 3
                    else: self.render.square[i][j].placement[1] = 2

class Gameboard:
    COORDINATES = '\030[47m'
    END = '\033[0m'

    def __init__(self, input_rows, input_cols, map=True):
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
                            if self.square[(i - 1)][j].kind == "mountain" or self.square[(i - 1)][(j - 1)].kind == "mountain":
                                dice = random.randrange(1, 3)
                                if dice != 1:
                                    dice = random.randrange(2, 9)
                            elif self.square[(i - 1)][j].kind == "water" or self.square[(i - 1)][
                                (j - 1)].kind == "water":
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
                landscape = Landscape(kind, [i, j], speed_drain)
                col.append(landscape)
            self.square.append(col)

    def beautifier(self, rows, cols):
        for i in range(rows):
            for j in range(cols):
                if (i > 0 and j > 0) and (i < rows - 1 and j < cols - 1):
                    if self.square[i][j].kind == "mountain":
                        counter = 0
                        for c in range(-1, 2):
                            for d in range(-1, 2):
                                if self.square[i + c][j + d].kind == "mountain":
                                    counter += 1
                        if counter < 3:
                            self.square[i][j].kind = "hills"
                            self.square[i][j].color = '\033[102m'
                            self.square[i][j].speed_drain = 1
                    elif self.square[i][j].kind == "water":
                        counter = 0
                        for c in range(-1, 2):
                            for d in range(-1, 2):
                                if self.square[i + c][j + d].kind == "water":
                                    counter += 1
                        if counter < 3:
                            self.square[i][j].kind = "hills"
                            self.square[i][j].color = '\033[102m'
                            self.square[i][j].speed_drain = 1

    def populator(self, input_rows, input_cols, number_of_players, computer):
        for i in range(number_of_players):
            start_row = 0
            end_row = 0
            start_col = 0
            end_col = 0
            mines = ["wood", "stone", "mercury", "crystal", "gems", "sulfur", "gold"]
            chests = ["Treasure", "Treasure", "Treasure", "Treasure"]
            buildings = ["XP_stone", "Pool", "Shrine1", "Shrine2"]
            artefacts = ["Sword", "Shield", "Boots"]
            archer = Hero("Archer", "monster", 1, 1, 1, 1, computer)
            archer2 = Hero("Archer", "monster", 1, 1, 1, 1, computer)
            archer.create_monster_army(5, 3)
            archer2.create_monster_army(5, 3)
            wolf_raider = Hero("Wolf Raider", "monster", 1, 1, 1, 1, computer)
            wolf_raider2 = Hero("Wolf Raider", "monster", 1, 1, 1, 1, computer)
            wolf_raider.create_monster_army(8, 3)
            wolf_raider2.create_monster_army(8, 3)
            angel = Hero("Angel", "monster", 1, 1, 1, 1, computer)
            angel.create_monster_army(1, 2)
            behemoth = Hero("Behemoth", "monster", 1, 1, 1, 1, computer)
            behemoth.create_monster_army(2, 1)
            mage = Hero("Mage", "monster", 1, 1, 1, 1, computer)
            mage2 = Hero("Mage", "monster", 1, 1, 1, 1, computer)
            mage.create_monster_army(4, 4)
            mage2.create_monster_army(4, 4)
            serpent_fly = Hero("Serpent Fly", "monster", 1, 1, 1, 1, computer)
            serpent_fly2 = Hero("Serpent Fly", "monster", 1, 1, 1, 1, computer)
            serpent_fly.create_monster_army(4, 5)
            serpent_fly2.create_monster_army(4, 5)
            enemies = [archer, angel, mage, serpent_fly, archer2, wolf_raider, behemoth, serpent_fly2, wolf_raider2,
                       mage2]
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

    def view_board(self, p, moving=False):
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
        print(f"{p.color} Wood:{p.resources.wood}        Mercury:{p.resources.mercury}      Stone:{p.resources.stone}      Sulfur:{p.resources.sulfur}"
              f"       Crystal:{p.resources.crystal}       Gems:{p.resources.gems}         Gold:{p.resources.gold}                                      "
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
        print(f"{p.color}Wood:{p.resources.wood} Mercury: {p.resources.mercury} Stone:{p.resources.stone} Sulfur:{p.resources.sulfur} "
            f"Crystal:{p.resources.crystal} Gems:{p.resources.gems} Gold:{p.resources.gold} {c.dw_color} {list(c.unit_names)[0]}:{c.available_units[0]} | "
            f"{list(c.unit_names)[1]}:{c.available_units[1]} | {list(c.unit_names)[2]}:{c.available_units[2]} | {list(c.unit_names)[3]}:"
            f"{c.available_units[3]} | {list(c.unit_names)[4]}:{c.available_units[4]}  |  {list(c.unit_names)[5]}:"
            f"{c.available_units[5]} | {list(c.unit_names)[6]}:{c.available_units[6]} \033[0m")

class Landscape:
    # os.system('color')
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
        self.placement = [0, 0]
        self.met_heroes = []
        self.speed_drain = input_speed
        self.has_hero = False
        self.hero = None
        self.color = ""
        self.has_object = False
        self.town = None
        self.operated_by = None
        self.object_name = ""
        self.seen = [0, 0, 0, 0, ]

        if self.kind == "plains": self.color = Landscape.PLAINS
        elif self.kind == "hills": self.color = Landscape.HILLS
        elif self.kind == "mountain": self.color = Landscape.MOUNTAIN
        elif self.kind == "water": self.color = Landscape.WATER
        elif self.kind == "forest": self.color = Landscape.FOREST

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
        if self.has_object and self.seen[input_player.number - 1] == 1:
            if self.operated_by:
                return f'{self.operated_by.color}' + '{: ^6s}'.format(self.object_name[:6]) + f'{Landscape.END}'
            elif type(self.object_name) == Hero:
                return f'{self.color}{Landscape.RED}' + '{: ^6s}'.format(
                    self.object_name.name[:6].upper()) + f'{Landscape.END}'
            else:
                return f'{self.color}{Landscape.DW}' + '{: ^6s}'.format(self.object_name[:6]) + f'{Landscape.END}'
        elif self.seen[input_player.number - 1] == 1:
            return f'{self.color}      {Landscape.END}'
        else:
            return f'      '

    def print_hero(self, input_player):
        if type(self.object_name) == Hero and self.seen[input_player.number - 1] == 1:
            amount = 0
            for unit in self.object_name.army:
                amount += unit.amount
            if amount > 10:
                return f'{self.color}{Landscape.RED}' + '{: ^6s}'.format("Lots") + f'{Landscape.END}'
            elif amount < 10:
                return f'{self.color}{Landscape.RED}' + '{: ^6s}'.format("Severa") + f'{Landscape.END}'
            elif amount < 4:
                return f'{self.color}{Landscape.RED}' + '{: ^6s}'.format("Few") + f'{Landscape.END}'
        elif self.has_hero and self.seen[input_player.number - 1] == 1:
            return f'{self.color}{Landscape.RED}' + '{: ^6s}'.format(self.hero.name[:4] + "," + str(self.hero.level)) + \
                   f'{Landscape.END}'
        elif self.seen[input_player.number - 1] == 1:
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
