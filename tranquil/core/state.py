__all__ = [
    'State',
    'ref',
]


class _object(object):
    def __init__(self, parent, name, data):
        super(_object, self).__init__()
        super(_object, self).__setattr__('_parent', parent)
        super(_object, self).__setattr__('_name', name)
        super(_object, self).__setattr__('_data', self._to_object(data))

    def __getattr__(self, item):
        if item in self._data:
            return self._data[item]
        else:
            raise AttributeError

    def __setattr__(self, key, value):
        self._data[key] = _object(self, key, value)

    def _to_object(self, data):
        if isinstance(data, dict):
            return {k: _object(self, k, v) for k, v in data.items()}
        else:
            return data

    @property
    def _val(self):
        return _object._get_value(self)

    @staticmethod
    def _get_value(obj):
        if isinstance(obj._data, dict):
            return {k: _object._get_value(v) for k, v in obj._data.items()}
        return obj._data

    def _set_value(self, value):
        super(_object, self).__setattr__('_data', self._to_object(value))

    @property
    def _ref(self):
        if self._name is not None:
            if (self._parent is not None) and (self._parent._name is not None):
                return '{}.{}'.format(self._parent._ref, self._name)
            else:
                return self._name
        return ''


class State(_object):
    def __init__(self, data=None):
        super(State, self).__init__(parent=None, name=None, data=({} if data is None else data))

    def to_dict(self):
        return super(State, self)._val

    def set_state(self, state):
        super(State, self)._set_value(state)


def ref(o):
    return '{{' + (o._ref if isinstance(o, _object) else str(o)) + '}}'


def is_var(o):
    return isinstance(o, _object)
