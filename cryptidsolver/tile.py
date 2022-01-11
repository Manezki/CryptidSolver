from cryptidsolver.structure import Structure


class _BiomeTile():

    __slots__ = (
        "biome",
        "animal"
    )

    def __init__(self, biome: str, animal: str = None) -> "_BiomeTile":
        self.biome = biome
        self.animal = animal


    def has_bear(self) -> bool:
        return self.animal == "bear"
    

    def has_cougar(self) -> bool:
        return self.animal == "cougar"

    
    def has_animal(self) -> bool:
        return self.animal is not None
    
    
    def __repr__(self) -> str:
        return f"{self.biome}"


class MapTile(_BiomeTile):

    __slots__ = (
        "x",
        "y",
        "structure"
    )

    def __init__(self, biome: str, x: int, y: int, animal: str = None, structure: Structure = None) -> "MapTile":
        assert isinstance(x, int)
        assert isinstance(y, int)
        super().__init__(biome, animal)
        self.x = x
        self.y = y
        self.structure = structure


    @classmethod
    def _from_BiomeTile(cls, biometile: _BiomeTile, x: int, y: int, structure: Structure = None):
        return cls(biometile.biome, x, y, animal = biometile.animal, structure = structure)


    def has_shack(self) -> bool:
        if self.structure is None:
            return False
        else:
            return self.structure.is_shack()
    

    def has_stone(self) -> bool:
        if self.structure is None:
            return False
        else:
            return self.structure.is_stone()

    
    def __hash__(self) -> int:
        return hash((self.x, self.y))


    def __repr__(self) -> str:

        coordinates = (self.x, self.y)

        if self.animal is not None and self.structure is not None:
            return f"{coordinates} - {self.biome} with {self.animal} and {str(self.structure)}"
        elif self.animal is not None:
            return f"{coordinates} - {self.biome} with {self.animal}"
        elif self.structure is not None:
            return f"{coordinates} - {self.biome} with {str(self.structure)}"
        else:
            return f"{coordinates} - {self.biome}"
