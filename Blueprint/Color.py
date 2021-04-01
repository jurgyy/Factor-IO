from typing_extensions import TypedDict


class ColorDict(TypedDict):
    r: float
    g: float
    b: float
    a: float


class Color:
    def __init__(self, r: float, g: float, b: float, a: float):
        self.r: float = r
        self.g: float = g
        self.b: float = b
        self.a: float = a

    def __repr__(self):
        return f"RGBA({self.r}, {self.g}, {self.b}, {self.a})"
