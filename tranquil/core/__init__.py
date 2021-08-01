from tranquil.core.component import *
from tranquil.core.element import *
from tranquil.core.state import *
from tranquil.core.template import *

__all__ = [
    'Element',
    'Component',
    'Template',
    'State',
    'ref',
    'html',
]


class ElementType(type):
    def __getattr__(cls, item):
        return cls(item)


class ElementBuilder(object, metaclass=ElementType):
    def __init__(self, tag):
        self.tag = tag

    def __call__(self, *args, **kwargs):
        return Element(self.tag, *args, **kwargs)


html = ElementBuilder
