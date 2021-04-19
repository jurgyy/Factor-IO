from __future__ import annotations

from typing import Type

from typing_extensions import TypedDict

from Blueprint.BaseBlueprintItem import BaseBlueprintItemDict, BaseBlueprintItem
from Blueprint.Blueprint import BlueprintDict
from Blueprint.BlueprintBook import BlueprintBookDict


class BlueprintWrapperDict(BaseBlueprintItemDict):
    pass


class BlueprintWrapper(BaseBlueprintItem):
    dict_type: Type[TypedDict] = BlueprintWrapperDict

    def __init__(self,
                 blueprint: BlueprintDict = None,
                 blueprint_book: BlueprintBookDict = None,
                 *args, **kwargs
                 ):
        super().__init__(blueprint, blueprint_book)