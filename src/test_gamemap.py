import unittest

from gamemap import Map, Structure, MapPiece

MAP_DESCRIPTOR = ["3N", "1S", "5S", "4S", "2N", "6S"]
STRUCTURES = [Structure("green", "stone", 12, 2), Structure("green", "shack", 7, 3), Structure("white", "stone", 8, 6),
              Structure("white", "shack", 10, 8), Structure("blue", "stone", 9, 1), Structure("blue", "shack", 7, 4)]
SAMPLE_LOCATIONS = [
    (2, 6, "F"), (3, 5, "D"), (3, 6, "W"), (4, 6, "W"),
    (9, 8, "S"), (8, 4, "F")
]

class TestMapGeneration(unittest.TestCase):

    def test_succesfully_generate_map(self) -> None:

        gamemap = Map(MAP_DESCRIPTOR, STRUCTURES)
        self.assertIsInstance(gamemap, Map)

    
    def test_no_duplicate_coordinates(self) -> None:

        gamemap = Map(MAP_DESCRIPTOR, STRUCTURES)
        coordinates = [(tile.x, tile.y) for tile in gamemap]

        self.assertEqual(len(coordinates), len(set(coordinates)))

    
    def test_extreme_coordinates_included(self) -> None:

        gamemap = Map(MAP_DESCRIPTOR, STRUCTURES)
        coordinates = [(tile.x, tile.y) for tile in gamemap]

        self.assertIn((1, 1), coordinates)
        self.assertIn((1, 9), coordinates)
        self.assertIn((12, 1), coordinates)
        self.assertIn((12, 9), coordinates)


    def test_structures_assigned_to_correct_coordinates(self) -> None:

        # Does not guarantee the correct structure type nor color

        gamemap = Map(MAP_DESCRIPTOR, STRUCTURES)
        for structure in STRUCTURES:
            x, y = (structure.x, structure.y)

            contains_structure = gamemap[x, y].has_shack() or gamemap[x, y].has_stone()

            self.assertTrue(contains_structure, "A structure coordinates did not match the coordinates of the map")


    def test_structure_color_matching(self) -> None:

        gamemap = Map(MAP_DESCRIPTOR, STRUCTURES)
        
        for structure in STRUCTURES:
            x, y = (structure.x, structure.y)

            contained_structure = gamemap[x, y].structure
            self.assertEqual(structure.color, contained_structure.color, "The color of the structure list and gamemap does not match")


    def test_structure_type_matching(self) -> None:

        gamemap = Map(MAP_DESCRIPTOR, STRUCTURES)
        
        for structure in STRUCTURES:
            x, y = (structure.x, structure.y)

            contained_structure = gamemap[x, y].structure
            self.assertEqual(structure.shape, contained_structure.shape, "The shape of the listed structures and gamemap does not match")


    def test_coordinate_biome(self) -> None:

        gamemap = Map(MAP_DESCRIPTOR, STRUCTURES)

        for x, y, biome in SAMPLE_LOCATIONS:
            
            tile = gamemap[x, y]
            self.assertEqual(tile.biome, biome, "The generated tiles did not match hand-checked tile: {}".format((x, y)))

if __name__ == "__main__":
    unittest.main()