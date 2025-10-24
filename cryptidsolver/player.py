from cryptidsolver.clue import Clue
from cryptidsolver.constant.clues import CLUE_COLLECTION, THREE_FROM_BLACK
from cryptidsolver.gamemap import Map


class Player:
    __slots__ = ("clue", "color", "cubes", "disks", "teamname")

    def __init__(
        self,
        color: str,
        clue: Clue | None = None,
        teamname: str | None = None,
        inverted_clues: bool = False,
    ) -> None:
        self.color = color
        self.teamname = teamname
        self.clue = clue
        self.cubes: list[tuple[int, int]] = []
        self.disks: list[tuple[int, int]] = []

    def possible_clues(
        self, gamemap: Map, inverted_clues: bool = False
    ) -> frozenset[Clue]:
        possible_clues = set()

        if inverted_clues:
            raise NotImplementedError(
                "Missing implementation for inverted clues"
            )
        clues = CLUE_COLLECTION.difference({THREE_FROM_BLACK})

        for clue in clues:
            # Clue is possible only if it accepts all disk locations and refuses all cube locations
            if all(
                gamemap[disk[0], disk[1]] in clue.accepted_tiles(gamemap)
                for disk in self.disks
            ):
                if all(
                    gamemap[cube[0], cube[1]]
                    not in clue.accepted_tiles(gamemap)
                    for cube in self.cubes
                ):
                    possible_clues.add(clue)

        return frozenset(possible_clues)

    def __repr__(self) -> str:
        return f"{self.color.capitalize()} player"
