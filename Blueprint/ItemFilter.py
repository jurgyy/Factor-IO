from typing import Type

from typing_extensions import TypedDict

from Blueprint.FactorioBlueprintObject import FactorioBlueprintObject


class ItemFilterDict(TypedDict):
    pass


class ItemFilter(FactorioBlueprintObject):
    dict_type: Type[TypedDict] = ItemFilterDict

    def __init__(self, *args, **kwargs):
        pass
