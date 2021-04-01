from __future__ import annotations

from typing import Type, Union

from typing_extensions import TypedDict

from Blueprint.BaseBlueprintItem import BaseBlueprintItemDict, BaseBlueprintItem
from Blueprint.Blueprint import Blueprint, BlueprintDict
from Blueprint.BlueprintBook import BlueprintBook, BlueprintBookDict
from Blueprint.DeconstructionPlanner import DeconstructionPlannerDict
from Blueprint.UpgradePlanner import UpgradePlannerDict
from cachedProperty import cached_property


class BlueprintWrapperDict(BaseBlueprintItemDict):
    pass


class BlueprintWrapper(BaseBlueprintItem):
    def __init__(self,
                 blueprint: BlueprintDict = None,
                 blueprint_book: BlueprintBookDict = None,
                 *args, **kwargs
                 ):
        super().__init__(blueprint, blueprint_book)