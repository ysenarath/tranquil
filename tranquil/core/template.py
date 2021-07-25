import abc

__all__ = [
    'Template',
]


class Template(abc.ABC):
    def render(self):
        raise NotImplementedError

    def __repr__(self):
        return self.render()
