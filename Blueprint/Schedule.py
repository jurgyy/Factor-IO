from typing import Type

from typing_extensions import TypedDict

from Blueprint.FactorioBlueprintObject import FactorioBlueprintObject


class ScheduleDict(TypedDict):
    pass


class Schedule(FactorioBlueprintObject):
    dict_type: Type[TypedDict] = ScheduleDict

    def __init__(self, *arg, **kwargs):
        pass
