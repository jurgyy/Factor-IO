from __future__ import annotations

import numpy as np
from matplotlib.path import Path

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


class Blueprint:
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
        x, y = self.get_dimensions()
        return f"Blueprint of shape ({x} x {y})"

    @cached_property
    def bounding_box(self):
        min_x, max_x = float('inf'), float('-inf')
        min_y, max_y = float('inf'), float('-inf')

        for e in self.entities:
            e_min_x, e_min_y = np.min(e.bounding_box, axis=0)
            e_max_x, e_max_y = np.max(e.bounding_box, axis=0)

            if e_min_x < min_x:
                min_x = e_min_x
            if e_max_x > max_x:
                max_x = e_max_x

            if e_min_y < min_y:
                min_y = e_min_y
            if e_max_y > max_y:
                max_y = e_max_y

        return Position(min_x, min_y), Position(max_x, max_y)

    def get_dimensions(self):
        bb = self.bounding_box
        x = bb[1].x - bb[0].x
        y = bb[1].y - bb[0].y
        return x, y

    def get_entity_at(self, x, y):
        if not self.bounding_box[0].x <= x <= self.bounding_box[1].x or \
               self.bounding_box[0].y <= y <= self.bounding_box[1].y:
            return None

        for e in self.entities:
            bb = e.bounding_box

        return None

            if e.position.y < minY:
                minY = e.position.y
            if e.position.y > maxY:
                maxY = e.position.y

        return (Position(minX, minY), Position(maxX, maxY))
