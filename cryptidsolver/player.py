from cryptidsolver.constant.clues import CLUE_COLLECTION, THREE_FROM_BLACK
from cryptidsolver.clue import Clue

class Player():
    def __init__(self, color: str, clue: Clue = None, teamname: str = None, inverse_clues: bool = False) -> "Player":
        self.color = color
        self.teamname = teamname
        self.clue = clue
        self.cubes = []
        self.disks = []

        if clue is None:
            self.possible_clues = CLUE_COLLECTION.copy()
            if not inverse_clues:
                self.possible_clues.remove(THREE_FROM_BLACK)
        else:
            self.possible_clues = set([self.clue])

    def __repr__(self) -> str:
        return "{} player".format(self.color.capitalize())
