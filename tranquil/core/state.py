from json import JSONEncoder

__all__ = [
    'State',
    'Var',
]


class State:
    def __init__(self, parent=None, name=None, value=None):
        super(State, self).__init__()
        self._name = name
        self._parent = parent
        self._value = value

    def __getattr__(self, item):
        if item.startswith('_'):
            raise AttributeError('Attribute names can\'t start with underscore (_) sign.')
        if self._value is None:
            self._value = {item: State(self, item)}
        elif item not in self._value:
            self._value[item] = State(self, item)
        elif item in self._value:
            pass
        else:
            raise AttributeError('Attribute named \'{}\' not found in \'{}\'.'.format(item, self._name))
        return self._value[item]

    def __setattr__(self, key, value):
        if key.startswith('_'):
            super().__setattr__(key, value)
        else:
            if self._value is None:
                self._value = {key: State(self, key, value)}
            elif key not in self._value:
                self._value[key] = State(self, key, value)
            elif key in self._value:
                pass
            else:
                raise AttributeError('Attribute named \'{}\' not found in \'{}\'.'.format(key, self._name))

    def __repr__(self):
        if (self._parent is None) or (self._parent._name is None):
            return str(self._name)
        else:
            return '{}.{}'.format(str(self._parent), self._name)

    def to_dict(self):
        return self._to_dict(self)

    @staticmethod
    def _to_dict(data=None):
        if isinstance(data, State):
            if data._name is None:
                return State._to_dict(data._value)
            else:
                return {data._name: State._to_dict(data._value)}
        elif isinstance(data, dict):
            return {d._name: State._to_dict(d._value) for d in data.values()}
        return data


class Var(JSONEncoder):
    def __init__(self, name):
        super(Var, self).__init__()
        self._name = name

    def __repr__(self):
        return self._name

    def default(self, o):
        return str(self)
