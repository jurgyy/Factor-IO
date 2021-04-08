from typing import Type

from typing_extensions import TypedDict

from Blueprint.FactorioBlueprintObject import FactorioBlueprintObject


class ConnectionDict(TypedDict):
    pass


class Connection(FactorioBlueprintObject):
    dict_type: Type[TypedDict] = ConnectionDict

    def __init__(self, *args, **kwargs):
        pass
