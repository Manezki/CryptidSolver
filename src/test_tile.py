from tile import _BiomeTile, MapTile
import unittest


class TestMapTile(unittest.TestCase):

    def test_succesfully_conver_from_BiomeTile_with_animal(self) -> None:

        biome_tile = _BiomeTile("F", animal="cougar")

        converted = MapTile._from_BiomeTile(biome_tile, 1, 2, structure=None)

        self.assertEqual(converted.biome, "F", msg="The biome of the converted tile should be the same as the biome tile's.")
        self.assertEqual(converted.animal, "cougar", msg="The animal of the biome tile's should be present in converted MapTile.")
        self.assertEqual(converted.x, 1, msg="The x coordinate should not change during the conversion.")
        self.assertEqual(converted.y, 2, msg="The y coordinate should not change during the conversion.")


if __name__ == "__main__":
    unittest.main()