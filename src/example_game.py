from game import Game
from player import Player
from gamemap import Structure
import clue

ME_1 = Player("red", clue.ONE_FROM_ANIMAL, teamname="alpha")
ME_2 = Player("orange", clue.DESERT_OR_SWAMP, teamname="beta")
EVA_1 = Player("cyan", None, teamname="gamma")
EVA_2 = Player("purple", None, teamname="epsilon")

GREEN_STONE = Structure("green", "stone", 12, 2)
GREEN_SHACK = Structure("green", "shack", 7, 3)
WHITE_STONE = Structure("white", "stone", 8, 6)
WHITE_SHACK = Structure("white", "shack", 10, 8)
BLUE_STONE = Structure("blue", "stone", 9, 1)
BLUE_SHACK = Structure("blue", "shack", 7, 4)

game = Game(["3N", "1S", "5S", "4S", "2N", "6S"], [ME_1, EVA_1, ME_2, EVA_2],
            [GREEN_STONE, GREEN_SHACK, WHITE_STONE, WHITE_SHACK, BLUE_STONE, BLUE_SHACK])

# TODO Add the structure ^^ to the map

# game.map.add_structure(8, 0, "blue", "stone")
# game.map.add_structure(6, 3, "blue", "shack")
# game.map.add_structure(11, 2, "green", "stone")
# game.map.add_structure(6, 3, "green", "shack")
# game.map.add_structure(7, 5, "white", "stone")
# game.map.add_structure(9, 7, "white", "shack")
print(len(game.possible_clues()))
for clue in game.possible_clues():
    print(clue)
