import unittest

from cryptidsolver.game import Game
from cryptidsolver.gamemap import Map, Structure
from cryptidsolver.player import Player
from cryptidsolver.constant import clues

MAP_DESCRIPTOR = ["3N", "1S", "5S", "4S", "2N", "6S"]
STRUCTURES = [Structure("green", "stone", 12, 2), Structure("green", "shack", 7, 3), Structure("white", "stone", 8, 6),
              Structure("white", "shack", 10, 8), Structure("blue", "stone", 9, 1), Structure("blue", "shack", 7, 4)]

class TestPossibleClues(unittest.TestCase):

    def setUp(self) -> None:
        # Redefine for every test as state persists otherwise
        PLAYER_1 = Player("orange", clues.by_booklet_entry("alpha", 2), teamname="alpha")
        PLAYER_2 = Player("cyan", None, teamname="beta")
        PLAYER_3 = Player("purple", None, teamname="epsilon")

        PLAYERS = [PLAYER_1, PLAYER_2, PLAYER_3]

        self.game = Game(MAP_DESCRIPTOR, PLAYERS, STRUCTURES)

    def test_returns_non_empty_collection(self) -> None:

        self.assertTrue(len(self.game.players[0].possible_clues(self.game.map)) != 0, msg="Should always return non-empty collection")


if __name__ == "__main__":
    unittest.main()
