import unittest
from structure import Structure


class TestCreateStructure(unittest.TestCase):

    def test_accepted_blue_stone_onboard(self):

        self.assertIsNotNone(Structure("blue", "stone", 1, 1), "Should allow creation of correctly positioned, recognized object")


    def test_reject_coordinates_out_of_board_lower(self):

        with self.assertRaises(ValueError, msg="Should not accept coordinates outside of the board"):
            Structure("blue", "stone", -1, -1)


    def test_reject_coordinates_out_of_board_over(self):

        with self.assertRaises(ValueError, msg="Should not accept coordinates outside of the board"):
            Structure("blue", "stone", 13, 10)


    def test_reject_unrecognized_colors(self):

        with self.assertRaises(ValueError, msg="Unrecognized colors (green, blue, white, black) are not to be accepted"):
            Structure("orange", "stone", 1, 1)


if __name__ == "__main__":
    unittest.main()