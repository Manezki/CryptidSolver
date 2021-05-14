from typing import Set
from copy import deepcopy

from cryptidsolver.constant.clues import CLUE_COLLECTION
from cryptidsolver.clue import Clue

class Player():
    def __init__(self, color: str, clue: Clue = None, teamname: str = None, inverse_clues: bool = False) -> "Player":
        self.color = color
        self.teamname = teamname
        self.clue = clue
        self.cubes = []
        self.disks = []


    def __repr__(self) -> str:
        return "{} player".format(self.color.capitalize())
