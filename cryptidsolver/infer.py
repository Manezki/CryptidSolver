from typing import List, Set, Tuple
from copy import deepcopy

from cryptidsolver.clue import Clue
from cryptidsolver.constant.clues import CLUE_COLLECTION, THREE_FROM_BLACK
from cryptidsolver.gamemap import Map

def possible_clues_from_placements(
        map: Map,
        player_cubes: List[Tuple[int, int]],
        player_disks: List[Tuple[int, int]],
        inverted_clues: bool = False
    ) -> Set[Clue]:

    possible_clues = set()

    if inverted_clues:
        raise NotImplementedError("Missing implementation for inverted clues")
    else:
        clues = CLUE_COLLECTION.difference([THREE_FROM_BLACK])

    for clue in clues:
        # Clue is possible only if it accepts all disk locations and refuses all cube locations
        if all([map[disk[0], disk[1]] in clue.accepted_tiles(map) for disk in player_disks]):
            if all([map[cube[0], cube[1]] not in clue.accepted_tiles(map) for cube in player_cubes]):
                possible_clues.add(deepcopy(clue))

    return possible_clues
