from __future__ import annotations

from cachedProperty import cached_property
from typing import List

from typing_extensions import TypedDict

from Blueprint.Color import Color, ColorDict
from Blueprint.Entity import Entity, EntityDict
from Blueprint.Icon import Icon, IconDict
from Blueprint.Position import Position
from Blueprint.Schedule import Schedule, ScheduleDict
from Blueprint.Tile import Tile, TileDict


class BlueprintDict(TypedDict):
    entities: List[EntityDict]
    item: str
    version: int
    label: str
    icons: List[IconDict]
    label_color: ColorDict
    tiles: List[TileDict]
    schedules: List[ScheduleDict]


class PlainBlueprint:
    def __init__(self,
                 entities: List[EntityDict] = (),
                 item: str = None,
                 version: int = None,
                 label: str = None,
                 icons: List[IconDict] = (),
                 label_color: ColorDict = None,
                 tiles: List[TileDict] = (),
                 schedules: List[ScheduleDict] = (),
                 *args, **kwargs
                 ):
        self.item: str = item
        self.label: str = label
        self.entities: List[Entity] = [Entity(**e) for e in entities]
        self.tiles: List[Tile] = [Tile(**t) for t in tiles]
        self.icons: List[Icon] = [Icon(**i) for i in icons]
        self.schedules: List[Schedule] = [Schedule(**s) for s in schedules]
        self.version: int = version
        self.label_color: Color = None if label_color is None else Color(**label_color)

    def __repr__(self):
        bb = self.boundingBox
        x = bb[1].x - bb[0].x + 1
        y = bb[1].y - bb[0].y + 1
        return f"Blueprint of shape ({x} x {y})"

    @cached_property
    def boundingBox(self):
        minX, maxX = float('inf'), float('-inf')
        minY, maxY = float('inf'), float('-inf')

        for e in self.entities:
            if e.position.x < minX:
                minX = e.position.x
            if e.position.x > maxX:
                maxX = e.position.x

            if e.position.y < minY:
                minY = e.position.y
            if e.position.y > maxY:
                maxY = e.position.y

        return (Position(minX, minY), Position(maxX, maxY))
