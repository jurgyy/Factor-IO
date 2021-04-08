from typing import Type

from typing_extensions import TypedDict

from Blueprint.FactorioBlueprintObject import FactorioBlueprintObject


class ConnectionDataDict(TypedDict):
    pass


class ConnectionData(FactorioBlueprintObject):
    dict_type: Type[TypedDict] = ConnectionDataDict

    def __init__(self, *args, **kwargs):
        pass
