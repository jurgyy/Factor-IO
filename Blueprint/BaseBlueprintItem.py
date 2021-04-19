from __future__ import annotations

import abc
from typing import TYPE_CHECKING, Type, Union

from typing_extensions import TypedDict

from Blueprint.FactorioBlueprintObject import FactorioBlueprintObject

# Type checking import to prevent import errors
if TYPE_CHECKING:
    from Blueprint.BlueprintBook import BlueprintBookDict, BlueprintBook
    from Blueprint.DeconstructionPlanner import DeconstructionPlannerDict
    from Blueprint.Blueprint import BlueprintDict, Blueprint
    from Blueprint.UpgradePlanner import UpgradePlannerDict

from cachedProperty import cached_property


class BaseBlueprintItemDict(TypedDict):
    blueprint: BlueprintDict
    blueprint_book: BlueprintBookDict
    upgrade_planner: UpgradePlannerDict
    deconstruction_planner: DeconstructionPlannerDict


class BaseBlueprintItem(FactorioBlueprintObject, metaclass=abc.ABCMeta):
    def __init__(self,
                 blueprint: BlueprintDict = None,
                 blueprint_book: BlueprintBookDict = None,
                 upgrade_planner: UpgradePlannerDict = None,
                 deconstruction_planner: DeconstructionPlannerDict = None,
                 *args, **kwargs
                 ):
        # Delayed import to prevent import errors
        global BlueprintBookDict, BlueprintBook, BlueprintDict, Blueprint
        from Blueprint.BlueprintBook import BlueprintBookDict, BlueprintBook
        from Blueprint.Blueprint import BlueprintDict, Blueprint

        self.blueprint_book: BlueprintBook = None if blueprint_book is None else BlueprintBook(**blueprint_book)
        self.blueprint: Blueprint = None if blueprint is None else Blueprint(**blueprint)

    def iter_items(self):
        if self.blueprint is not None:
            if len(self.blueprint.entities) != 0:
                yield self.blueprint
        if self.blueprint_book is not None:
            for bp in self.blueprint_book.iter_blueprints():
                if len(bp.entities) == 0:
                    continue
                yield bp

    def __repr__(self):
        return f"Blueprint item of length {len(self)}"

    @cached_property
    def _calc_length(self):
        count = 0
        for _ in self.iter_items():
            count += 1
        return count

    def __len__(self):
        return self._calc_length

    def iter_entities(self):
        for bp in self.iter_items():
            for e in bp.entities:
                yield e
