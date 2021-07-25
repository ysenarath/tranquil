from tranquil.core.element import ElementBase

__all__ = [
    'Component'
]


class Component(ElementBase):
    def __init__(self, state, refresh, template):
        self.state = state
        self.template = template
        self.refresh = refresh

    @property
    def etree(self):
        return self.template.etree

    def render(self):
        return self.template.render()
