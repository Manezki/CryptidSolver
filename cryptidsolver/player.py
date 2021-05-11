from typing import Set
from copy import copy

from cryptidsolver.constant.clues import CLUE_COLLECTION, THREE_FROM_BLACK
from cryptidsolver.clue import Clue

class Player():
    def __init__(self, color: str, clue: Clue = None, teamname: str = None, inverse_clues: bool = False) -> "Player":
        self.color = color
        self.teamname = teamname
        self.clue = clue
        self.cubes = []
        self.disks = []

    def possible_clues(self) -> Set[Clue]:

        possible_clues = set()

        for clue in CLUE_COLLECTION:
            # Clue is possible only if it accepts all disk locations and refuses all cube locations
            if all([clue.accepts_tile(disk) for disk in self.disks]):
                if all([~clue.accepts_tile(cube) for cube in self.cubes]):
                    possible_clues.add(copy(clue))

        return possible_clues

    def __repr__(self) -> str:
        return "{} player".format(self.color.capitalize())
