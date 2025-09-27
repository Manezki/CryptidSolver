import unittest

from cryptidsolver.constant import clues
from cryptidsolver.game import Game
from cryptidsolver.gamemap import Structure
from cryptidsolver.player import Player

MAP_DESCRIPTOR = ["3N", "1S", "5S", "4S", "2N", "6S"]
STRUCTURES = [
    Structure("green", "stone", 12, 2),
    Structure("green", "shack", 7, 3),
    Structure("white", "stone", 8, 6),
    Structure("white", "shack", 10, 8),
    Structure("blue", "stone", 9, 1),
    Structure("blue", "shack", 7, 4),
]


class TestCubePlacement(unittest.TestCase):
    def setUp(self) -> None:
        # Redefine for every test as state persists otherwise
        player_1 = Player(
            "orange", clues.by_booklet_entry("alpha", 2), teamname="alpha"
        )
        player_2 = Player("cyan", None, teamname="beta")
        player_3 = Player("purple", None, teamname="epsilon")

        players = [player_1, player_2, player_3]

        self.game = Game(MAP_DESCRIPTOR, players, STRUCTURES)

    def test_cube_added_to_player(self) -> None:
        before_placement = len(self.game.players[0].cubes)

        # Confers to the players clue
        self.game.place_cube(1, 1)

        self.assertEqual(len(self.game.players[0].cubes), before_placement + 1)

    def test_gametick_advances(self) -> None:
        before_placement = self.game.gametick

        self.game.place_cube(1, 1)

        self.assertEqual(self.game.gametick, before_placement + 1)

    def test_rejects_placement_when_cube_present(self) -> None:
        self.game.place_cube(1, 1)

        with self.assertRaises(
            ValueError, msg="Cubes cannot be placed on tiles with cubes"
        ):
            self.game.place_cube(1, 1)


class TestAcceptsCube(unittest.TestCase):
    def setUp(self) -> None:
        # Redefine for every test as state persists otherwise
        player_1 = Player(
            "orange", clues.by_booklet_entry("alpha", 2), teamname="alpha"
        )
        player_2 = Player("cyan", None, teamname="beta")
        player_3 = Player("purple", None, teamname="epsilon")

        players = [player_1, player_2, player_3]

        self.game = Game(MAP_DESCRIPTOR, players, STRUCTURES)

    def test_rejects_when_cube_present(self) -> None:
        self.game.place_cube(1, 1)

        self.assertFalse(
            self.game.accepts_cube(1, 1),
            msg="Cubes cannot be placed on tiles with other cubes",
        )

    def test_accepts_when_no_cube_present(self) -> None:
        self.assertTrue(
            self.game.accepts_cube(1, 1),
            msg="Cubes can be placed on tiles with other cubes",
        )


class TestDiskPlacement(unittest.TestCase):
    def setUp(self) -> None:
        player_1 = Player(
            "orange", clues.by_booklet_entry("alpha", 2), teamname="alpha"
        )
        player_2 = Player("cyan", None, teamname="beta")
        player_3 = Player("purple", None, teamname="epsilon")

        players = [player_1, player_2, player_3]

        self.game = Game(MAP_DESCRIPTOR, players, STRUCTURES)

    def test_disk_added_to_player(self) -> None:
        before_placement = len(self.game.players[0].disks)

        self.game.place_disk(1, 1)

        self.assertEqual(len(self.game.players[0].disks), before_placement + 1)

    def test_gametick_advances(self) -> None:
        before_placement = self.game.gametick

        self.game.place_disk(1, 1)

        self.assertEqual(self.game.gametick, before_placement + 1)


class TestPossibleTiles(unittest.TestCase):
    def test_known_clues_return_a_single_tile(self) -> None:
        player_1 = Player(
            "red", clues.by_booklet_entry("alpha", 2), teamname="alpha"
        )
        player_2 = Player(
            "orange", clues.by_booklet_entry("beta", 79), teamname="beta"
        )
        player_3 = Player(
            "purple", clues.by_booklet_entry("epsilon", 28), teamname="epsilon"
        )

        players = [player_1, player_2, player_3]

        game = Game(MAP_DESCRIPTOR, players, STRUCTURES)

        possible_tiles = game.possible_tiles()

        self.assertTrue(
            len(possible_tiles) == 1,
            msg="Should always return a single maptile when, all clues are known",
        )


if __name__ == "__main__":
    unittest.main()
