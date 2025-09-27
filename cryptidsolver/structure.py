from cryptidsolver.constant.limits import _MAP_MAX_X, _MAP_MAX_Y


class Structure:
    """
    Container for the structure related data.
    """

    __slots__ = ("color", "shape", "x", "y")

    def __init__(self, color: str, shape: str, x: int, y: int) -> None:
        if x < 1 or y < 1:
            raise ValueError("Coordinates have to be strictly positive")

        if x > _MAP_MAX_X:
            raise ValueError(
                f"X coordinate cannot be higher than {_MAP_MAX_X} (map-limit)"
            )

        if y > _MAP_MAX_Y:
            raise ValueError(
                f"Y coordinate cannot be higher than {_MAP_MAX_Y} (map-limit)"
            )

        if color.lower() not in ["blue", "green", "white", "black"]:
            raise ValueError(
                "Unrecognized color. Accepted ones are: Blue, Green, White, Black"
            )

        self.color = color.lower()
        self.shape = shape.lower()
        self.x = x
        self.y = y

    def is_blue(self) -> bool:
        return self.color.lower() == "blue"

    def is_green(self) -> bool:
        return self.color.lower() == "green"

    def is_white(self) -> bool:
        return self.color.lower() == "white"

    def is_black(self) -> bool:
        return self.color.lower() == "black"

    def is_shack(self) -> bool:
        return self.shape.lower() == "shack"

    def is_stone(self) -> bool:
        return self.shape.lower() == "stone"

    def __repr__(self) -> str:
        return f"{self.color.capitalize()} {self.shape.capitalize()}"
