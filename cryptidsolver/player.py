from typing import FrozenSet

from cryptidsolver.clue import Clue
from cryptidsolver.gamemap import Map
from cryptidsolver.constant.clues import CLUE_COLLECTION, THREE_FROM_BLACK


class Player:

    __slots__ = ("color", "teamname", "clue", "cubes", "disks")

    def __init__(
        self, color: str, clue: Clue = None, teamname: str = None, inverted_clues: bool = False
    ) -> "Player":
        self.color = color
        self.teamname = teamname
        self.clue = clue
        self.cubes = []
        self.disks = []

    def possible_clues(self, gamemap: Map, inverted_clues: bool = False) -> FrozenSet[Clue]:

        possible_clues = set()

        if inverted_clues:  # pylint: disable=no-else-raise
            raise NotImplementedError("Missing implementation for inverted clues")
        else:
            clues = CLUE_COLLECTION.difference([THREE_FROM_BLACK])

        for clue in clues:
            # Clue is possible only if it accepts all disk locations and refuses all cube locations
            if all(
                gamemap[disk[0], disk[1]] in clue.accepted_tiles(gamemap) for disk in self.disks
            ):
                if all(
                    gamemap[cube[0], cube[1]] not in clue.accepted_tiles(gamemap)
                    for cube in self.cubes
                ):
                    possible_clues.add(clue)

        return frozenset(possible_clues)

    def __repr__(self) -> str:
        return f"{self.color.capitalize()} player"
