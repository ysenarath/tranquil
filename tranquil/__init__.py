import flask

from tranquil import config as cfg
from tranquil.core import *
from tranquil.utils import find_components

STATIC_PATH = cfg.config['DEFAULT']['static_path']
TEMPLATES_PATH = cfg.config['DEFAULT']['templates_path']
TITLE = cfg.config['DEFAULT'].get('title', 'Tranquil')

__all__ = [
    'Tranquil',
    'Component',
    'State',
    'render_layout',
    'callback',
    'html',
]


def render_layout(layout, state=State(), callbacks=None):
    if callbacks is None:
        callbacks = []
    if not isinstance(layout, list):
        layout = [layout]
    return flask.render_template(
        'tranquil/index.html',
        children=layout,
        state=state,
        callbacks=callbacks,
        components=find_components(layout)
    )


def callback(fn, input, output):
    return {
        'fn': fn,
        'input': input,
        'output': output,
    }


class Tranquil:
    def __init__(self, app=None):
        self.tq = flask.Blueprint('tq', __name__, url_prefix='/tq', static_folder=STATIC_PATH,
                                  template_folder=TEMPLATES_PATH)
        self.app = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.register_blueprint(self.tq)
        self.app = app
