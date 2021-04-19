from __future__ import annotations

from typing import List

from typing_extensions import TypedDict

from Blueprint.BookItem import BookItemDict, BookItem
from Blueprint.Color import Color, ColorDict


class BlueprintBookDict(TypedDict):
    item: str
    label: str
    blueprints: List[BookItemDict]
    active_index: int
    version: int
    label_color: Color


class BlueprintBook:
    def __init__(self,
                 item: str,
                 blueprints: List[BookItemDict],
                 active_index: int,
                 version: int = None,
                 label: str = None,
                 label_color: ColorDict = None,
                 *args, **kwargs
                 ):
        self.item: str = item
        self.label: str = label
        self.blueprints: List[BookItem] = [BookItem(**b) for b in blueprints]
        self.active_index: int = active_index
        self.version: int = version
        self.label_color: Color = None if label_color is None else Color(**label_color)

    def iter_blueprints(self):
        for bpi in self.blueprints:
            for bp in bpi.iter_items():
                yield bp
