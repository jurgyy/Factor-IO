from typing_extensions import TypedDict

from Blueprint.Position import Position, PositionDict


class TileDict(TypedDict):
    name: str
    Position: PositionDict


class Tile:
    def __init__(self, name: str, position: PositionDict):
        self.name = name
        self.Position = Position(**position)

    def __repr__(self):
        return f"[Tile {self.name}@{self.Position}]"
