from tranquil.core.component import Component
from tranquil.core import html


class Chart(Component):
    def __init__(self, id, state):
        super(Chart, self).__init__(
            state=state,
            refresh=f'Plotly.react("{id}", state.data, state.layout, state.config);',
            template=html.DIV(id=id),
        )
