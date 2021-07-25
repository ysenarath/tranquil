from types import SimpleNamespace

import flask
from flask import Flask, render_template, g
from werkzeug.local import LocalProxy

from tranquil import config as gc
from tranquil.core import *
from tranquil.utils import find_components

STATIC_PATH = gc.config['DEFAULT']['static_path']
TEMPLATES_PATH = gc.config['DEFAULT']['templates_path']
TITLE = gc.config['DEFAULT'].get('title', 'Tranquil')

__all__ = [
    'Tranquil',
    'Component',
    'callback',
    'state',
    'ref',
]


def _get_state():
    if 'state' not in g:
        g.state = State()
    return g.state


state = LocalProxy(_get_state)


def _get_callbacks():
    if 'callbacks' not in g:
        g.callbacks = []
    return g.callbacks


callbacks = LocalProxy(_get_callbacks)


# noinspection PyShadowingBuiltins
def callback(fn, input, output):
    c = dict(fn=fn.__name__, input=input, output=output)
    callbacks.append(c)
    return c


class Tranquil:
    def __init__(self, config=None):
        """Initialize Application

        :param config: other custom config.
        """
        if config is None:
            config = {}
        self.config = config
        self.server = self._create_app()
        self.routes = {}
        self.version = '1'

    # noinspection PyMethodMayBeStatic
    def _create_app(self):
        """Create app.

        :return: return app.
        """
        server = Flask(__name__, static_folder=STATIC_PATH, template_folder=TEMPLATES_PATH)
        server.config['templates'] = {}
        for k, v in self.config.items():
            if (k in server.config) and (server.config[k] is not None):
                server.config[k].update(v)
            else:
                server.config[k] = v
        if 'title' not in server.config:
            server.config['title'] = TITLE
        return server

    def app_context(self):
        """Gets and returns app context from Flask app.

        :return: return app context.
        """
        return self.server.app_context()

    def route(self, rule, **options):
        def decorator(func):
            def decorated_func(*args, **kwargs):
                children = func(*args, **kwargs)
                if isinstance(children, dict) and 'template' in children:
                    children = children['template']
                if isinstance(children, Template):
                    children = [children]
                return render_template('index.html', children=children, state=state, callbacks=callbacks,
                                       components=find_components(children))

            decorated_func.__name__ = func.__name__
            self.server.route(rule, **options)(decorated_func)
            return func

        return decorator

    def api_route(self, rule, **options):
        rule = f'/api/v{self.api.version}/{rule}'

        def decorator(func):
            def decorated_func(*args, **kwargs):
                result = func(*args, **kwargs)
                return flask.jsonify(result)

            decorated_func.__name__ = func.__name__
            self.server.route(rule, **options)(decorated_func)
            return func

        return decorator

    @property
    def api(self):
        return SimpleNamespace(route=self.api_route, version='1')
