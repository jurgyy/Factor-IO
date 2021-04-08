from typing import Type

from typing_extensions import TypedDict

from Blueprint.FactorioBlueprintObject import FactorioBlueprintObject


class InventoryDict(TypedDict):
    pass


class Inventory(FactorioBlueprintObject):
    dict_type: Type[TypedDict] = InventoryDict

    def __init__(self, *args, **kwargs):
        pass
