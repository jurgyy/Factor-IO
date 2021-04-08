from typing import Type

from typing_extensions import TypedDict

from Blueprint.FactorioBlueprintObject import FactorioBlueprintObject


class SpeakerParameterDict(TypedDict):
    pass


class SpeakerParameter(FactorioBlueprintObject):
    dict_type: Type[TypedDict] = SpeakerParameterDict
    
    def __init__(self, *args, **kwargs):
        pass
