import argparse
from cryptidsolver.constant.clues import by_booklet_entry
from cryptidsolver.player import Player
from cryptidsolver.structure import Structure
from cryptidsolver.game import Game


def parse_player(stringified: str) -> Player:
    alphabet_lookup = {"a": "alpha", "b": "beta", "g": "gamma", "d": "delta", "e": "epsilon"}
    
    color, booklet = stringified.split("_")
    (booklet_alpha, booklet_num) = (alphabet_lookup[booklet[0].lower()], int(booklet[1:]))
    
    return Player(color, by_booklet_entry(booklet_alpha, booklet_num))


def parse_structure(stringified: str) -> Structure:
    color_lookup = {"b": "blue", "g": "green", "w": "white", "b": "black"}
    shape_lookup = {"ss": "stone", "as": "shack"}

    (color, struct, loc) = (color_lookup[stringified[0].lower()], shape_lookup[stringified[2:4].lower()], stringified[5:])
    (x, y) = loc.split(",")
    (x, y) = (int(x), int(y))
    
    return Structure(color, struct, x, y)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Interactive Cryptid solver")
    parser.add_argument("--map", type=str, nargs=6, required=True, help="Map description. Columnar from top-left as '(Mappiece number)(S/N)'")
    # TODO Add an identifier for acting players
    parser.add_argument("--players", type=str, nargs="+", required=True, help="Ordered players as '(color)_(clue alphabet)(clue number)'")
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
                for clue in player.possible_clues():
                    print(clue)
                print(" ")
        elif cmd == "infer cube placement":
            raise NotImplementedError
        else:
            print("""Did not quite catch that. Use the following commands:
            - place [c/d] x y : to place Cube or Disk
            - possible clues : to list out possible clues
            - infer placement : to have a placement for a cube
            """)

