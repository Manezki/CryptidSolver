from typing import Set, FrozenSet
from functools import lru_cache

from cryptidsolver.tile import MapTile
from cryptidsolver.gamemap import Map


class Clue:
    """
    Represents a Clue
    """

    __slots__ = ("distance", "distance_from", "clue_type", "inverted")

    def __init__(
        self,
        distance: int,
        distance_from: Set[str],
        clue_type: str = "biome",
        inverted: bool = False,
    ) -> None:
        """
        Construct a game clue

        Args:
            distance (int): Distance mentioned on clue. For 'on X', use 0.
            distance_from (Set[str]): Distance from what
            clue_type (str): Type of clue biome/animal/structure. Defaults to "biome".
            inverted (bool, optional): Is the clue inverted, i.e. 'not X'. Defaults to False.
        """

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
            (self.distance, *sorted(list(self.distance_from)), self.clue_type, self.inverted)
        )

    def __eq__(self, other) -> bool:

        if not isinstance(other, Clue):
            return False

        return (
            self.distance == other.distance
            and self.distance_from == other.distance_from
            and self.clue_type == other.clue_type
            and self.inverted == other.inverted
        )

    @lru_cache(maxsize=128)
    def accepted_tiles(self, gamemap: Map) -> FrozenSet[MapTile]:
        """
        Infer which tiles are possible for given clue

        Args:
            gamemap (Map): Current gamemap

        Returns:
            FrozenSet[MapTile]: Tiles that are possible according to the clue
        """

        accepted_tiles = set()

        for tile in gamemap:

            x, y = (tile.x, tile.y)
            distanced_tiles = gamemap.tiles_on_distance(x, y, self.distance)

            if self.inverted:
                if all(
                    self.__tile_confers_to_clue(clue_distance_from_tile)
                    for clue_distance_from_tile in distanced_tiles
                ):
                    accepted_tiles.add(tile)
            else:
                if any(
                    self.__tile_confers_to_clue(clue_distance_from_tile)
                    for clue_distance_from_tile in distanced_tiles
                ):
                    accepted_tiles.add(tile)

        assert len(accepted_tiles) != 0, "Clue should always accept at least a single tile"

        return frozenset(accepted_tiles)

    def __tile_confers_to_clue(self, tile: MapTile) -> bool:

        if self.clue_type == "biome":
            if tile.biome in self.distance_from:
                return not self.inverted
        elif self.clue_type == "animal":
            if tile.animal in self.distance_from:
                return not self.inverted
        elif tile.structure is not None:
            if tile.structure.color in self.distance_from:
                return not self.inverted
            if tile.structure.shape in self.distance_from:
                return not self.inverted

        return self.inverted
