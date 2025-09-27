import argparse
import copy
from typing import TypedDict

from cryptidsolver import infer
from cryptidsolver.constant.clues import by_booklet_entry
from cryptidsolver.constant.limits import _MIN_PLAYERS
from cryptidsolver.game import Game
from cryptidsolver.player import Player
from cryptidsolver.structure import Structure
from cryptidsolver.tile import MapTile

_N_ARGUMENTS_ANSWER = 5
_N_ARGUMENTS_PLACEMENT = 4


class PotentialQuestion(TypedDict):
    tile: MapTile | None
    fitness: float
    results: dict[str, tuple[int, int]]


def parse_player(stringified: str) -> Player:
    alphabet_lookup = {
        "a": "alpha",
        "b": "beta",
        "g": "gamma",
        "d": "delta",
        "e": "epsilon",
    }

    if stringified.startswith("@"):
        acting_player = True
        stringified = stringified[1:]
    else:
        acting_player = False

    color, booklet = stringified.split("_")
    (booklet_alpha, booklet_num) = (
        alphabet_lookup[booklet[0].lower()],
        int(booklet[1:]),
    )

    if acting_player:
        return Player(color, by_booklet_entry(booklet_alpha, booklet_num))

    return Player(color, clue=None)


def parse_structure(stringified: str) -> Structure:
    stringified = stringified.lower()

    if not stringified.startswith(("green", "white", "black", "blue")):
        raise ValueError(
            "Structure parameter has to start by color definition"
        )

    if stringified.startswith(("green", "white", "black")):
        color_str = stringified[:5]
    else:
        # Blue
        color_str = stringified[:4]

    shape_lookup = {"ss": "stone", "as": "shack"}

    offset = len(color_str)

    (struct, loc) = (
        shape_lookup[stringified[offset + 1 : offset + 3]],
        stringified[offset + 4 :],
    )
    (x_str, y_str) = loc.split(",")
    (x_coord, y_coord) = (int(x_str), int(y_str))

    return Structure(color_str, struct, x_coord, y_coord)


def question_fitness(n_locations: int, n_combinations: int) -> float:
    if n_locations == 1:
        return 0

    if n_combinations == 1 and n_locations != 1:
        return -9999

    if n_locations == 0:
        return -9999

    if n_combinations == 0:
        return -9999

    return (-n_locations + 1) * (n_combinations**0.5)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Interactive Cryptid solver")
    parser.add_argument(
        "--map",
        type=str,
        nargs=6,
        required=True,
        help="Map description. Columnar from top-left as '(Mappiece number)(S/N)'",
    )
    parser.add_argument(
        "--players",
        type=str,
        nargs="+",
        required=True,
        help=(
            "Ordered players as '[@](color)_(clue alphabet)(clue number)'"
            " with @ for acting player"
        ),
    )
    parser.add_argument(
        "--structures",
        type=str,
        nargs="+",
        required=True,
        help="Structures as '(color)_([SS/AS])_(x),(y)'",
    )
    args = parser.parse_args()

    players = [parse_player(player) for player in args.players]
    structures = [parse_structure(structure) for structure in args.structures]

    __minimal_structures = [
        ("white", "stone"),
        ("white", "shack"),
        ("green", "stone"),
        ("green", "shack"),
        ("blue", "stone"),
        ("blue", "shack"),
    ]

    assert len(players) >= _MIN_PLAYERS, (
        "Game should have at least three players"
    )
    assert all(
        ms in [(s.color.lower(), s.shape.lower()) for s in structures]
        for ms in __minimal_structures
    ), "All the basic structures should be present"

    game = Game(args.map, players, structures)

    # TODO: Refactor main-loop into a function

    while True:
        cmd = input().lower().strip()

        if (
            cmd.startswith("place")
            and len(cmd.split(" ")) == _N_ARGUMENTS_PLACEMENT
        ):
            try:
                (_, mapObject, x_str, y_str) = cmd.split(" ")
                (x, y) = (int(x_str), (int(y_str)))

                if mapObject == "c":
                    action = game.place_cube(x, y)
                    print(f"{action[0]} placed cube on {action[1]}")
                elif mapObject == "d":
                    action = game.place_disk(x, y)
                    print(f"{action[0]} placed disk on {action[1]}")
                else:
                    raise ValueError

            except ValueError:
                pass

        elif (
            cmd.startswith("answer")
            and len(cmd.split(" ")) == _N_ARGUMENTS_ANSWER
        ):
            (_, color, mapObject, x_str, y_str) = cmd.split(" ")
            (x, y) = (int(x_str), (int(y_str)))

            try:
                player_colors = [
                    player.color.lower() for player in game.players
                ]
                matched_player = game.players[
                    player_colors.index(color.lower())
                ]

            except ValueError:
                print(
                    f"Player with color '{color}' was not found. Please check your command"
                )
                continue

            if mapObject == "c":
                matched_player.cubes.append((x, y))
                print(f"{matched_player.color} placed cube on {(x, y)}")
            elif mapObject == "d":
                matched_player.disks.append((x, y))
                game.gametick += 1
                print(f"{matched_player.color} placed cube on {(x, y)}")
            else:
                print(
                    f"Placed object '{mapObject}' was not "
                    "cube (c) or disk (d). Pease check your command"
                )

        elif cmd == "possible clues":
            for player in game.players:
                print(f"{player}'s possible clues")
                print("----------")

                if player.clue is not None:
                    print(player.clue)
                else:
                    for clue in player.possible_clues(game.map):
                        print(clue)

                print("")

        elif cmd == "infer cube placement":
            player = game.current_player()
            before_placement = player.possible_clues(game.map)

            placement_alternatives = {}

            for tile in game.map:
                if game.accepts_cube(tile.x, tile.y):
                    # Does not account for impossible clues - that is cannot produce
                    # clue-combination that singles out a tile.

                    clues_after_placement = (
                        infer.possible_clues_after_cube_placement(
                            game.map, player, (tile.x, tile.y)
                        )
                    )

                    placement_reduces_clues = len(
                        before_placement.difference(clues_after_placement)
                    )
                    placement_alternatives[tile] = placement_reduces_clues

            minimum_reveal = sorted(
                placement_alternatives.items(), key=lambda x: x[1]
            )[0]

            print(
                f"Place cube on x:{minimum_reveal[0].x} y:{minimum_reveal[0].y} "
                f"to reduce {minimum_reveal[1]} clues"
            )

        elif cmd == "location prob":
            possible_locations_unsorted = game.possible_tiles()
            possible_locations = sorted(
                possible_locations_unsorted.items(), key=lambda x: x[1]
            )

            print("Location probabilities")
            print("---------")
            for location, probability in possible_locations:
                print(
                    f"Tile x:{location.x} y:{location.y} has probability of {probability}"
                )

        elif cmd == "question":
            print()

            possible_tiles = game.possible_tiles()
            n_possible_locations = len(possible_tiles.keys())
            # BUG: possible_tiles.values have been normalized earlier (to probability),
            # so the sum equals n_possible_locations always
            n_possible_combinations = round(sum(possible_tiles.values()))

            imagined_game = copy.deepcopy(game)

            except_current_player = [
                player
                for player in imagined_game.players
                if player != imagined_game.current_player()
            ]

            potential_questions: dict[Player, PotentialQuestion] = {
                player: {
                    "tile": None,
                    "fitness": question_fitness(
                        n_possible_locations, n_possible_combinations
                    ),
                    "results": {
                        "locations": (
                            n_possible_locations,
                            n_possible_locations,
                        ),
                        "combinations": (
                            n_possible_locations,
                            n_possible_locations,
                        ),
                    },
                }
                for player in except_current_player
            }

            for player in except_current_player:
                # No point asking questions from players with known clues, i.e. acting players
                if player.clue is not None:
                    continue

                for tile in imagined_game.map:
                    # imagine cube placement
                    player.cubes.append((tile.x, tile.y))

                    after_locations = imagined_game.possible_tiles()
                    n_negative_locations_after = len(after_locations.keys())
                    n_negative_combinations_after = round(
                        sum(after_locations.values())
                    )

                    player.cubes.remove((tile.x, tile.y))

                    # imagine disk placement

                    player.disks.append((tile.x, tile.y))

                    after_locations = imagined_game.possible_tiles()
                    n_positive_locations_after = len(after_locations.keys())
                    n_positive_combinations_after = round(
                        sum(after_locations.values())
                    )

                    player.disks.remove((tile.x, tile.y))

                    fitness = (
                        question_fitness(
                            n_negative_locations_after,
                            n_negative_combinations_after,
                        )
                        + question_fitness(
                            n_positive_locations_after,
                            n_positive_combinations_after,
                        )
                    ) / 2

                    if fitness >= potential_questions[player]["fitness"]:
                        results = {
                            "locations": (
                                n_positive_locations_after,
                                n_negative_locations_after,
                            ),
                            "combinations": (
                                n_positive_combinations_after,
                                n_negative_combinations_after,
                            ),
                        }
                        potential_questions[player] = {
                            "tile": tile,
                            "fitness": fitness,
                            "results": results,
                        }

            favored_question = max(
                potential_questions.items(), key=lambda x: x[1]["fitness"]
            )

            if favored_question[1]["tile"] is None:
                raise AttributeError(
                    "Encountered a question which does "
                    f"not point to tile. Question: {favored_question}"
                )

            print("Question found.")
            print(
                f"Ask player: {favored_question[0]} about x: {favored_question[1]['tile'].x} "
                f"y: {favored_question[1]['tile'].y}"
            )

        else:
            print(
                """Did not quite catch that. Try one of the following commands:
            - place [c/d] x y : to place Cube or Disk
            - answer color [c/d] x y : to answer a 'question'. Cube placement with this does not advance the turn.
            - possible clues : to list out possible clues
            - infer cube placement : to have a placement for a cube
            - location prob : to list monster location probabilities
            - question : to return an effective question
            """
            )
