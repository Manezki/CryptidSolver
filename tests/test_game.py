import unittest

from cryptidsolver.game import Game
from cryptidsolver.gamemap import Map, Structure
from cryptidsolver.player import Player
from cryptidsolver.constant import clues

MAP_DESCRIPTOR = ["3N", "1S", "5S", "4S", "2N", "6S"]
STRUCTURES = [Structure("green", "stone", 12, 2), Structure("green", "shack", 7, 3), Structure("white", "stone", 8, 6),
              Structure("white", "shack", 10, 8), Structure("blue", "stone", 9, 1), Structure("blue", "shack", 7, 4)]

PLAYER_1 = Player("orange", clues.by_booklet_entry("alpha", 2), teamname="alpha")
PLAYER_2 = Player("cyan", None, teamname="beta")
PLAYER_3 = Player("purple", None, teamname="epsilon")

PLAYERS = [PLAYER_1, PLAYER_2, PLAYER_3]


class TestCubePlacement(unittest.TestCase):

    def setUp(self) -> None:
        self.game = Game(MAP_DESCRIPTOR, PLAYERS, STRUCTURES)


    def test_cube_added_to_player(self) -> None:

        before_placement = len(self.game.players[0].cubes)

        # Confers to the players clue
        self.game.place_cube(1, 1)

        self.assertEqual(len(self.game.players[0].cubes), before_placement + 1)


    def test_gametick_advanced(self) -> None:

        before_placement = self.game.gametick

        self.game.place_cube(1, 1)

        self.assertEqual(self.game.gametick, before_placement + 1)


class TestDiskPlacement(unittest.TestCase):

    def setUp(self) -> None:
        self.game = Game(MAP_DESCRIPTOR, PLAYERS, STRUCTURES)


    def test_disk_added_to_player(self) -> None:

        before_placement = len(self.game.players[0].disks)

        self.game.place_disk(1, 1)

        self.assertEqual(len(self.game.players[0].disks), before_placement + 1)


    def test_gametick_advanced(self) -> None:

        before_placement = self.game.gametick

        self.game.place_disk(1, 1)

        self.assertEqual(self.game.gametick, before_placement + 1)


if __name__ == "__main__":
    unittest.main()
