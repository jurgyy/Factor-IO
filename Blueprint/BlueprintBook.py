from __future__ import annotations

from typing import List, Type

from typing_extensions import TypedDict

from Blueprint.BookItem import BookItemDict, BookItem
from Blueprint.Color import Color, ColorDict
from Blueprint.FactorioBlueprintObject import FactorioBlueprintObject
from Blueprint.Icon import IconDict, Icon


class BlueprintBookDict(TypedDict):
    item: str
    label: str
    blueprints: List[BookItemDict]
    active_index: int
    version: int
    label_color: Color
    description: str
    icons: List[IconDict]


class BlueprintBook(FactorioBlueprintObject):
    dict_type: Type[TypedDict] = BlueprintBookDict

    def __init__(self,
                 item: str,
                 blueprints: List[BookItemDict],
                 active_index: int,
                 version: int = None,
                 label: str = None,
                 label_color: ColorDict = None,
                 description: str = None,
                 icons: List[IconDict] = (),
                 *args, **kwargs
                 ):
        self.item: str = item
        self.label: str = label
        self.blueprints: List[BookItem] = [BookItem(**b) for b in blueprints]
        self.active_index: int = active_index
        self.version: int = version
        self.label_color: Color = None if label_color is None else Color(**label_color)
        self.description: str = description
        self.icons: List[Icon] = [Icon(**i) for i in icons]

        if len(kwargs) > 0:
            print(f"Unknown kwargs in {self.__class__.__name__}: {kwargs}")

    def iter_blueprints(self):
        for bpi in self.blueprints:
            for bp in bpi.iter_items():
                yield bp
