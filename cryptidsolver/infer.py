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
    return player.possible_clues(gamemap, inverted_clues)


def possible_clues_after_cube_placement(
    gamemap: Map, player: Player, placement: Tuple[int, int], inverted_clues: bool = False
) -> FrozenSet[Clue]:

    imagined_player = copy.deepcopy(player)
    imagined_player.cubes.append(placement)

    return imagined_player.possible_clues(gamemap=gamemap, inverted_clues=inverted_clues)


def possible_clues_after_disk_placement(
    gamemap: Map, player: Player, placement: Tuple[int, int], inverted_clues: bool = False
) -> FrozenSet[Clue]:

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
