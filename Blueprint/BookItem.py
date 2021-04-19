from __future__ import annotations

from typing import TYPE_CHECKING, Type

from typing_extensions import TypedDict

from Blueprint.BaseBlueprintItem import BaseBlueprintItem, BaseBlueprintItemDict
from Blueprint.DeconstructionPlanner import DeconstructionPlanner
from Blueprint.UpgradePlanner import UpgradePlanner

if TYPE_CHECKING:
    from Blueprint.Blueprint import BlueprintDict
    from Blueprint.BlueprintBook import BlueprintBookDict


class BookItemDict(BaseBlueprintItemDict):
    index: int


class BookItem(BaseBlueprintItem):
    dict_type: Type[TypedDict] = BookItemDict

    def __init__(self,
                 index: int,
                 blueprint: BlueprintDict = None,
                 blueprint_book: BlueprintBookDict = None,
                 upgrade_planner: UpgradePlanner = None,
                 deconstruction_planner: DeconstructionPlanner = None,
                 ):
        super().__init__(blueprint, blueprint_book, upgrade_planner, deconstruction_planner)
        self.index: int = index
