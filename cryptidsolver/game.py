import itertools
import functools
from typing import List, Tuple

from cryptidsolver.gamemap import Map
from cryptidsolver.player import Player
from cryptidsolver.structure import Structure
from cryptidsolver.tile import MapTile


class Game():
    def __init__(self, map_descriptor: List[str], ordered_players: List[Player], structures: List[Structure]) -> "Game":
        self.players = ordered_players
        self.map = Map(map_descriptor, structures)

        self.gametick = 0


    def current_player(self) -> Player:
        return self.players[self.gametick % len(self.players)]


    def accepts_cube(self, x: int, y: int) -> bool:

        # Cubes cannot be placed on tiles which already have a cube
        map_objects = set()
        for player in self.players:
            for tile in player.cubes:
                map_objects.add(tile)

        if (x, y) in map_objects:
            return False

        return True


    def place_cube(self, x: int, y: int, advance_tick: bool = True) -> Tuple[Player, MapTile]:
        """
        Place a cube for the acting player.

        Args:
            x - int : x coordinate for the cube. In range 1 ... 12
            y - int : y coordinate for the cube. In range 1 ... 9
            advance_tick - bool : Advance gametick. This should be false when players place a cube after unsuccesful question.
        
        Returns:
            Tuple[Player, MapTile] : Acting player with the MapTile at location [x, y]
        """

        if not self.accepts_cube(x, y):
            raise ValueError("Cubes cannot be placed on tiles with existing cubes")

        acting_player = self.current_player()
        acting_player.cubes.append((x, y))

        if advance_tick:
            self.gametick += 1

        return (acting_player, self.map[x, y])


    def place_disk(self, x: int, y: int, advance_tick: bool = True) -> Tuple[Player, MapTile]:
        """
        Place a disk for the acting player.

        Args:
            x - int : x coordinate for the disk. In range 1 ... 12
            y - int : y coordinate for the disk. In range 1 ... 9
            advance_tick - bool : Advance gametick. This should be false when players respond to monster location guess.

        Returns:
            Tuple[Player, MapTile] : Acting player with the MapTile at location [x, y]
        """

        acting_player = self.current_player()
        acting_player.disks.append((x, y))

        if advance_tick:
            self.gametick += 1

        return (acting_player, self.map[x, y])


    def possible_tiles(self, inverted_clues: bool = False) -> List[Tuple[MapTile, float]]:
        """
        Infer possible tiles from the clue possible clue combinations.

        Args:
            gamemap: Map - Current gamemap.
            players: List[Player] - List of players.

        Returns:
            Dict[MapTile: int]] - MapTile with number of clue combinations pointing on them
        """

        if inverted_clues:
            raise NotImplementedError("Inverse clues not implemented")

        potential_clues = []

        for player in self.players:
            if player.clue is not None:
                # Add known clues
                potential_clues.append(set([player.clue]))
            else:
                potential_clues.append(player.possible_clues(self.map))

        potential_tiles = {}
        total = 0

        for combination in itertools.product(*potential_clues):
            possible_tiles = functools.reduce(lambda x, y: x & y.accepted_tiles(self.map), combination, set(self.map))
            if len(possible_tiles) == 1:
                tile = possible_tiles.pop()
                total += 1

                if tile in potential_tiles:
                    potential_tiles[tile] += 1
                else:
                    potential_tiles[tile] = 1

        potential_tiles = {k: v/total for k, v in potential_tiles.items()}

        return potential_tiles
