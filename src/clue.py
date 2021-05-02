class Clue():
    def __init__(self, distance, distance_from, clue_type="biome"):
        self.distance = distance
        self.distance_from = set(distance_from)
        self.clue_type = clue_type

        self.__accepted_tiles = None


    def __repr__(self):
        return "Distance {} from {}".format(self.distance, self.distance_from)


    def accepted_tiles(self, gamemap) -> set:

        if self.__accepted_tiles is not None:
            return self.__accepted_tiles.copy()

        accepted_tiles = set()

        for tile in gamemap:
            
            x, y = (tile.x, tile.y)
            distanced_tiles = gamemap.tiles_on_distance(x, y, self.distance)

            for clued_distance in distanced_tiles:
                if self.accepts_tile(clued_distance):
                    accepted_tiles.add(tile)

        assert len(accepted_tiles) != 0, "Should accept tiles"

        self.__accepted_tiles = accepted_tiles.copy()
        return accepted_tiles


    def accepts_tile(self, tile):
        if self.clue_type == "biome":
            if tile.biome in self.distance_from:
                return True
        elif self.clue_type == "animal":
            if tile.animal in self.distance_from:
                return True
        else:
            try:
                if tile.structure.color in self.distance_from:
                    return True
                elif tile.structure.shape in self.distance_from:
                    return True
            except AttributeError:
                pass
        
        return False


FOREST_OR_DESERT = Clue(0, set(["F", "D"]))
FOREST_OR_WATER = Clue(0, set(["F", "W"]))
FOREST_OR_SWAMP = Clue(0, set(["F", "S"]))
FOREST_OR_MOUNTAIN = Clue(0, set(["F", "M"]))
DESERT_OR_WATER = Clue(0, set(["D", "W"]))
DESERT_OR_SWAMP = Clue(0, set(["D", "S"]))
DESERT_OR_MOUNTAIN = Clue(0, set(["D", "M"]))
WATER_OR_SWAMP = Clue(0, set(["W", "S"]))
WATER_OR_MOUNTAIN = Clue(0, set(["W", "M"]))
SWAMP_OR_MOUNTAIN = Clue(0, set(["S", "M"]))

ONE_FROM_FOREST = Clue(1, set(["F"]))
ONE_FROM_DESERT = Clue(1, set(["D"]))
ONE_FROM_SWAMP = Clue(1, set(["S"]))
ONE_FROM_MOUNTAIN = Clue(1, set(["M"]))
ONE_FROM_WATER = Clue(1, set(["W"]))
ONE_FROM_ANIMAL = Clue(1, set(["cougar", "bear"]), clue_type="animal")

TWO_FROM_STANDING_STONE = Clue(2, set(["stone"]), clue_type="structure")
TWO_FROM_ABANDONED_SHACK = Clue(2, set(["shack"]), clue_type="structure")
TWO_FROM_COUGAR = Clue(2, set(["cougar"]), clue_type="animal")
TWO_FROM_BEAR = Clue(2, set(["bear"]), clue_type="animal")

THREE_FROM_BLUE = Clue(3, set(["blue"]), clue_type="structure")
THREE_FROM_WHITE = Clue(3, set(["white"]), clue_type="structure")
THREE_FROM_GREEN = Clue(3, set(["green"]), clue_type="structure")
THREE_FROM_BLACK = Clue(3, set(["black"]), clue_type="structure")

CLUE_COLLECTION = set([
    FOREST_OR_DESERT, FOREST_OR_WATER, FOREST_OR_SWAMP, FOREST_OR_MOUNTAIN, DESERT_OR_WATER,
    DESERT_OR_SWAMP, DESERT_OR_MOUNTAIN, WATER_OR_SWAMP, WATER_OR_MOUNTAIN, SWAMP_OR_MOUNTAIN,
    ONE_FROM_FOREST, ONE_FROM_DESERT, ONE_FROM_SWAMP, ONE_FROM_MOUNTAIN, ONE_FROM_WATER,
    ONE_FROM_ANIMAL, TWO_FROM_STANDING_STONE, TWO_FROM_ABANDONED_SHACK, TWO_FROM_COUGAR, TWO_FROM_BEAR,
    THREE_FROM_BLUE, THREE_FROM_WHITE, THREE_FROM_GREEN, THREE_FROM_BLACK
])
