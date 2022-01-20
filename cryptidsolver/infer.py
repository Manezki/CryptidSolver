import copy

from typing import Dict, FrozenSet, Tuple

from cryptidsolver.clue import Clue
from cryptidsolver.gamemap import Map
from cryptidsolver.tile import MapTile
from cryptidsolver.player import Player
from cryptidsolver.game import Game


def possible_clues_for_player(
    gamemap: Map, player: Player, inverted_clues: bool = False
) -> FrozenSet[Clue]:
    """
    Infer which clues are possible for the given player.

    Args:
        gamemap (Map): Current gamemap.
        player (Player): Player, for whom to infer the clues.
        inverted_clues (bool, optional): Should inverted clues be considered. Defaults to False.

    Returns:
        FrozenSet[Clue]: Set of Clues that are possible for the player
    """
    return player.possible_clues(gamemap, inverted_clues)


def possible_clues_after_cube_placement(
    gamemap: Map, player: Player, placement: Tuple[int, int], inverted_clues: bool = False
) -> FrozenSet[Clue]:
    """
    Infer which clues would be possible after a cube placement.

    Args:
        gamemap (Map): Current gamemap.
        player (Player): Player for whom the cube would be placed.
        placement (Tuple[int, int]): cube placement location
        inverted_clues (bool, optional): Should inverted clues be considered. Defaults to False.

    Returns:
        FrozenSet[Clue]: Set of Clues that would remain possible after cube placement.
    """

    imagined_player = copy.deepcopy(player)
    imagined_player.cubes.append(placement)

    return imagined_player.possible_clues(gamemap=gamemap, inverted_clues=inverted_clues)


def possible_clues_after_disk_placement(
    gamemap: Map, player: Player, placement: Tuple[int, int], inverted_clues: bool = False
) -> FrozenSet[Clue]:
    """
    Infer which clues would be possible after a disk placement.

    Args:
        gamemap (Map): Current gamemap.
        player (Player): Player for whom the disk would be placed.
        placement (Tuple[int, int]): Disk placement location
        inverted_clues (bool, optional): Should inverted clues be considered. Defaults to False.

    Returns:
        FrozenSet[Clue]: Set of Clues that would remain possible after disk placement.
    """

    imagined_player = copy.deepcopy(player)
    imagined_player.disks.append(placement)

    return imagined_player.possible_clues(gamemap=gamemap, inverted_clues=inverted_clues)


def possible_tiles(game: Game, inverted_clues: bool = False) -> Dict[MapTile, float]:
    """
    Infer possible tiles from the clue possible clue combinations.

    Args:
        game: Game - Current game.
        inverted_clues: bool - Playing with inverted clue?

    Returns:
        Dict[MapTile: int]] - MapTile with number of clue combinations pointing on them
    """

    return game.possible_tiles(inverted_clues)
