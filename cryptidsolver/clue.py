from typing import Set
from functools import lru_cache

from cryptidsolver.tile import MapTile
from cryptidsolver.gamemap import Map

class Clue():

    __slots__ = (
        "distance",
        "distance_from",
        "clue_type"
    )

    def __init__(self, distance: int, distance_from: Set[str], clue_type: str = "biome") -> "Clue":
        self.distance = distance
        self.distance_from = set(distance_from)
        self.clue_type = clue_type


    def __repr__(self) -> str:
        return "Distance {} from {}".format(self.distance, self.distance_from)


    def __hash__(self) -> int:
        return hash((self.distance, *sorted(list(self.distance_from)), self.clue_type))


    def __eq__(self, other) -> bool:

        if not isinstance(other, Clue):
            return False

        return self.distance == other.distance and self.distance_from == other.distance_from and self.clue_type == other.clue_type


    @lru_cache(maxsize=128)
    def accepted_tiles(self, gamemap: Map) -> Set[MapTile]:

        accepted_tiles = set()

        for tile in gamemap:
            
            x, y = (tile.x, tile.y)
            distanced_tiles = gamemap.tiles_on_distance(x, y, self.distance)

            for clued_distance in distanced_tiles:
                if self.__tile_confers_to_clue(clued_distance):
                    accepted_tiles.add(tile)

        assert len(accepted_tiles) != 0, "Should accept tiles"

        return accepted_tiles


    def __tile_confers_to_clue(self, tile: MapTile) -> bool:

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
