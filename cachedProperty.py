class cached_property(object):
    #  https://stackoverflow.com/a/4037979/7274764
    def __init__(self, factory):
        self._attr_name = factory.__name__
        self._factory = factory

    def __get__(self, instance, owner):
        attr = self._factory(instance)
        setattr(instance, self._attr_name, attr)

        return attr
