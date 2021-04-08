from typing import Type

from typing_extensions import TypedDict

from Blueprint.FactorioBlueprintObject import FactorioBlueprintObject


class InfinityFilterDict(TypedDict):
    pass


class InfinityFilter(FactorioBlueprintObject):
    dict_type: Type[TypedDict] = InfinityFilterDict

    def __init__(self, *args, **kwargs):
        pass
