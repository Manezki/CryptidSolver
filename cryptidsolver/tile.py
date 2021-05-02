class _BiomeTile():

    def __init__(self, biome, animal=None):
        self.biome = biome
        self.animal = animal


    def has_bear(self):
        return self.animal == "bear"
    

    def has_cougar(self):
        return self.animal == "cougar"

    
    def has_animal(self):
        return self.animal is not None
    
    
    def __repr__(self) -> str:
        return "{}".format(self.biome)


class MapTile(_BiomeTile):

    def __init__(self, biome, x, y, animal=None, structure=None):
        assert isinstance(x, int)
        assert isinstance(y, int)
        super().__init__(biome, animal)
        self.x = x
        self.y = y
        self.structure = structure


    @classmethod
    def _from_BiomeTile(cls, biometile, x, y, structure=None):
        return cls(biometile.biome, x, y, animal = biometile.animal, structure = structure)


    def has_shack(self):
        if self.structure is None:
            return False
        else:
            return self.structure.is_shack()
    

    def has_stone(self):
        if self.structure is None:
            return False
        else:
            return self.structure.is_stone()

    
    def __hash__(self):
        return hash((self.x, self.y))


    def __repr__(self):

        coordinates = (self.x, self.y)

        if self.animal is not None and self.structure is not None:
            return str("{} - {} with {} and {}".format(coordinates, self.biome, self.animal, str(self.structure)))
        elif self.animal is not None:
            return str("{} - {} with {}".format(coordinates, self.biome, self.animal))
        elif self.structure is not None:
            return str("{} - {} with {}".format(coordinates, self.biome, str(self.structure)))
        else:
            return str("{} - {}".format(coordinates, self.biome))
