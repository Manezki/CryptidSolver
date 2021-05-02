from gamemap import Map
import itertools

class Game():
    def __init__(self, map_descriptor, ordered_players, structures):
        self.players = ordered_players
        self.map = Map(map_descriptor, structures)

        self.possible_tiles = set(self.map)

        self.__reduce_possible_tiles_by_clues()

    
    def __reduce_possible_tiles_by_clues(self):
        for player in self.players:
            if player.clue is not None:
                for tile in self.possible_tiles.copy():

                    x, y = (tile.x, tile.y)
                    distanced_tiles = self.map.tiles_on_distance(x, y, player.clue.distance)
                    
                    for clued_distance in distanced_tiles:
                        if not player.clue.accepts_tile(clued_distance):
                            try:
                                self.possible_tiles.remove(clued_distance)
                            except KeyError:
                                # Possibly removed already
                                pass
    

    def possible_clues(self):
        clue_combinations = itertools.product(*[p.possible_clues for p in self.players])
        
        possible_combinations = set()

        for combination in clue_combinations:
            
            accepted_tiles = combination[0].accepted_tiles(self.map)
            for clue in combination[1:]:
                accepted_tiles = accepted_tiles.intersection(clue.accepted_tiles(self.map))

            if len(accepted_tiles) == 1:
                possible_combinations.add(combination)
        
        return possible_combinations