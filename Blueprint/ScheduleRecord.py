from typing import Type

from typing_extensions import TypedDict

from Blueprint.FactorioBlueprintObject import FactorioBlueprintObject


class ScheduleRecordDict(TypedDict):
    pass


class ScheduleRecord(FactorioBlueprintObject):
    dict_type: Type[TypedDict] = ScheduleRecordDict

    def __init__(self, *args, **kwargs):
        pass
