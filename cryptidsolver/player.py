from typing import Set

from cryptidsolver.clue import Clue
from cryptidsolver.gamemap import Map
from cryptidsolver import infer

class Player():
    def __init__(self, color: str, clue: Clue = None, teamname: str = None, inverse_clues: bool = False) -> "Player":
        self.color = color
        self.teamname = teamname
        self.clue = clue
        self.cubes = []
        self.disks = []


    def possible_clues(self, map: Map, inverted_clues: bool = False) -> Set[Clue]:
        return infer.possible_clues_from_placements(map, self.cubes, self.disks, inverted_clues)


    def __repr__(self) -> str:
        return "{} player".format(self.color.capitalize())
