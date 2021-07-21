from tranquil.core import *


def find_components(elements):
    components = {}
    for e in elements:
        if isinstance(e, ComponentElement):
            components[e.component.name] = e.component
        elif isinstance(e, Element):
            components.update(find_components(e.children))
    return components
