from typing import Type

from typing_extensions import TypedDict

from Blueprint.FactorioBlueprintObject import FactorioBlueprintObject


class SignalIDDict(TypedDict):
    name: str
    type: str


class SignalID(FactorioBlueprintObject):
    dict_type: Type[TypedDict] = SignalIDDict

    def __init__(self, name: str, type: str):
        self.name: str = name
        self.type: str = type
