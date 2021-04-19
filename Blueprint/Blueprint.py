from __future__ import annotations

from Blueprint.FactorioBlueprintObject import FactorioBlueprintObject
from cachedProperty import cached_property
from typing import List, Tuple, Type

from typing_extensions import TypedDict

from Blueprint.Color import Color, ColorDict
from Blueprint.Entity import Entity, EntityDict, CurvedRailEntity
from Blueprint.Icon import Icon, IconDict
from Blueprint.Position import Position, PositionDict
from Blueprint.Schedule import Schedule, ScheduleDict
from Blueprint.Tile import Tile, TileDict


BlueprintDict = TypedDict("BlueprintDict", {
    "entities": List[EntityDict],
    "item": str,
    "version": int,
    "label": str,
    "icons": List[IconDict],
    "label_color": ColorDict,
    "tiles": List[TileDict],
    "schedules": List[ScheduleDict],
    "description": str,
    "snap-to-grid": PositionDict,
    "absolute-snapping": bool,
})


class Blueprint(FactorioBlueprintObject):
    dict_type: Type[TypedDict] = BlueprintDict
    field_translation_map = {
        "snap_to_grid": "snap-to-grid",
        "absolute_snapping": "absolute-snapping",
    }

    def __init__(self,
                 entities: List[EntityDict] = (),
                 item: str = None,
                 version: int = None,
                 label: str = None,
                 icons: List[IconDict] = (),
                 label_color: ColorDict = None,
                 tiles: List[TileDict] = (),
                 schedules: List[ScheduleDict] = (),
                 description: str = None,
                 *args, **kwargs
                 ):
        self.entities: List[Entity] = [Blueprint._create_entity(e) for e in entities]
        self.item: str = item
        self.label: str = label
        self.tiles: List[Tile] = [Tile(**t) for t in tiles]
        self.icons: List[Icon] = [Icon(**i) for i in icons]
        self.schedules: List[Schedule] = [Schedule(**s) for s in schedules]
        self.version: int = version
        self.label_color: Color = None if label_color is None else Color(**label_color)
        self.description: str = description

        self.snap_to_grid: Position
        if "snap-to-grid" in kwargs:
            self.snap_to_grid = Position(**kwargs["snap-to-grid"])
            del kwargs["snap-to-grid"]

        self.absolute_snapping: bool
        if "absolute-snapping" in kwargs:
            self.absolute_snapping = kwargs["absolute-snapping"]
            del kwargs["absolute-snapping"]

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

    def get_dimensions(self) -> Tuple[int, int]:
        bb = self.bounding_box
        x = bb[1].x - bb[0].x
        y = bb[1].y - bb[0].y
        return int(x), int(y)

    @staticmethod
    def _create_entity(entity_dict: EntityDict):
        if entity_dict["name"] == "curved-rail":
            return CurvedRailEntity(**entity_dict)
        return Entity(**entity_dict)
