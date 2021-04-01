from __future__ import annotations

from Blueprint.DeconstructionPlanner import DeconstructionPlanner
from Blueprint.UpgradePlanner import UpgradePlanner

import Blueprint.BlueprintWrapper
import Blueprint.PlainBlueprint
import Blueprint.BlueprintBook


class BookItemDict(Blueprint.BlueprintWrapper.BlueprintWrapperDict):
    index: int


class BookItem(Blueprint.BlueprintWrapper.BlueprintWrapper):
    def __init__(self,
                 index: int,
                 blueprint: Blueprint.PlainBlueprint.BlueprintDict = None,
                 blueprint_book: Blueprint.BlueprintBook.BlueprintBookDict = None,
                 deconstruction_planner: DeconstructionPlanner = None,
                 upgrade_planner: UpgradePlanner = None
                 ):
        super().__init__(blueprint, blueprint_book)
        # self.blueprint: Blueprint = blueprint if blueprint is None else Blueprint(**blueprint)
        # self.blueprint_book: BlueprintBook = blueprint_book if blueprint_book is None else BlueprintBook(**blueprint_book)
        # self.deconstruction_planner: DeconstructionPlanner = deconstruction_planner
        self.index: int = index
