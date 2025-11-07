import unittest

from cryptidsolver.constant import clues
from cryptidsolver.gamemap import Map, Structure
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


class TestPossibleClues(unittest.TestCase):
    def test_returns_non_empty_collection(self) -> None:
        self.assertTrue(
            len(
                Player(
                    "orange", clues.WATER_OR_MOUNTAIN, teamname="alpha"
                ).possible_clues(Map(MAP_DESCRIPTOR, STRUCTURES))
            )
            != 0,
            msg="Should always return non-empty collection",
        )

    def test_defaults_to_return_all_clues(self) -> None:
        # We don't know anything about the players clue
        player = Player("cyan", None, teamname="beta")

        original_collection = clues.CLUE_COLLECTION.difference(
            {clues.THREE_FROM_BLACK}
        )
        possible_clues = player.possible_clues(Map(MAP_DESCRIPTOR, STRUCTURES))

        self.assertSetEqual(
            original_collection,
            possible_clues,
            msg="Should return all clues when no cubes or disks are present",
        )

    def test_cubes_limit_possibile_clues(self) -> None:
        player = Player(
            "orange", clues.by_booklet_entry("alpha", 2), teamname="alpha"
        )
        # Place a cube for the 1st player
        player.cubes.append((1, 1))

        possible_clues = player.possible_clues(Map(MAP_DESCRIPTOR, STRUCTURES))

        # Cube on (1, 1) excludes the following clues:
        # 2 from cougar, 1 from animal, swamp, 1 from swamp
        original_collection = clues.CLUE_COLLECTION.difference(
            {clues.THREE_FROM_BLACK}
        )
        reduced_collection = original_collection.difference(
            {
                clues.FOREST_OR_SWAMP,
                clues.DESERT_OR_SWAMP,
                clues.WATER_OR_SWAMP,
                clues.SWAMP_OR_MOUNTAIN,
                clues.ONE_FROM_SWAMP,
                clues.ONE_FROM_ANIMAL,
                clues.TWO_FROM_COUGAR,
            }
        )

        self.assertSetEqual(
            reduced_collection,
            possible_clues,
            msg="Placement of cube should remove associated clues",
        )


if __name__ == "__main__":
    unittest.main()
