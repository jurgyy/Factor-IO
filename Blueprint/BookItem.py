from __future__ import annotations

from typing import TYPE_CHECKING

from Blueprint.BaseBlueprintItem import BaseBlueprintItem, BaseBlueprintItemDict
from Blueprint.DeconstructionPlanner import DeconstructionPlanner
from Blueprint.UpgradePlanner import UpgradePlanner

if TYPE_CHECKING:
    from Blueprint.Blueprint import Blueprint, BlueprintDict
    from Blueprint.BlueprintBook import BlueprintBook, BlueprintBookDict


class BookItemDict(BaseBlueprintItemDict):
    index: int


class BookItem(BaseBlueprintItem):
    def __init__(self,
                 index: int,
                 blueprint: BlueprintDict = None,
                 blueprint_book: BlueprintBookDict = None,
                 deconstruction_planner: DeconstructionPlanner = None,
                 upgrade_planner: UpgradePlanner = None
                 ):
        super().__init__(blueprint, blueprint_book)
        # self.blueprint: Blueprint = blueprint if blueprint is None else Blueprint(**blueprint)
        # self.blueprint_book: BlueprintBook = blueprint_book if blueprint_book is None else BlueprintBook(**blueprint_book)
        # self.deconstruction_planner: DeconstructionPlanner = deconstruction_planner
        self.index: int = index
