from enum import Enum
from typing import Iterable, List, FrozenSet
from cryptidsolver.structure import Structure
from cryptidsolver.tile import _BiomeTile, MapTile


class MapPiece(Enum):
    P1 = [[_BiomeTile("W"), _BiomeTile("S"), _BiomeTile("S")],
          [_BiomeTile("W"), _BiomeTile("S"), _BiomeTile("S")],
          [_BiomeTile("W"), _BiomeTile("W"), _BiomeTile("D")],
          [_BiomeTile("W"), _BiomeTile("D"), _BiomeTile("D", "bear")],
          [_BiomeTile("F"), _BiomeTile("F"), _BiomeTile("D", "bear")],
          [_BiomeTile("F"), _BiomeTile("F"), _BiomeTile("F", "bear")]]

    P2 = [[_BiomeTile("S", animal="cougar"), _BiomeTile("S"), _BiomeTile("S")],
          [_BiomeTile("F", animal="cougar"), _BiomeTile("S"), _BiomeTile("M")],
          [_BiomeTile("F", animal="cougar"), _BiomeTile("F"), _BiomeTile("M")],
          [_BiomeTile("F"), _BiomeTile("D"), _BiomeTile("M")],
          [_BiomeTile("F"), _BiomeTile("D"), _BiomeTile("M")],
          [_BiomeTile("F"), _BiomeTile("D"), _BiomeTile("D")]]

    P3 = [[_BiomeTile("S"), _BiomeTile("S", animal="cougar"), _BiomeTile("M", animal="cougar")],
          [_BiomeTile("S"), _BiomeTile("S", animal="cougar"), _BiomeTile("M")],
          [_BiomeTile("F"), _BiomeTile("F"), _BiomeTile("M")],
          [_BiomeTile("F"), _BiomeTile("M"), _BiomeTile("M")],
          [_BiomeTile("F"), _BiomeTile("W"), _BiomeTile("W")],
          [_BiomeTile("W"), _BiomeTile("W"), _BiomeTile("W")]]
    
    P4 = [[_BiomeTile("D"), _BiomeTile("D"), _BiomeTile("D")],
          [_BiomeTile("D"), _BiomeTile("D"), _BiomeTile("D")],
          [_BiomeTile("M"), _BiomeTile("M"), _BiomeTile("D")],
          [_BiomeTile("M"), _BiomeTile("W"), _BiomeTile("F")],
          [_BiomeTile("M"), _BiomeTile("W"), _BiomeTile("F")],
          [_BiomeTile("M"), _BiomeTile("W", animal="cougar"), _BiomeTile("F", animal="cougar")]]
    
    P5 = [[_BiomeTile("S"), _BiomeTile("S"), _BiomeTile("D")],
          [_BiomeTile("S"), _BiomeTile("D"), _BiomeTile("D")],
          [_BiomeTile("S"), _BiomeTile("D"), _BiomeTile("W")],
          [_BiomeTile("M"), _BiomeTile("W"), _BiomeTile("W")],
          [_BiomeTile("M"), _BiomeTile("M"), _BiomeTile("W", animal="bear")],
          [_BiomeTile("M"), _BiomeTile("M", animal="bear"), _BiomeTile("W", animal="bear")]]
    
    P6 = [[_BiomeTile("D", animal="bear"), _BiomeTile("M", animal="bear"), _BiomeTile("M")],
          [_BiomeTile("D"), _BiomeTile("M"), _BiomeTile("W")],
          [_BiomeTile("S"), _BiomeTile("S"), _BiomeTile("W")],
          [_BiomeTile("S"), _BiomeTile("S"), _BiomeTile("W")],
          [_BiomeTile("S"), _BiomeTile("F"), _BiomeTile("W")],
          [_BiomeTile("F"), _BiomeTile("F"), _BiomeTile("F")]]
    

class Map():

    __slots__ = (
        "map"
    )

    def __init__(self, map_description: List[str], structures: Iterable[Structure]) -> "Map":
        """
        Describe the map using the map pieces ({number}{south/north})

        Args:
            description - list: Map pieces (num, heading) in an ordered list (Starting from top-left to bottom-left, continue top-right to bottom-right).
            structures - iterable[Structures]: Map structures to be added to the map 
        
        Returns:
            map - [[Tile]]: 12x9 matrix of describing the game map.
        """

        assert len(structures) == 6 or len(structures) == 8, "Game must have 6 or 8 structures"
        assert len(map_description) == 6, "Map description has to be 6 pieces"

        self.map = self._generate_terrain_map(map_description, structures)


    @staticmethod
    def neighbouring_coordinates(x: int, y: int) -> FrozenSet:
        neighbours = set()

        for row in [x-1, x , x+1]:
            for col in [y-1, y, y+1]:
                
                # Odd rows have left & right neighbours in y-1 and y.
                if x%2 == 1 and col == y+1 and row != x:
                    continue
                elif x%2 == 0 and col == y-1 and row != x:
                    continue

                if 1 <= row <= 12 and 1 <= col <= 9:
                    neighbours.add((row, col))

        return frozenset(neighbours)


    def tiles_on_distance(self, x: int, y: int, d: int) -> FrozenSet:
        
        neighbours = set()
        neighbours.add(self.__getitem__([x, y]))

        for _ in range(d):

            new_neighbours = set()

            for point in neighbours:
                for neig_x, neig_y in self.neighbouring_coordinates(point.x, point.y):
                    new_neighbours.add(self[neig_x, neig_y])
            neighbours = neighbours.union(new_neighbours)

        return frozenset(neighbours)


    def _reverse_map_piece(self, map_piece: MapPiece) -> list:
        
        reversed_piece = []
        
        for width in range(5, -1, -1):

            reverse_col = []
            for height in range(2, -1, -1):

                reverse_col.append(map_piece[width][height])
            
            reversed_piece.append(reverse_col)

        return reversed_piece

    def _generate_terrain_map(self, description: List[str], structures: List[Structure]) -> List[List[MapTile]]:
        """
        Form a map from map pieces.

        Args:
            description - list: Map pieces (num, heading) in an ordered list. Left column first from top down.
            structures - iterable: Map structures to be added to the map 
        
        Returns:
            map - [[]]: Fullsize matrix of Tile-objects describing the game map.
        """

        lookup_mapPiece = {"1": MapPiece.P1, "2": MapPiece.P2, "3": MapPiece.P3,
                        "4": MapPiece.P4, "5": MapPiece.P5, "6": MapPiece.P6,}

        lookup_structure = {(structure.x, structure.y): structure for structure in structures}

        game_map = [[], [], [], [], [], [], [], [], [], [], [], []]

        for num, descriptor in enumerate(description):
            piece_num, piece_heading = descriptor[0], descriptor[1]

            map_piece = lookup_mapPiece[piece_num].value
            if piece_heading.lower() == "s":
                map_piece = self._reverse_map_piece(map_piece)

            # The 6x3 pieces are added in blocks starting from top-left corner. Offset for block coordinates can then be
            # calculated from the block number
            y_offset = (num % 3) * 3
            x_offset = (num // 3) * 6

            for x, col in enumerate(map_piece):
                
                for y, biome in enumerate(col):

                    x_coord = x + x_offset
                    y_coord = y + y_offset

                    # Add one to convert into humanlike strictly positive coordinates
                    map_tile = MapTile._from_BiomeTile(biome, x_coord + 1, y_coord + 1, structure = lookup_structure.get((x_coord + 1, y_coord + 1), None))
                    
                    game_map[x_coord].append(map_tile)

        # The 0,0 coordinate is on the top-left corner
        return game_map


    def __iter__(self) -> MapTile:
        for col in self.map:
            for tile in col:
                yield tile


    def __repr__(self) -> str:
        stringify = ""
        for row in range(len(self.map[0])):
            for col in range(len(self.map)):
                element = self.map[col][row]
                stringify += "| {:^8} |".format(str(element))
            stringify += "\n"
        return stringify


    def __getitem__(self, coordinates) -> MapTile:

        assert len(coordinates) == 2, "Two coordinates required to fetch a tile"
        assert isinstance(coordinates[0], int), "First coordinate has to be an integer"
        assert isinstance(coordinates[1], int), "Second coordinate has to be an integer"

        # Convert from strictly positive coordinates to 0-starting-indexing
        return self.map[coordinates[0] - 1][coordinates[1] - 1]
