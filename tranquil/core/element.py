import typing

from lxml import etree
from lxml.html.builder import E
from six import string_types

from tranquil.core.state import State
from tranquil.core.template import Template

__all__ = [
    'Element',
]


class Element(Template):
    def __init__(self, tag, *children, **kwargs):
        self.tag = tag
        self.children = children
        self.kwargs = kwargs

    def render(self, *args, **kwargs):
        return etree.tostring(self.etree, encoding='unicode', method='html')

    @property
    def etree(self) -> typing.Union[etree.ElementBase, typing.Dict[str, typing.Any], str]:
        children = []
        for child in self.children:
            if isinstance(child, Template):
                children.append(child.etree)
            else:
                children.append(str(child))
        if 'V_ON' == self.tag.upper():
            action = self.children[0]
            if 'script' in self.kwargs:
                script = self.kwargs['script']
            elif len(self.children) > 0:
                script = self.children[1]
            else:
                script = ''
            return {'v-on:{}'.format(action): script}
        if 'V_BIND' == self.tag.upper():
            attr, val = self.children[0], self.children[1]
            return {'v-bind:{}'.format(attr): val}
        if 'V_DATA' == self.tag.upper():
            return '{{ ' + self.children[0] + ' }}'
        if 'V_MODEL' == self.tag.upper():
            value = self.children[0]
            attr = 'v-model'
            if 'modifier' in self.kwargs:
                attr = 'v-model.{}'.format(self.kwargs['modifier'])
            return {attr: value}
        if 'V_MODEL' == self.tag.upper():
            return {'v-model': self.children[0]}
        if 'CLASS' == self.tag.upper():
            return {'class': self.children[0]}
        if 'FOR' == self.tag.upper():
            return {'for': self.children[0]}
        if 'ATTR' == self.tag.upper():
            if isinstance(children[0], dict):
                return children[0]
            return dict(**self.kwargs)
        builder = getattr(E, self.tag.upper())
        if '_class' in self.kwargs:
            self.kwargs['class'] = self.kwargs['_class']
        return builder(*children, **self.kwargs)
