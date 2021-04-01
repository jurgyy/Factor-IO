from typing_extensions import TypedDict


class SignalIDDict(TypedDict):
    name: str
    type: str


class SignalID:
    def __init__(self, name: str, type: str):
        self.name: str = name
        self.type: str = type
