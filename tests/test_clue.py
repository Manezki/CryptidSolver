import unittest
import cryptidsolver.constant.clues as clue
from cryptidsolver.game import Game
from cryptidsolver.player import Player
from cryptidsolver.structure import Structure

class TestClueAcceptsTiles(unittest.TestCase):

    def setUp(self) -> None:
        self.game = Game(["6N", "5S", "2N", "3N", "4N", "1S"], 
                         [Player("Red", clue=clue.FOREST_OR_MOUNTAIN),
                          Player("Green"), Player("Brown"), Player("Purple")],
                         [Structure("Blue", "Shack", x=1, y=7), Structure("Blue", "Stone", x=8, y=3),
                          Structure("White", "Stone", x=2, y=2), Structure("White", "Shack", x=11, y=7),
                          Structure("Green", "Shack", x=5, y=6), Structure("Green", "Stone", x=12, y=4)])
        self.forest_or_mountain_coordinates = {(1, 2), (1, 3), (1, 5), (1, 6), (2, 2), (2, 5), (2, 6), (2, 7), (2, 9),
                                               (3, 6), (3, 7), (3, 8), (3, 9), (4, 7), (4, 9), (5, 2), (5, 7), (5, 9),
                                               (6, 1), (6, 2), (6, 3), (6, 7), (7, 3), (7, 7), (7, 8), (7, 9), (8, 3),
                                               (8, 8), (8, 9), (9, 1), (9, 2), (9, 3), (9, 4), (9, 5), (10, 1),
                                               (10, 2), (10, 3), (10, 4), (10, 6), (11, 1), (11, 4), (11, 6), (12, 4),
                                               (12, 6)}

    def test_accepted_tiles_have_matching_coordinates(self) -> None:

        accepted_tiles = self.game.players[0].clue.accepted_tiles(self.game.map)

        for tile in accepted_tiles:
            self.assertIn((tile.x, tile.y), self.forest_or_mountain_coordinates, msg="'{} @ x{} y{}' of accepted tiles does not have coordinates matching to hand-checked tiles".format(tile, tile.x, tile.y))


if __name__ == "__main__":
    unittest.main()
