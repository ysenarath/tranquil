from tranquil import Component
from tranquil.html import html


def Chart(id, state):
    return Component(
        state=state,
        refresh=f'Plotly.react("{id}", state.data, state.layout, state.config);',
        template=html.DIV(id=id),
    )
