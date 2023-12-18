import json


class ModelMetaclass(type):
    def __new__(mcs, name, bases, attrs):
        # print("")
        # print("")
        # print(name)
        # print(bases)
        # print(attrs)
        # print("__new__")
        # print(list(attrs.keys()))

        mappings = dict()
        for attr in attrs:
            if isinstance(attrs[attr], tuple):
                print("key=", attr, ", value = ", attrs[attr])
                mappings[attr] = attrs[attr]

        # attrs['__mappings__'] = mappings
        # attrs['__table__'] = name

        return type.__new__(mcs, name, bases, attrs)

class Model(metaclass=ModelMetaclass):

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def __str__(self):
        mappings = dict()
        for key in list(vars(self.__class__).keys()):
            if key.startswith("__"): continue
            v = getattr(self, key)
            if v:
                mappings[key] = v

        return json.dumps(mappings)

    def toDictionary(self):
        mappings = dict()
        for key in list(vars(self.__class__).keys()):
            if key.startswith("__"): continue
            v = getattr(self, key)
            if v:
                mappings[key] = v

        return mappings