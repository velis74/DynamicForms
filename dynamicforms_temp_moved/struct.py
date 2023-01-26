class Struct(object):
    def __init__(self, data=None, **kwds):
        if not data:
            data = {}
        for name, value in data.items():
            if name:
                setattr(self, name, self._wrap(value))
        for name, value in kwds.items():
            if name:
                setattr(self, name, self._wrap(value))

    def _wrap(self, value):
        if isinstance(value, (tuple, list, set, frozenset)):
            return type(value)([self._wrap(v) for v in value])
        else:
            return Struct(value) if isinstance(value, dict) else value

    def clone(self, **kwds):
        return Struct(self.__to_dict__(), **kwds)

    def __repr__(self):
        return "Struct: " + repr(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __to_dict__(self):
        res = {}
        res.update(self.__dict__)
        for k in res.keys():
            if isinstance(res[k], Struct):
                res[k] = res[k].__to_dict__()
            elif isinstance(res[k], (tuple, list, set, frozenset)):
                res[k] = [i.__to_dict__() if isinstance(i, Struct) else i for i in res[k]]
        return res


class StructDefault(Struct):
    def __getattr__(self, item):
        return self._default_
