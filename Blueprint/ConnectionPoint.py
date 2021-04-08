from typing import Type

from typing_extensions import TypedDict

from Blueprint.FactorioBlueprintObject import FactorioBlueprintObject


class ConnectionPointDict(TypedDict):
    pass


class ConnectionPoint(FactorioBlueprintObject):
    dict_type: Type[TypedDict] = ConnectionPointDict

    def __init__(self, *args, **kwargs):
        pass
