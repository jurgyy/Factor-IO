from __future__ import annotations

from typing import Type, Union

from typing_extensions import TypedDict

import Blueprint.PlainBlueprint
import Blueprint.BlueprintBook
from Blueprint.DeconstructionPlanner import DeconstructionPlannerDict
from Blueprint.UpgradePlanner import UpgradePlannerDict
from cachedProperty import cached_property


class BlueprintWrapperDict(TypedDict):
    type: Type
    item: Union[Blueprint.BlueprintBook.BlueprintBookDict, Blueprint.PlainBlueprint.BlueprintDict, UpgradePlannerDict, DeconstructionPlannerDict]


class BlueprintWrapper:
    def __init__(self,
                 blueprint: Blueprint.PlainBlueprint.BlueprintDict = None,
                 blueprint_book: Blueprint.BlueprintBook.BlueprintBookDict = None,
                 *args, **kwargs
                 ):
        if blueprint is not None and blueprint_book is not None:
            print(blueprint_book, blueprint)
            raise Exception("either blueprint xor blueprintBook must be None")

        self.type: Type = next(
            (t for e, t in [(blueprint, Blueprint), (blueprint_book, Blueprint.BlueprintBook.BlueprintBook)] if e is not None), None)
        self.item: Union[Blueprint.BlueprintBook.BlueprintBookDict, Blueprint.PlainBlueprint.BlueprintDict, None] = None

        if blueprint_book is not None:
            self.item = Blueprint.BlueprintBook.BlueprintBook(**blueprint_book)
        elif blueprint is not None:
            self.item = Blueprint.PlainBlueprint.PlainBlueprint(**blueprint)

    def __iter__(self):
        if self.type is Blueprint:
            yield self.item
            return
        elif self.type is Blueprint.BlueprintBook.BlueprintBook:
            for bp in self.item:
                yield bp

    def __repr__(self):
        return f"{self.type.__name__} of length {len(self)}"

    @cached_property
    def __len__(self):
        count = 0
        for bp in self:
            count += 1

        return count

    def iterEntities(self):
        if self.type is Blueprint.BlueprintBook.BlueprintBook:
            for bp in self.item:
                for e in bp.entities:
                    yield e
        if self.type is Blueprint:
            for e in self.item.entities:
                yield e
