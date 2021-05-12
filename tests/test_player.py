import unittest

from cryptidsolver.game import Game
from cryptidsolver.gamemap import Map, Structure
from cryptidsolver.player import Player
from cryptidsolver.constant import clues

MAP_DESCRIPTOR = ["3N", "1S", "5S", "4S", "2N", "6S"]
STRUCTURES = [Structure("green", "stone", 12, 2), Structure("green", "shack", 7, 3), Structure("white", "stone", 8, 6),
              Structure("white", "shack", 10, 8), Structure("blue", "stone", 9, 1), Structure("blue", "shack", 7, 4)]

class TestPlayerClues(unittest.TestCase):

    def test_possible_clues_returns_known_clue(self) -> None:
        player = Player("red", clues.by_booklet_entry("alpha", 2))

        self.assertEqual(len(player.possible_clues()), 1, msg="Should have only one possible clue when player clue is known")

    
    def test_possible_clues_defaults_to_return_all_clues(self) -> None:
        player = Player("red", clue=None)

        # Hashes are incomparable. See clue.py/self.__accepted_tiles for bug details.
        original_collection = set(["{}{}".format(clue.distance, sorted(list(clue.distance_from))) for clue in clues.CLUE_COLLECTION])
        possible_clues = set(["{}{}".format(clue.distance, sorted(list(clue.distance_from))) for clue in player.possible_clues()])

        self.assertSetEqual(original_collection, possible_clues, msg="Should return all clues when no information is provided")


if __name__ == "__main__":
    unittest.main()
