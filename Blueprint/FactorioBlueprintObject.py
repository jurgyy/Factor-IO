import abc
from typing import Type, Iterable

from typing_extensions import TypedDict


class FactorioBlueprintObject(abc.ABC):
    @property
    @abc.abstractmethod
    def dict_type(self) -> Type[TypedDict]:
        return TypedDict

    field_translation_map = {}

    def to_typed_dict(self) -> TypedDict:
        def to_dict(obj, first=False):
            """
            Recursively convert a Python object graph to sequences (lists)
            and mappings (dicts) of primitives (bool, int, float, string, ...)
            """
            if isinstance(obj, str):
                return obj
            elif isinstance(obj, dict):
                return dict((key, to_dict(val)) for key, val in obj.items()
                            if not (val is None
                                    or (isinstance(val, Iterable) and len(val) == 0)))
            elif isinstance(obj, Iterable):
                return [to_dict(val) for val in obj]
            elif not first and isinstance(obj, FactorioBlueprintObject):
                return to_dict(obj.to_typed_dict())
            elif hasattr(obj, '__dict__'):
                d = vars(obj)
                if isinstance(obj, FactorioBlueprintObject):
                    for key in list(d.keys()):
                        if key not in self.dict_type.__required_keys__ \
                                and key not in self.dict_type.__optional_keys__ \
                                and key not in self.field_translation_map:
                            del d[key]
                    for key, val in obj.field_translation_map.items():
                        if key in d:
                            d[val] = d[key]
                            del d[key]

                return to_dict(d)
            elif hasattr(obj, '__slots__'):
                return to_dict(dict((name, getattr(obj, name)) for name in getattr(obj, '__slots__')))
            return obj

        d = to_dict(self, first=True)
        return self.dict_type(d)
