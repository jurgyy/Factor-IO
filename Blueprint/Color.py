from typing import Type

from typing_extensions import TypedDict

from Blueprint.FactorioBlueprintObject import FactorioBlueprintObject


class ColorDict(TypedDict):
    r: float
    g: float
    b: float
    a: float


class Color(FactorioBlueprintObject):
    dict_type: Type[TypedDict] = ColorDict

    def __init__(self, r: float, g: float, b: float, a: float):
        self.r: float = r
        self.g: float = g
        self.b: float = b
        self.a: float = a

    def __repr__(self):
        return f"RGBA({self.r}, {self.g}, {self.b}, {self.a})"
