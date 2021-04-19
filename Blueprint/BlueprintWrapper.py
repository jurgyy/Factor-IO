from __future__ import annotations

from typing import Type

from typing_extensions import TypedDict

from Blueprint.BaseBlueprintItem import BaseBlueprintItemDict, BaseBlueprintItem
from Blueprint.Blueprint import BlueprintDict
from Blueprint.BlueprintBook import BlueprintBookDict
from Blueprint.DeconstructionPlanner import DeconstructionPlannerDict
from Blueprint.UpgradePlanner import UpgradePlannerDict


class BlueprintWrapperDict(BaseBlueprintItemDict):
    pass


class BlueprintWrapper(BaseBlueprintItem):
    dict_type: Type[TypedDict] = BlueprintWrapperDict

    def __init__(self,
                 blueprint: BlueprintDict = None,
                 blueprint_book: BlueprintBookDict = None,
                 upgrade_planner: UpgradePlannerDict = None,
                 deconstruction_planner: DeconstructionPlannerDict = None,
                 *args, **kwargs
                 ):
        super().__init__(blueprint, blueprint_book, upgrade_planner, deconstruction_planner)

        if len(kwargs) > 0:
            print(f"Unknown kwargs in {self.__class__.__name__}: {kwargs}")
