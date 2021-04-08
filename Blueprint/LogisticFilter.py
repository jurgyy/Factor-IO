from typing import Type

from typing_extensions import TypedDict

from Blueprint.FactorioBlueprintObject import FactorioBlueprintObject


class LogisticFilterDict(TypedDict):
    pass


class LogisticFilter(FactorioBlueprintObject):
    dict_type: Type[TypedDict] = LogisticFilterDict

    def __init__(self, *args, **kwargs):
        pass
