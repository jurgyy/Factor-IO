from typing_extensions import TypedDict

from Blueprint.SignalID import SignalID, SignalIDDict


class IconDict(TypedDict):
    index: int
    signal: SignalIDDict


class Icon:
    def __init__(self, index: int, signal: SignalIDDict):
        self.index: int = index
        self.signal: SignalID = None if signal is None else SignalID(**signal)
