# Launching the game
* This game requires python3 installed. Set dir of the .py files as current working directory and type python3 main.py (in your terminal) to start the game.
* It is necessary to run this game in full screen on 1080p resolution with standard size of objects.
* If the map looks corrupted with black lines and/or you cannot see top and bottom action bars, your resolution is too low. Lower your font size in your terminal settings, open a new window with the new setting and run the game again.
* It is recommended to use a light grey background with black letters for your terminal / command line. This way, the selected colors in game will stand out more, as opposed to if you have a terminal using strong colours as default.
* When the map opens you should see two action bars; top and bottom. Make sure both of these can be seen; they display all available commands and information to you. If find yourself in a situation when you don't know what command to use or what you are able to do, look at the top action bar.
* **Third-party libraries: None!**

# How to play
### The map
Each player will start in a random place of the map, with a solid text displaying Town, and a plain text stating the first 4 letters of your hero's name followed by the hero's current level.
![adventuremap](https://user-images.githubusercontent.com/99674687/201476929-e5e94ca2-a062-44cb-8ae5-136dc6cdc4ec.png)
_Orrin, level 1, is moving between rogue enemy stacks of Serpent Flies and Archers, discovering the map as he goes. Artefact 'Boots of Speed' visible._

These commands are available to you, and always shown in the top action bar. Type them to enter corresponding state:
* **Move:** Use QWE, ASD, ZX to move in any direction (Q,E,Z,X for diagonal movement).
You must press Enter after each direction, moving one step at a time.
Enter the letter 'o' to exit movement. 

* **Town:**
Enter your town. The town can also be entered by moving a hero to the tile with the town.

* **View:**
Get a list of your current towns and heroes, and armies of these.

![view info](https://user-images.githubusercontent.com/99674687/201476932-2c71b669-b629-427f-8290-44a995d4be7b.png)

_Result from calling View in map mode. Player name, towns and heroes under the players control, and their army, are displayed._
* **Spells:**
Get a list of specified hero's spells. This is how you cast adventure spells such as Summon Boat.
* **End turn:**
End your turn.

If you move your hero to an object, the hero will confront it. If the object is a mine you will occupy the mine. If it is an artefact it will be picked up. If it's another object, it will be interacted with. If it is an enemy, marked with red text, a battle will commence.

### Battle
When in battle, other commands are available to you. The current units turn will be marked with yellow.
![battlefield](https://user-images.githubusercontent.com/99674687/201476930-f7a524b6-6ac1-4cd9-9594-73f7eb3117b8.png)

_The hero Zydar has attacked a rogue enemy (AI-controlled) stack of Serpent Flies. Gog, a ranged unit, is choosing its target. A Serpent Fly affected by the spell Slow is seen in the bottom right.
The "sp" attribute for the slowed Serpent Fly shows original speed since the unit is not active - when it reaches its turn, the sp number will be lower than its original, on behalf of the spell._

A units name will blink if it is a ranged unit. Type r to name your target and shoot it. 
When moving, you will use QWEASDZX to navigate, however, in Battle you are able to enter several steps at once. Moving 3 grids to the right at once can be done with ddd + Enter, for example, as opposed to d + enter, d + enter, d + enter etc as when in the adventure map.
To attack an enemy, just navigate to its tile.
* You can also throw spells in battle.
* You cannot retreat or negotiate out of a battle at the time of writing.

All available actions are listed in the top action bar in-game as commands.

### Town
![castle town](https://user-images.githubusercontent.com/99674687/201476931-7348f4c6-416e-4aa1-9ff4-d25e9f65d2cc.png)

_A view inside a Castle town as Player One: Red action and status bar for Player One, yellow highlights for Castle-specific information._

See the top action bar for available commands when in town. You can build new structures such as Town Hall, Citadel, upgrade your Mage Guild, and new Creature Dwellings, when in town. You can also hire new heroes in the Tavern, visit the mage guild to gain new spells, and recruit new units, either for your visiting hero or for town defense.

### Winning
Capture all towns and defeat all enemy heroes to win.

## CHEAT CODES
Do you want to try the game alone but it seems a hassle to take so many turns exploring everything?
Enter the hyphen symbol "-" instead of a direction when in the movement state to gain 1000 movement points for that hero. Then enter the movement state again to start moving.

# A brief technical overview of the features of this project.
The goal of this project is to implement the game Heroes of Might and Magic 3 into the terminal, with as many features from the original game as possible.

The game is written in Python 3. I spent around 11 days, about 6 hours a day, planning and coding this game. More hours were spent testing and squashing some bugs.
* The program consists of three .py files: main, renderer and entities. There are no third-party libraries used.
* Main shows startup info, collects number of players, player names, chosen kingdoms, calls methods to create objects for the setup and keeps track of current players turn. 
* Renderer runs rendering of the town view. There is also a map and battlefield renderer - these are not in renderer.py but in the third file 'entities.py'.
* Entities contains everything else that is necessary for the game to run, including following objects:

### Player
The player object houses attributes for player name, kingdom, in-game resources such as gold and stone, daily resource increase from mines.
It houses a list of heroes and towns belonging to this player as well as current day and week.

### Town
Every player starts with a town matching the players' chosen kingdom. There are several differences between towns depending on kingdom, such as highlight color, dwelling names, dwelling and unit cost and maximum Mage Guild level.
Naturally, the units for purchase in each town are unique to that kingdom, as are the spells in the mage guild.
Some attributes for the town object include currently operating player, available units for recruitment, built dwellings/structures, defending army, if such exists.
Currently available spells, future available spells. Kingdom color. Prices of buildings.

If a player conquers a town, they can enter it and recruit units from that kingdom, build structures and do everything the former owner of the town could.

### Hero
Each hero has a name, an operating player and attributes for the different skills; Attack, defense, knowledge and spell power.
The hero also keeps their spellbook, if they have one (buy one in a mage guild if not) and a list of artefacts. The hero object also keeps track of movement points and the hero's army, and if they currently have a boat and are able to cross water.

### Unit
The unit is a troop in a town or hero army, and is operated by such entity. They have names and attributes directly copied from the original game, such as Gremlin, Angel, Behemoth, Mage, Naga, etc. 
The unit also keeps track of any spells currently affecting them and their location on the battlefield.

### Gameboard and Landscape
These two objects works in tandem to display either the map or the battlefield, or even the town.
In short, a gameboard is a 2D-array of landscapes.
For the adventure map the landscape object hold types such as hills and water, with resource mines or rogue enemies, heroes etc. The landscape object also keeps track of if they are discovered and therefore should be rendered and visible, to the current player.

On a battlefield the landscapes are void of such, instead they are used to house and display troops and corresponding info.

In a town the landscape objects hold symbols that, when the complete 2D-array is printed, display the current buildings of the town.

## Methods
The game has 40 unique methods for the different needs of the users. Entities.py contains over 2200 lines of code. They will not be accounted for here, but for a few mentions:

### Map creation
The map is created from randomly generated landscapes, where the chance for mountains and water to spawn is lower.
On the other hand, if mountain or water should spawn, the chance for adjacent tiles to also spawn as such is greatly improved.

After the map has been generated a new method looks for tiles of water and mountains that ended up lonely and change them to another, passable landscape. The result is a map with mountain ridges and rivers of water, or at least, more resemblance of such.

Then, according to current number of players, each player is randomly placed on the map. Hero and town are placed on the same tile.
If there are 2 players, one start in the top and one in the bottom half.
If there are 3 or 4 players, everyone gets a corner of the map each.
The map is then filled with more objects. Every player gets a full set of mines available to gain control of, 3 different artefacts to pickup, and rogue enemies, as well as experience stones, treasures and shrines of magic, all in "their" starting zone of the map.

The populator method makes sure no objects are placed on water or on top of a mountain. 

### The Battlefield
The battlefield is one of the most complex chain of methods in the game.
When two heroes or a hero and a rogue enemy, or a hero and a town with an army confronts each other, a battlefield is generated and the armies of the opposing sides placed on each side of the battlefield.
Then the assault starts and each player controls a unit, one per turn. When all the units on either side of the battlefield are dead, the battle is over.

If the hero has a spellbook they can throw a spell. The spell could be direct damage or effect the attributes of own or enemy troops. If it is an effect spell, the targeted unit will receive a status bar, green or red depending on positive or negative effect, with the title of the spell affecting them. More than one spell can affect a unit, however only one can be displayed at a time.

If the current unit is a ranged unit, they can make a ranged attack by typing command "r" and typing the first 5 letters, or the full name, of targeted unit.

A melee unit will receive a retaliation after attack, if the attacked unit has not already retaliated this round.

Both attack and defense damage is affected by controlling hero's (if any) attack and defense skill, and spell damage is affected by hero spell power.

### AI:
If the enemy is a rogue enemy, that is an enemy not controlled by a human player, it will be controlled by an AI. The AI will effectively select a unit on your side as target, based on which unit who will receive the most damage. Ranged units are favored.
For example, a stack of 30 units of Pikemen with total health of 300 hp will be chosen over a stack with 1 unit of Pikeman, since a blow to the 30 Pikemen will kill more units than a blow to 1 Pikeman.

After a target is chosen the AI will shoot it if controlling a ranged unit, or move towards it, as far as possible. The AI will find a way on its own, and can sidestep own or enemy units in order to reach its target, with very few exceptions.
Such an exception can be the AI unit being at the edge of the battlefield, the target also at the edge, and another unit blocking passage, making the AI go out-of-bounds of the battlefield array when trying to move around the obstacle. However steps have been taken to avoid this and it has never been encountered at the time of writing.

### Town rendering
The town renders every time a town command is issued, and as such it is "real-time". You can build a new structure and have it appear in front of your eyes without leaving and entering the town. At the time of this writing the towns are rendered to look the same, since coding different renderings is quite time-consuming. What differs is colouring and names of the dwelling.


## Limitations
There are quite a few limitations of the game when comparing to the original game. Some mentions:

* You cannot exchange artefacts or armies between heroes or towns, and defeating a hero will not yield their artefacts.
* A hero can have, for example, two sword artefacts simultaneously and receive an attack bonus for both of them.
* There is no marketplace, blacksmith or several other kingdom-specific buildings (such as the Treasury or Library).
* Only spells up to and including level 2 are available at time of writing.
* There are no skills such as Offense, Magic Resistance, Estates, Wisdom etc to learn for heroes. 
* Only four kingdoms are available: Tower, Castle, Rampart and Inferno
* The upgraded version of each unit is not available at the time of writing.
* A player starts with one hero and can only hire two more in total.
* No option to save or load a game
* There are no obelisks and no grail to be found, neither is there an "underground" map available.
* Movement on the map is done one step at a time. On the battlefield you can insert several steps at a time and then press enter.
* The different Fort/Citadel/Castle buildings are purely cosmetic and for creature dwelling requirements at the time; There is no defence provided if your town is attacked.
* A hero cannot equip a ballista, catapult, or other devices of war.

## Future updates
* Switching to storing kingdom specific information in a database.
* Adding defence structures for town defense in-battle, and therefore naturally, a catapult for the attacking hero
* Adding more kingdoms
* Possibly adding the original music
* An AI for controlling a hero, unlocking the possibility of a computer-controlled player
* Placing of loose piles of resources on the map
* And much else.



