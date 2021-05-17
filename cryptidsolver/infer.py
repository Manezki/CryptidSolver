import copy

from typing import List, Set, Tuple

from cryptidsolver.clue import Clue
from cryptidsolver.gamemap import Map
from cryptidsolver.tile import MapTile
from cryptidsolver.player import Player
from cryptidsolver.game import Game


def possible_clues_for_player(
        gamemap: Map,
        player: Player,
        inverted_clues: bool = False
    ) -> Set[Clue]:
    return player.possible_clues(gamemap, inverted_clues)


def possible_clues_after_cube_placement(
        gamemap: Map,
        player: Player,
        placement: Tuple[int, int],
        inverted_clues: bool = False
    ) -> Set[Clue]:

    imagined_player = copy.deepcopy(player)
    imagined_player.cubes.append(placement)

    return imagined_player.possible_clues(gamemap = gamemap, inverted_clues = inverted_clues)


def possible_clues_after_disk_placement(
        gamemap: Map,
        player: Player,
        placement: Tuple[int, int],
        inverted_clues: bool = False
    ) -> Set[Clue]:

    imagined_player = copy.deepcopy(player)
    imagined_player.disks.append(placement)

    return imagined_player.possible_clues(gamemap = gamemap, inverted_clues = inverted_clues)


def possible_tiles(
        game: Game,
        inverted_clues: bool = False
    ) -> List[Tuple[MapTile, float]]:
    """
    Infer possible tiles from the clue possible clue combinations.

    Args:
        game: Game - Current game.
        inverted_clues: bool - Playing with inverted clue?

    Returns:
        List[Tuple[MapTile, float]] - Ordered list of maptiles with associated probabilities for monster
    """

    return game.possible_tiles(inverted_clues)
