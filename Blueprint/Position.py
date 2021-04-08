from typing import Type

from typing_extensions import TypedDict

from Blueprint.FactorioBlueprintObject import FactorioBlueprintObject


class PositionDict(TypedDict):
    x: float
    y: float


class Position(FactorioBlueprintObject):
    dict_type: Type[TypedDict] = PositionDict

    def __init__(self, x: float, y: float):
        self.x: float = x
        self.y: float = y

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __getitem__(self, item):
        return (self.x, self.y)[item]

    def to_typed_dict(self) -> PositionDict:
        return self.__dict__
