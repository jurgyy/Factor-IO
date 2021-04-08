from typing import Type

from typing_extensions import TypedDict

from Blueprint.FactorioBlueprintObject import FactorioBlueprintObject


class WaitConditionDict(TypedDict):
    pass


class WaitCondition(FactorioBlueprintObject):
    dict_type: Type[TypedDict] = WaitConditionDict

    def __init__(self, *args, **kwargs):
        pass
