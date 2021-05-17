import argparse
import copy

from cryptidsolver.constant.clues import by_booklet_entry
from cryptidsolver.player import Player
from cryptidsolver.structure import Structure
from cryptidsolver.game import Game
from cryptidsolver import infer


def parse_player(stringified: str) -> Player:
    alphabet_lookup = {"a": "alpha", "b": "beta", "g": "gamma", "d": "delta", "e": "epsilon"}

    if stringified.startswith("@"):
        acting_player = True
        stringified = stringified[1:]
    else:
        acting_player = False

    color, booklet = stringified.split("_")
    (booklet_alpha, booklet_num) = (alphabet_lookup[booklet[0].lower()], int(booklet[1:]))
    
    if acting_player:
        return Player(color, by_booklet_entry(booklet_alpha, booklet_num))
    else:
        return Player(color, clue=None)


def parse_structure(stringified: str) -> Structure:

    stringified = stringified.lower()

    if not (stringified.startswith(("green", "white", "black", "blue"))):
        raise ValueError("Structure parameter has to start by color definition")

    if stringified.startswith(("green", "white", "black")):
        color = stringified[:5]
    else:
        # Blue
        color = stringified[:4]

    shape_lookup = {"ss": "stone", "as": "shack"}

    offset = len(color)

    (struct, loc) = (shape_lookup[stringified[offset + 1: offset + 3]], stringified[offset + 4:])
    (x, y) = loc.split(",")
    (x, y) = (int(x), int(y))
    
    return Structure(color, struct, x, y)


def question_fitness(n_locations: int, n_combinations: int) -> float:
    if (n_locations == 1):
        return 0
    elif (n_combinations == 1 and n_locations != 1):
        return -9999
    elif (n_locations == 0):
        return -9999
    elif (n_combinations == 0):
        return -9999
    else:
        return (-n_locations + 1)*(n_combinations**0.5)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Interactive Cryptid solver")
    parser.add_argument("--map", type=str, nargs=6, required=True, help="Map description. Columnar from top-left as '(Mappiece number)(S/N)'")
    parser.add_argument("--players", type=str, nargs="+", required=True, help="Ordered players as '[@](color)_(clue alphabet)(clue number)' with @ for acting player")
    parser.add_argument("--structures", type=str, nargs="+", required=True, help="Structures as '(color)_([SS/AS])_(x),(y)'")
    args = parser.parse_args()

    players = [parse_player(player) for player in args.players]
    structures = [parse_structure(structure) for structure in args.structures]

    __minimal_structures = [("white", "stone"), ("white", "shack"), ("green", "stone"), ("green", "shack"), ("blue", "stone"), ("blue", "shack")]

    assert len(players) >= 3, "Game should have at least three players"
    assert all(ms in [(s.color.lower(), s.shape.lower()) for s in structures] for ms in __minimal_structures), "All the basic structures should be present"

    game = Game(args.map, players, structures)


    while(True):

        cmd = input().lower().strip()

        if cmd.startswith("place") and len(cmd.split(" ")) == 4:

            try:
                (_, mapObject, x, y) = cmd.split(" ")
                (x, y) = (int(x), (int(y)))

                if mapObject == "c":
                    action = game.place_cube(x, y)
                    print("{} placed cube on {}".format(action[0], action[1]))
                elif mapObject == "d":
                    action = game.place_disk(x, y)
                    print("{} placed disk on {}".format(action[0], action[1]))
                else:
                    raise ValueError

            except ValueError:
                pass

        elif cmd == "possible clues":
            for player in game.players:
                print("{}'s possible clues".format(player))
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

                    # Does not account for impossible clues - that is cannot produce clue-combination
                    # that singles out a tile.

                    clues_after_placement = infer.possible_clues_after_cube_placement(game.map, player, (tile.x, tile.y))

                    placement_reduces_clues = len(before_placement.difference(clues_after_placement))
                    placement_alternatives[tile] = placement_reduces_clues

            minimum_reveal = sorted(placement_alternatives.items(), key=lambda x: x[1])[0]

            print("Place cube on x:{} y:{} to reduce {} clues".format(minimum_reveal[0].x, minimum_reveal[0].y, minimum_reveal[1]))

        elif cmd == "location prob":

            possible_locations = game.possible_tiles()
            possible_locations = sorted(possible_locations.items(), key=lambda x: x[1])

            print("Location probabilities")
            print("---------")
            for location, probability in possible_locations:
                print("Tile x:{} y:{} has probability of {}".format(location.x, location.y, probability))


        elif cmd == "question":

            print()

            possible_tiles = game.possible_tiles()
            n_possible_locations = len(possible_tiles.keys())
            n_possible_combinations = sum(possible_tiles.values())

            imagined_game = copy.deepcopy(game)

            expect_current = [p for p in imagined_game.players if p != imagined_game.current_player()]

            potential_questions = {p: {
                "tile": None,
                "fitness": question_fitness(n_possible_locations, n_possible_combinations),
                "results": {
                    "locations": n_possible_locations,
                    "combinations": n_possible_combinations
                }
            } for p in expect_current}

            for player in expect_current:

                # No point asking questions from players with known clues, i.e. acting players
                if player.clue is not None:
                    continue

                for tile in imagined_game.map:

                    # imagine cube placement
                    player.cubes.append((tile.x, tile.y))

                    after_locations = imagined_game.possible_tiles()
                    n_negative_locations_after = len(after_locations.keys())
                    n_negative_combinations_after = sum(after_locations.values())

                    player.cubes.remove((tile.x, tile.y))

                    # imagine disk placement

                    player.disks.append((tile.x, tile.y))

                    after_locations = imagined_game.possible_tiles()
                    n_positive_locations_after = len(after_locations.keys())
                    n_positive_combinations_after = sum(after_locations.values())

                    player.disks.remove((tile.x, tile.y))

                    fitness = (
                            question_fitness(n_negative_locations_after, n_negative_combinations_after) +
                            question_fitness(n_positive_locations_after, n_positive_combinations_after)
                        )/2

                    if fitness >= potential_questions[player]["fitness"]:
                        results = {
                                "locations": (n_positive_locations_after, n_negative_locations_after),
                                "combinations": (n_positive_combinations_after, n_negative_combinations_after)
                            }
                        potential_questions[player] = {"tile": tile, "fitness": fitness, "results": results}

            favored_question = max(potential_questions.items(), key = lambda x: x[1]["fitness"])

            print("Question found.")
            print("Ask player: {} about x: {} y: {}".format(favored_question[0], favored_question[1]["tile"].x, favored_question[1]["tile"].y))
            print(favored_question[1]["fitness"], favored_question[1]["results"])

        else:
            print("""Did not quite catch that. Try one of the following commands:
            - place [c/d] x y : to place Cube or Disk
            - possible clues : to list out possible clues
            - infer cube placement : to have a placement for a cube
            - location prob : to list monster location probabilities
            - question : to return an effective question
            """)

