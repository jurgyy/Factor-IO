from typing import Type

from typing_extensions import TypedDict

from Blueprint.FactorioBlueprintObject import FactorioBlueprintObject


class UpgradePlannerDict(TypedDict):
    pass


class UpgradePlanner(FactorioBlueprintObject):
    dict_type: Type[TypedDict] = UpgradePlannerDict

    def __init__(self, *arg, **kwargs):
        pass
