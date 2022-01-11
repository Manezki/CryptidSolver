from typing import Set, FrozenSet
from functools import lru_cache

from cryptidsolver.tile import MapTile
from cryptidsolver.gamemap import Map

class Clue():

    __slots__ = (
        "distance",
        "distance_from",
        "clue_type",
        "inverted"
    )

    def __init__(
            self,
            distance: int,
            distance_from: Set[str],
            clue_type: str = "biome",
            inverted: bool = False
            ) -> "Clue":

        self.distance = distance
        self.distance_from = frozenset(distance_from)
        self.clue_type = clue_type
        self.inverted = inverted


    def __repr__(self) -> str:
        return (
            f"{'Not d' if self.inverted else 'D'}istance "
            f"{self.distance} from {self.distance_from}"
        )


    def __hash__(self) -> int:
        return hash(
            (self.distance, *sorted(list(self.distance_from)),
            self.clue_type, self.inverted)
            )


    def __eq__(self, other) -> bool:

        if not isinstance(other, Clue):
            return False

        return (self.distance == other.distance
            and self.distance_from == other.distance_from
            and self.clue_type == other.clue_type
            and self.inverted == other.inverted)


    @lru_cache(maxsize=128)
    def accepted_tiles(self, gamemap: Map) -> FrozenSet[MapTile]:

        accepted_tiles = set()

        for tile in gamemap:
            
            x, y = (tile.x, tile.y)
            distanced_tiles = gamemap.tiles_on_distance(x, y, self.distance)

            if self.inverted:
                if all(self.__tile_confers_to_clue(clue_distance_from_tile) for clue_distance_from_tile in distanced_tiles):
                    accepted_tiles.add(tile)
            else:
                if any(self.__tile_confers_to_clue(clue_distance_from_tile) for clue_distance_from_tile in distanced_tiles):
                    accepted_tiles.add(tile)

        assert len(accepted_tiles) != 0, "Should accept tiles"

        return frozenset(accepted_tiles)


    def __tile_confers_to_clue(self, tile: MapTile) -> bool:

        if self.clue_type == "biome":
            if tile.biome in self.distance_from:
                return True and (not self.inverted)
        elif self.clue_type == "animal":
            if tile.animal in self.distance_from:
                return True and (not self.inverted)
        else:
            try:
                if tile.structure.color in self.distance_from:
                    return True and (not self.inverted)
                elif tile.structure.shape in self.distance_from:
                    return True and (not self.inverted)
            except AttributeError:
                pass
        
        return self.inverted
