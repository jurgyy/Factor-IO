from typing import Type

from typing_extensions import TypedDict

from Blueprint.FactorioBlueprintObject import FactorioBlueprintObject


class ItemRequestDict(TypedDict):
    pass


class ItemRequest(FactorioBlueprintObject):
    dict_type: Type[TypedDict] = ItemRequestDict

    def __init__(self, *args, **kwargs):
        pass
