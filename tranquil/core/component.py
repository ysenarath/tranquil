import json

from lxml import etree
from lxml.builder import ElementMaker

from tranquil.core.template import Template
from tranquil.core.element import Element

__all__ = [
    'ComponentElement',
    'Component',
]

html_builder = ElementMaker()


class ComponentElement(Element):
    def __init__(self, component, **kwargs):
        super().__init__(tag=component.name, **kwargs)
        self.component = component

    @property
    def etree(self) -> etree.ElementBase:
        # noinspection PyArgumentList
        return html_builder(self.tag, **self.kwargs)

    def render(self, *args, **kwargs):
        return etree.tostring(self.etree, encoding='unicode', method='html')

    def __repr__(self):
        if 'ref' not in self.kwargs:
            raise AttributeError('Add ref to element {} to refer to the element in scripts.'.format(self.tag))
        _ref = self.kwargs['ref']
        return 'this.$refs["{ref}"]'.format(ref=_ref)


class Component:
    # noinspection PyShadowingBuiltins
    def __init__(self, id, definition):
        self.id = id
        if (not isinstance(definition, ComponentDefinition)) and isinstance(definition, dict):
            definition = ComponentDefinition(**definition)
        self.definition = definition

    def __call__(self, **kwargs):
        return ComponentElement(self, **kwargs)

    @property
    def name(self):
        return self.id

    def to_json(self):
        return self.definition.to_json()


class ComponentDefinition:
    def __init__(self, data=None, props=None, methods=None, mounted='', template='', computed=None):
        if computed is None:
            computed = []
        if data is None:
            data = {}
        if props is None:
            props = []
        if methods is None:
            methods = []
        self.props = props
        self.data = data
        self.methods = methods
        self.mounted = mounted
        self.template = template
        self.computed = computed

    def to_json(self):
        methods = [
            '__update__(url, payload, then_fn=null) {axios.post(url, {data:payload}).then(response => '
            '{let data = {...this.$data, ...response.data,}; '
            'for (const property in data) {this.$data[property] = data[property];}'
            'if (then_fn !== null) then_fn();});}',
        ]
        methods += self.methods
        if isinstance(self.template, Template):
            template = self.template.render()
        else:
            template = self.template
        return '{{props: ["{props}"], data(){{return {data}}},methods:{{{methods}}},mounted(){{{mounted}}}' \
               ',computed(){{{computed}}}' \
               ',template:`{template}`}}' \
            .format(props='","'.join(self.props),
                    data=json.dumps(self.data),
                    template=template,
                    mounted=self.mounted,
                    computed=','.join(self.computed),
                    methods=','.join(methods))
