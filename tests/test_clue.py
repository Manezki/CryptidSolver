import unittest
from copy import deepcopy

from cryptidsolver.constant import clues
from cryptidsolver.game import Game
from cryptidsolver.player import Player
from cryptidsolver.structure import Structure
from cryptidsolver.clue import Clue

MAP_DESCRIPTOR = ["3N", "1S", "5S", "4S", "2N", "6S"]
STRUCTURES = [
    Structure("green", "stone", 12, 2),
    Structure("green", "shack", 7, 3),
    Structure("white", "stone", 8, 6),
    Structure("white", "shack", 10, 8),
    Structure("blue", "stone", 9, 1),
    Structure("blue", "shack", 7, 4),
]


class TestAcceptedTiles(unittest.TestCase):
    def setUp(self) -> None:
        self.game = Game(
            ["6N", "5S", "2N", "3N", "4N", "1S"],
            [
                Player("Red", clue=clues.FOREST_OR_MOUNTAIN),
                Player("Green"),
                Player("Brown"),
                Player("Purple"),
            ],
            [
                Structure("Blue", "Shack", x=1, y=7),
                Structure("Blue", "Stone", x=8, y=3),
                Structure("White", "Stone", x=2, y=2),
                Structure("White", "Shack", x=11, y=7),
                Structure("Green", "Shack", x=5, y=6),
                Structure("Green", "Stone", x=12, y=4),
            ],
        )
        self.forest_or_mountain_coordinates = {
            (1, 2),
            (1, 3),
            (1, 5),
            (1, 6),
            (2, 2),
            (2, 5),
            (2, 6),
            (2, 7),
            (2, 9),
            (3, 6),
            (3, 7),
            (3, 8),
            (3, 9),
            (4, 7),
            (4, 9),
            (5, 2),
            (5, 7),
            (5, 9),
            (6, 1),
            (6, 2),
            (6, 3),
            (6, 7),
            (7, 3),
            (7, 7),
            (7, 8),
            (7, 9),
            (8, 3),
            (8, 8),
            (8, 9),
            (9, 1),
            (9, 2),
            (9, 3),
            (9, 4),
            (9, 5),
            (10, 1),
            (10, 2),
            (10, 3),
            (10, 4),
            (10, 6),
            (11, 1),
            (11, 4),
            (11, 6),
            (12, 4),
            (12, 6),
        }

    def test_accepted_tiles_have_matching_coordinates(self) -> None:

        if self.game.players[0].clue is None:
            self.fail("Test requires player 1 to have a clue defined")

        accepted_tiles = self.game.players[0].clue.accepted_tiles(self.game.map)

        for tile in accepted_tiles:
            self.assertIn(
                (tile.x, tile.y),
                self.forest_or_mountain_coordinates,
                msg=(
                    f"'{tile} @ x{tile.x} y{tile.y}' "
                    "of accepted tiles does not have coordinates matching to hand-checked tiles"
                ),
            )

    def test_cougar_clue_accepts_tile_next_to_cougar_zone(self) -> None:

        # Encountered during manual testing

        PLAYER_1 = Player("orange", clues.by_booklet_entry("alpha", 2), teamname="alpha")
        PLAYER_2 = Player("cyan", None, teamname="beta")
        PLAYER_3 = Player("purple", None, teamname="epsilon")

        PLAYERS = [PLAYER_1, PLAYER_2, PLAYER_3]

        game = Game(MAP_DESCRIPTOR, PLAYERS, STRUCTURES)

        self.assertIn(
            game.map[1, 1],
            clues.TWO_FROM_COUGAR.accepted_tiles(game.map),
            msg="2 from cougar should accept tile next to cougar zone",
        )

    def test_repeated_calls_are_cached(self) -> None:

        two_from_cougar = deepcopy(clues.TWO_FROM_COUGAR)

        PLAYER_1 = Player("orange", clues.by_booklet_entry("alpha", 2), teamname="alpha")
        PLAYER_2 = Player("cyan", None, teamname="beta")
        PLAYER_3 = Player("purple", None, teamname="epsilon")

        PLAYERS = [PLAYER_1, PLAYER_2, PLAYER_3]
        game = Game(MAP_DESCRIPTOR, PLAYERS, STRUCTURES)

        _ = two_from_cougar.accepted_tiles(game.map)

        before_call = two_from_cougar.accepted_tiles.cache_info()

        _ = two_from_cougar.accepted_tiles(game.map)

        after_call = two_from_cougar.accepted_tiles.cache_info()

        self.assertEqual(
            after_call[0],
            before_call[0] + 1,
            msg="Number of cache hits should increase when called with same parameters",
        )


class TestHashing(unittest.TestCase):
    def test_new_objects_evaluate_same_hash(self) -> None:
        a = Clue(1, set(["bear", "cougar"]), clue_type="animal")
        b = Clue(1, set(["bear", "cougar"]), clue_type="animal")

        self.assertEqual(
            hash(a), hash(b), msg="Fresh clues with same parameters should be comparable"
        )

    def test_accepted_tiles_maintains_hash(self) -> None:

        a = Clue(1, set(["bear", "cougar"]), clue_type="animal")
        b = Clue(1, set(["bear", "cougar"]), clue_type="animal")

        self.assertEqual(
            hash(a), hash(b), msg="Fresh clues with same parameters should be comparable"
        )

        PLAYER_1 = Player("orange", clues.by_booklet_entry("alpha", 2), teamname="alpha")
        PLAYER_2 = Player("cyan", None, teamname="beta")
        PLAYER_3 = Player("purple", None, teamname="epsilon")

        PLAYERS = [PLAYER_1, PLAYER_2, PLAYER_3]

        game = Game(MAP_DESCRIPTOR, PLAYERS, STRUCTURES)

        _ = b.accepted_tiles(game.map)

        self.assertEqual(
            hash(a), hash(b), msg="Invoking class methods should not change the hash of a clue"
        )

    def test_set_unpacking_order_does_not_change_hash(self) -> None:

        a = set(["bear", "cougar"])
        b = set(["bear", "cougar"])

        tupled_a = (*a,)
        tupled_b = (*b,)

        i = 0

        while tupled_a != tupled_b:

            b = set(["bear", "cougar"])
            tupled_b = (*b,)

            i += 1

            if i >= 1000:
                self.fail("Did not find sets with different unpacking order")

        clue_a = Clue(1, a, clue_type="animal")
        clue_b = Clue(1, b, clue_type="animal")

        self.assertEqual(
            hash(clue_a), hash(clue_b), msg="Clue hash should be independent of set-unpacking order"
        )


class TestEquality(unittest.TestCase):
    def test_different_instances_of_same_clues_evaluate_to_be_same(self) -> None:

        a = Clue(1, set(["bear", "cougar"]), clue_type="animal")
        b = Clue(1, set(["bear", "cougar"]), clue_type="animal")

        self.assertEqual(a, b, msg="Instances of same clue should evaluate to be equal")

    def test_accepted_tiles_comparison(self) -> None:

        a = Clue(1, set(["bear", "cougar"]), clue_type="animal")
        b = Clue(1, set(["bear", "cougar"]), clue_type="animal")

        self.assertEqual(a, b, msg="Instances of same clue should evaluate to be equal")

        PLAYER_1 = Player("orange", clues.by_booklet_entry("alpha", 2), teamname="alpha")
        PLAYER_2 = Player("cyan", None, teamname="beta")
        PLAYER_3 = Player("purple", None, teamname="epsilon")

        PLAYERS = [PLAYER_1, PLAYER_2, PLAYER_3]

        game = Game(MAP_DESCRIPTOR, PLAYERS, STRUCTURES)

        _ = b.accepted_tiles(game.map)

        self.assertEqual(
            a,
            b,
            msg="Invoking class methods should not change equality comparison of Clue instance",
        )

    def test_set_creation_order_does_not_change_equality(self) -> None:

        a = Clue(1, set(["bear", "cougar"]), clue_type="animal")
        b = Clue(1, set(["cougar", "bear"]), clue_type="animal")

        self.assertEqual(a, b, msg="Order of distance_from set should not change equality")


class TestInvertedClue(unittest.TestCase):
    def test_inverting_a_clue_changes_repr(self) -> None:
        normal = Clue(0, set(["F", "D"]), clue_type="biome", inverted=False)
        inverted = Clue(0, set(["F", "D"]), clue_type="biome", inverted=True)

        normal_repr = str(normal)
        inverted_repr = str(inverted)

        self.assertNotEqual(
            normal_repr, inverted_repr, msg="Inverting a clue should produce a different 'repr'"
        )

    def test_inverting_a_clue_changes_hash(self) -> None:
        normal = Clue(0, set(["F", "D"]), clue_type="biome", inverted=False)
        inverted = Clue(0, set(["F", "D"]), clue_type="biome", inverted=True)

        normal_repr = hash(normal)
        inverted_repr = hash(inverted)

        self.assertNotEqual(
            normal_repr, inverted_repr, msg="Inverting a clue should produce a different hash"
        )

    def test_inverted_is_unequal_to_noninverted(self) -> None:
        normal = Clue(0, set(["F", "D"]), clue_type="biome", inverted=False)
        inverted = Clue(0, set(["F", "D"]), clue_type="biome", inverted=True)

        self.assertNotEqual(
            normal, inverted, msg="Inverted clue must be UNEQUAL to non-inverted clue"
        )

    def test_inverted_clue_rejects_associated_tiles(self) -> None:

        PLAYER_1 = Player("red", Clue(1, {"S"}, clue_type="biome", inverted=True), teamname="alpha")
        PLAYER_2 = Player("cyan", None, teamname="beta")
        PLAYER_3 = Player("purple", None, teamname="epsilon")

        game = Game(
            ["4N", "3N", "6S", "1S", "5S", "2S"],
            [PLAYER_1, PLAYER_2, PLAYER_3],
            [
                Structure("black", "stone", 2, 3),
                Structure("green", "shack", 4, 1),
                Structure("blue", "shack", 5, 8),
                Structure("blue", "stone", 6, 3),
                Structure("white", "shack", 7, 2),
                Structure("green", "stone", 8, 2),
                Structure("black", "shack", 8, 7),
                Structure("white", "stone", 8, 9),
            ],
        )

        inverted_one_from_swamp_clue = Clue(1, {"S"}, clue_type="biome", inverted=True)

        self.assertNotIn(
            game.map[1, 3],
            inverted_one_from_swamp_clue.accepted_tiles(game.map),
            msg="'Not 1 from swamp' should reject tile next to swamp",
        )


if __name__ == "__main__":
    unittest.main()
