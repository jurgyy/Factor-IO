from __future__ import annotations

from typing import TYPE_CHECKING, Type, Union

from typing_extensions import TypedDict

# Type checking import to prevent import errors
if TYPE_CHECKING:
    from Blueprint.BlueprintBook import BlueprintBookDict, BlueprintBook
    from Blueprint.DeconstructionPlanner import DeconstructionPlannerDict
    from Blueprint.Blueprint import BlueprintDict, Blueprint
    from Blueprint.UpgradePlanner import UpgradePlannerDict

from cachedProperty import cached_property


class BaseBlueprintItemDict(TypedDict):
    type: Type
    item: Union[BlueprintBookDict, BlueprintDict, UpgradePlannerDict, DeconstructionPlannerDict]


class BaseBlueprintItem:
    def __init__(self,
                 blueprint: BlueprintDict = None,
                 blueprint_book: BlueprintBookDict = None,
                 *args, **kwargs
                 ):
        # Delayed import to prevent import errors
        global BlueprintBookDict, BlueprintBook, BlueprintDict, Blueprint
        from Blueprint.BlueprintBook import BlueprintBookDict, BlueprintBook
        from Blueprint.Blueprint import BlueprintDict, Blueprint

        if blueprint is not None and blueprint_book is not None:
            print(blueprint_book, blueprint)
            raise Exception("either blueprint xor blueprintBook must be None")

        self.type: Type = next(
            (t for e, t in [(blueprint, Blueprint), (blueprint_book, BlueprintBook)] if e is not None), None)
        self.item: Union[BlueprintBookDict, BlueprintDict, None] = None

        if blueprint_book is not None:
            self.item = BlueprintBook(**blueprint_book)
        elif blueprint is not None:
            self.item = Blueprint(**blueprint)

    def __iter__(self):
        if self.type is Blueprint:
            yield self.item
            return
        elif self.type is BlueprintBook:
            for bp in self.item:
                yield bp

    def __repr__(self):
        return f"{self.type.__name__} of length {len(self)}"

    @cached_property
    def _calc_length(self):
        count = 0
        for _ in self:
            count += 1
        return count

    def __len__(self):
        return self._calc_length

    def iterEntities(self):
        if self.type is BlueprintBook:
            for bp in self.item:
                for e in bp.entities:
                    yield e
        if self.type is Blueprint:
            for e in self.item.entities:
                yield e