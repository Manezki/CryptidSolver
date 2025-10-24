import copy

from cryptidsolver.clue import Clue
from cryptidsolver.game import Game
from cryptidsolver.gamemap import Map
from cryptidsolver.player import Player
from cryptidsolver.tile import MapTile


def possible_clues_for_player(
    gamemap: Map, player: Player, inverted_clues: bool = False
) -> frozenset[Clue]:
    """
    Infer which clues are possible for the given player.

    Args:
        gamemap: Current gamemap.
        player: Player, for whom to infer the clues.
        inverted_clues: Should inverted clues be considered.

    Returns:
        Set of Clues that are possible for the player
    """
    return player.possible_clues(gamemap, inverted_clues)


def possible_clues_after_cube_placement(
    gamemap: Map,
    player: Player,
    placement: tuple[int, int],
    inverted_clues: bool = False,
) -> frozenset[Clue]:
    """
    Infer which clues would be possible after a cube placement.

    Args:
        gamemap: Current gamemap.
        player: Player for whom the cube would be placed.
        placement: cube placement location
        inverted_clues: Should inverted clues be considered.

    Returns:
        Set of Clues that would remain possible after cube placement.
    """

    imagined_player = copy.deepcopy(player)
    imagined_player.cubes.append(placement)

    return imagined_player.possible_clues(
        gamemap=gamemap, inverted_clues=inverted_clues
    )


def possible_clues_after_disk_placement(
    gamemap: Map,
    player: Player,
    placement: tuple[int, int],
    inverted_clues: bool = False,
) -> frozenset[Clue]:
    """
    Infer which clues would be possible after a disk placement.

    Args:
        gamemap: Current gamemap.
        player: Player for whom the disk would be placed.
        placement: Disk placement location
        inverted_clues: Should inverted clues be considered.

    Returns:
        Set of Clues that would remain possible after disk placement.
    """

    imagined_player = copy.deepcopy(player)
    imagined_player.disks.append(placement)

    return imagined_player.possible_clues(
        gamemap=gamemap, inverted_clues=inverted_clues
    )


def possible_tiles(
    game: Game, inverted_clues: bool = False
) -> dict[MapTile, float]:
    """
    Infer possible tiles from the clue possible clue combinations.

    Args:
        game: Current game.
        inverted_clues: Playing with inverted clue?

    Returns:
        MapTile with number of clue combinations pointing on them
    """

    return game.possible_tiles(inverted_clues)
