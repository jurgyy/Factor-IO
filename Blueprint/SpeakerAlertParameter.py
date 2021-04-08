from typing import Type

from typing_extensions import TypedDict

from Blueprint.FactorioBlueprintObject import FactorioBlueprintObject


class SpeakerAlertParameterDict(TypedDict):
    pass


class SpeakerAlertParameter(FactorioBlueprintObject):
    dict_type: Type[TypedDict] = SpeakerAlertParameterDict

    def __init__(self, *args, **kwargs):
        pass
