from cryptidsolver.structure import Structure


class _BiomeTile:
    """
    Container for map independent hexagon information, such as animal and biome information.
    """

    __slots__ = ("animal", "biome")

    def __init__(self, biome: str, animal: str | None = None) -> None:
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
    """
    Container for map specific hexagon information, including the coordinates.
    """

    __slots__ = ("structure", "x", "y")

    def __init__(
        self,
        biome: str,
        x: int,
        y: int,
        animal: str | None = None,
        structure: Structure | None = None,
    ) -> None:
        assert isinstance(x, int)
        assert isinstance(y, int)
        super().__init__(biome, animal)
        self.x = x
        self.y = y
        self.structure = structure

    @classmethod
    def _from_BiomeTile(
        cls,
        biometile: _BiomeTile,
        x: int,
        y: int,
        structure: Structure | None = None,
    ):
        return cls(
            biometile.biome, x, y, animal=biometile.animal, structure=structure
        )

    def has_shack(self) -> bool:
        if self.structure is None:
            return False

        return self.structure.is_shack()

    def has_stone(self) -> bool:
        if self.structure is None:
            return False

        return self.structure.is_stone()

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __repr__(self) -> str:
        coordinates = (self.x, self.y)

        if self.animal is not None and self.structure is not None:
            return f"{coordinates} - {self.biome} with {self.animal} and {self.structure!s}"

        if self.animal is not None:
            return f"{coordinates} - {self.biome} with {self.animal}"

        if self.structure is not None:
            return f"{coordinates} - {self.biome} with {self.structure!s}"

        return f"{coordinates} - {self.biome}"
