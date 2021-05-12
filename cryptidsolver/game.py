import itertools
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

        self.possible_tiles = set(self.map)

        self.__reduce_possible_tiles_by_clues()


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

        # Cubes cannot be placed on tiles which already have a cube
        map_objects = set()
        for player in self.players:
            for tile in player.cubes:
                map_objects.add(tile)

        if (x, y) in map_objects:
            raise ValueError("Cubes cannot be placed on tiles with existing cubes")

        acting_player = self.players[self.gametick % len(self.players)]
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

        acting_player = self.players[self.gametick % len(self.players)]
        acting_player.disks.append((x, y))

        if advance_tick:
            self.gametick += 1

        return (acting_player, self.map[x, y])

    
    def __reduce_possible_tiles_by_clues(self) -> None:
        for player in self.players:
            if player.clue is not None:
                for tile in self.possible_tiles.copy():

                    x, y = (tile.x, tile.y)
                    distanced_tiles = self.map.tiles_on_distance(x, y, player.clue.distance)
                    
                    for clued_distance in distanced_tiles:
                        if clued_distance not in player.clue.accepted_tiles(self.map):
                            try:
                                self.possible_tiles.remove(clued_distance)
                            except KeyError:
                                # Possibly removed already
                                pass
    

    def possible_clues(self) -> set:
        clue_combinations = itertools.product(*[p.possible_clues for p in self.players])
        
        possible_combinations = set()

        for combination in clue_combinations:
            
            accepted_tiles = combination[0].accepted_tiles(self.map)
            for clue in combination[1:]:
                accepted_tiles = accepted_tiles.intersection(clue.accepted_tiles(self.map))

            if len(accepted_tiles) == 1:
                possible_combinations.add(combination)
        
        return possible_combinations