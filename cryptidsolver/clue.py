from cryptidsolver.tile import MapTile
from cryptidsolver.gamemap import Map
from typing import Set

class Clue():
    def __init__(self, distance: int, distance_from: Set[str], clue_type: str = "biome") -> "Clue":
        self.distance = distance
        self.distance_from = set(distance_from)
        self.clue_type = clue_type

        self.__accepted_tiles = None


    def __repr__(self) -> str:
        return "Distance {} from {}".format(self.distance, self.distance_from)


    def accepted_tiles(self, gamemap: Map) -> set:

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


    def accepts_tile(self, tile: MapTile) -> bool:
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
