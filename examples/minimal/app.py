from flask import Flask, jsonify

from tranquil import Tranquil, State, render_layout, callback
from tranquil import components as tcc
from tranquil import html

app = Flask(__name__)

tq = Tranquil(app)


@app.route('/update_chat_1', methods=['POST'])
def update_chat_1():
    return jsonify({
        'data': [
            {
                'x': [1, 2, 3, 4],
                'y': [16, 5, 11, 9],
                'type': 'scatter'
            }
        ]
    })


@app.route('/')
def index():
    state = State({
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
    return render_layout(
        [
            tcc.Navbar(is_fluid=False),
            html.Div(
                html.Div(
                    html.DIV(
                        html.BUTTON('Click Me!', html.V_ON('click', state.button_1.n_count), _class='btn btn-primary'),
                        _class='col col-auto'
                    ),
                    html.DIV(
                        html.SELECT(html.V_MODEL(state.input_1.value), html.V_OPTIONS(state.input_1.options),
                                    _class='form-select'),
                        _class='col'
                    ),
                    _class='row'
                ),
                html.DIV(tcc.Chart('chart-1', state.chart_1), _class='row'),
                _class='container pt-3'
            )
        ],
        callbacks=[
            callback('update_chat_1', input=[state.button_1.n_count], output=state.chart_1),
        ],
        state=state
    )
