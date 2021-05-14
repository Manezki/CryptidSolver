import argparse
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Interactive Cryptid solver")
    parser.add_argument("--map", type=str, nargs=6, required=True, help="Map description. Columnar from top-left as '(Mappiece number)(S/N)'")
    parser.add_argument("--players", type=str, nargs="+", required=True, help="Ordered players as '[@](color)_(clue alphabet)(clue number)' with @ for acting player")
    parser.add_argument("--structures", type=str, nargs="+", required=True, help="Structures as '(color)_([SS/AS])_(x),(y)'")
    args = parser.parse_args()

    players = [parse_player(player) for player in args.players]
    structures = [parse_structure(structure) for structure in args.structures]

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
                    for clue in infer.possible_clues_from_placements(map=game.map, player_cubes=player.cubes, player_disks=player.disks):
                        print(clue)

                print("")

        elif cmd == "infer cube placement":
            
            player = game.current_player()
            before_placement = infer.possible_clues_from_placements(game.map, player.cubes, player.disks)

            placement_alternatives = {}

            for tile in game.map:
                if game.accepts_cube(tile.x, tile.y):

                    # Does not account for impossible clues - that is cannot produce clue-combination
                    # that singles out a tile.

                    clues_after_placement = infer.possible_clues_from_placements(game.map, player.cubes + [(tile.x, tile.y)], player.disks)

                    placement_reduces_clues = len(before_placement.difference(clues_after_placement))
                    placement_alternatives[tile] = placement_reduces_clues

            minimum_reveal = sorted(placement_alternatives.items(), key=lambda x: x[1])[0]

            print("Place cube on x:{} y:{} to reduce {} clues".format(minimum_reveal[0].x, minimum_reveal[0].y, minimum_reveal[1]))

        else:
            print("""Did not quite catch that. Use the following commands:
            - place [c/d] x y : to place Cube or Disk
            - possible clues : to list out possible clues
            - infer placement : to have a placement for a cube
            """)

