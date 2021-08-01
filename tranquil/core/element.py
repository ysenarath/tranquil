from abc import ABC

from jinja2 import Environment, BaseLoader
from lxml import etree
from lxml.html.builder import E

from tranquil.core import state
from tranquil.core.template import Template

__all__ = [
    'ElementBase',
    'Element',
]


class ElementBase(Template, ABC):
    @property
    def etree(self):
        raise NotImplementedError


class Element(ElementBase):
    def __init__(self, tag, *children, **kwargs):
        self.tag = tag
        self.children = children
        self.kwargs = kwargs

    def render(self):
        return etree.tostring(self.etree, encoding='unicode', method='html')

    @property
    def etree(self):
        children = []
        for child in self.children:
            if isinstance(child, ElementBase):
                children.append(child.etree)
            else:
                children.append(str(child))
        if 'PARSE' == self.tag.upper():
            template = Environment(loader=BaseLoader).from_string(self.children[0])
            return etree.fromstring(template.render(**self.kwargs))
        if 'CLASS' == self.tag.upper():
            return {'class': self.children[0]}
        if 'FOR' == self.tag.upper():
            return {'for': self.children[0]}
        if 'V_ON' == self.tag.upper():
            action, value = self.children[0], self.children[1]
            if state.is_var(value):
                value = '{}++'.format(value._ref)
            return {'v-on:{}'.format(action): value}
        if 'V_BIND' == self.tag.upper():
            attr, val = self.children[0], self.children[1]
            return {'v-bind:{}'.format(attr): val}
        if 'V_MODEL' == self.tag.upper():
            value = self.children[0]
            if state.is_var(value):
                value = value._ref
            attr = 'v-model'
            if 'modifier' in self.kwargs:
                attr = 'v-model.{}'.format(self.kwargs['modifier'])
            return {attr: value}
        if 'ATTR' == self.tag.upper():
            if isinstance(children[0], dict):
                return children[0]
            return dict(**self.kwargs)
        builder = getattr(E, self.tag.upper())
        if '_class' in self.kwargs:
            self.kwargs['class'] = self.kwargs['_class']
            del self.kwargs['_class']
        if ('V_OPTIONS' == self.tag.upper()) or ((self.tag.upper() == 'SELECT') and ('options' in self.kwargs)):
            if 'V_OPTIONS' == self.tag.upper():
                value = self.children[0]
            else:
                value = self.kwargs['options']
            if state.is_var(value):
                value = value._ref
            option = getattr(E, 'OPTION')
            children.append(option('{{ option.text }}', {
                'v-for': 'option in {}'.format(value),
                ':key': 'option.key',
                ':value': 'option.value'
            }))
            if 'options' in self.kwargs:
                del self.kwargs['options']
        return builder(*children, **self.kwargs)
