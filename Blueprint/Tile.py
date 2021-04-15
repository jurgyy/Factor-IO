from typing import Type

from typing_extensions import TypedDict

from Blueprint.FactorioBlueprintObject import FactorioBlueprintObject
from Blueprint.Position import Position, PositionDict


class TileDict(TypedDict):
    name: str
    Position: PositionDict


class Tile(FactorioBlueprintObject):
    dict_type: Type[TypedDict] = TileDict

    def __init__(self, name: str, position: PositionDict):
        pass
        # self.name = name
        # self.Position = Position(**position)

    # def __repr__(self):
    #     return f"[Tile {self.name}@{self.Position}]"
