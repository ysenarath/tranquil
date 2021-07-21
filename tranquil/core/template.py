import abc

from lxml import etree

__all__ = [
    'Template',
]


class Template(abc.ABC):
    def render(self, *args, **kwargs):
        raise NotImplementedError

    @property
    def etree(self) -> etree.ElementBase:
        raise NotImplementedError

    def __call__(self, *args, **kwargs):
        return self.render(*args, **kwargs)
