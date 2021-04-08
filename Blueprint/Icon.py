from typing import Type

from typing_extensions import TypedDict

from Blueprint.FactorioBlueprintObject import FactorioBlueprintObject
from Blueprint.SignalID import SignalID, SignalIDDict


class IconDict(TypedDict):
    index: int
    signal: SignalIDDict


class Icon(FactorioBlueprintObject):
    dict_type: Type[TypedDict] = IconDict

    def __init__(self, index: int, signal: SignalIDDict):
        self.index: int = index
        self.signal: SignalID = None if signal is None else SignalID(**signal)
