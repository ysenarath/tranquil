from flask import request

from tranquil import Tranquil, callback, ref, state
from tranquil.components import plotly
from tranquil.html import html

app = Tranquil()


@app.api.route('/data', methods=["POST"])
def data_provider():
    data = request.get_json()
    return {
        'data': [{
            'type': "treemap",
            'labels': ["Eve", "Cain", "Seth", "Enos", "Noam", "Abel", "Awan", "Enoch", "Azura"],
            'parents': ["", "Eve", "Eve", "Seth", "Seth", "Eve", "Eve", "Awan", "Eve"]
        }],
        'layout': {
            'height': 'auto',
        },
        'config': {'responsive': True},
    }


@app.route('/')
def index():
    state.set_state({
        'inDarkMode': True,
        'button_1': {
            'n_count': 0
        },
        'input_1': {
            'value': 0,
            'options': [1, 2, 3],
        },
    })
    callback(data_provider, state.button_1.n_count, state.input_1.options)
    callback(data_provider, state.input_1.value, state.input_1.options)
    return [
        html.INPUT(html.V_MODEL(state.input_1.value)),
        html.BUTTON('Click Me!', html.V_ON('click', state.button_1.n_count)),
        html.P(f'Hello World! {ref(state.input_1)}'),
        html.P(f'Number of Clicks: {ref(state.button_1.n_count)}'),
    ]


@app.route('/page_2')
def page_2():
    state.set_state({
        'inDarkMode': True,
        'chart_1': {},
        'button_1': {
            'n_count': 0
        },
        'input_1': {
            'value': 1,
            'options': [
                {'text': 'Value 1', 'key': 'K1', 'value': 0},
                {'text': 'Value 2', 'key': 'K1', 'value': 1},
            ],
        },
    })
    chart_1 = plotly.Chart('chart-1', state.chart_1)
    callback(data_provider, [state.button_1.n_count, state.input_1.value], state.chart_1)
    return [
        html.BUTTON('Click Me!', html.V_ON('click', state.button_1.n_count)),
        html.DIV(chart_1),
        html.SELECT(html.V_MODEL(state.input_1.value), html.V_OPTIONS(state.input_1.options)),
        html.P(f'{ref(state.chart_1)}'),
    ]


def create_app():
    return app.server
