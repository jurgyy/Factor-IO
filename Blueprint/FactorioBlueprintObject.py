import abc
from typing import Type, Iterable

from typing_extensions import TypedDict


class FactorioBlueprintObject(abc.ABC):
    @property
    @classmethod
    @abc.abstractmethod
    def dict_type(cls) -> Type[TypedDict]:
        raise NotImplementedError()

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
                return to_dict(vars(obj))
            elif hasattr(obj, '__slots__'):
                return to_dict(dict((name, getattr(obj, name)) for name in getattr(obj, '__slots__')))
            return obj

        d = to_dict(self, first=True)
        for k in list(d.keys()):
            if k not in type(self).dict_type.__required_keys__ \
                    and k not in type(self).dict_type.__optional_keys__:
                del d[k]

        return type(self).dict_type(d)
