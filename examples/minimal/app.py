import random

from flask import request, url_for

from tranquil import Tranquil
from tranquil.html import html
from tranquil.components import plotly as tcp
from tranquil.components import bootstrap as tcb

app = Tranquil()


@app.api.route('/scatter_data', methods=['POST'])
def scatter_data():
    data = request.get_json().get('data', {'value': 1})
    try:
        value = int(data['value'])
    except (TypeError, ValueError):
        value = 1
    return {
        'data': [
            {
                'x': [i for i in range(value)],
                'y': [random.random() for _ in range(value)],
                'type': 'scatter',
            }
        ],
    }


def heading():
    return tcb.Navbar('3Minimal', [
        dict(label='Home', url=url_for('home')),
        dict(label='Page 2', url=url_for('home')),
    ], id='heading-navbar')


@app.route('/')
def home():
    app.state.input_1.value = 100
    scatter_plot = tcp.ScatterPlot(
        id='scatter-plot-1',
        data_url=url_for('scatter_data'),
        ref='scatter-plot-1',
    )
    return dict(
        template=[
            heading(),
            html.DIV(
                html.P('# of Values'),
                html.INPUT(
                    html.V_MODEL('input_1.value', modifier='number'),
                    html.V_ON('keyup.enter', script=f'{scatter_plot}.update(input_1)')
                ),
                _class='m-3',
            ),
            html.DIV(scatter_plot),
        ],
        mounted=f'{scatter_plot}.update(store.state.input_1);',
    )


def create_app():
    return app.server
