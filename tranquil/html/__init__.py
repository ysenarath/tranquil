from tranquil.core import Element

__all__ = [
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
