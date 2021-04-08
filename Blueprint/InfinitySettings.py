from typing import Type

from typing_extensions import TypedDict

from Blueprint.FactorioBlueprintObject import FactorioBlueprintObject


class InfinitySettingsDict(TypedDict):
    pass


class InfinitySettings(FactorioBlueprintObject):
    dict_type: Type[TypedDict] = InfinitySettingsDict

    def __init__(self, *args, **kwargs):
        pass
