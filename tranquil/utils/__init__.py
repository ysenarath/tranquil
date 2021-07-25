from tranquil.core import *


def find_components(children):
    results = []
    for e in children:
        if isinstance(e, Component):
            results.append(e)
        elif isinstance(e, Element):
            results += find_components(e.children)
    return results
