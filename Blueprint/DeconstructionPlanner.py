from typing import Type

from typing_extensions import TypedDict

from Blueprint.FactorioBlueprintObject import FactorioBlueprintObject


class DeconstructionPlannerDict(TypedDict):
    pass


class DeconstructionPlanner(FactorioBlueprintObject):
    dict_type: Type[TypedDict] = DeconstructionPlannerDict

    def __init__(self, *arg, **kwargs):
        pass
