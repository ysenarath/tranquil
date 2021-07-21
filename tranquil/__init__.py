from types import SimpleNamespace

import flask
from flask import Flask, render_template, url_for
from six import string_types

from tranquil import config as g, utils
from tranquil.core import *

STATIC_PATH = g.config['DEFAULT']['static_path']
TEMPLATES_PATH = g.config['DEFAULT']['templates_path']

__all__ = [
    'Tranquil',
    'JavaScriptFormatter',
]


class Tranquil:
    def __init__(self, app=None, config=None):
        """Initialize Application

        :param app: flask app to register components and routes.
        :param config: other custom config.
        """
        if config is None:
            config = {}
        self.config = config
        if app is None:
            app = self._create_app()
        self.server = app
        self.methods = []
        self.state = Variable()
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
            server.config['title'] = g.config['DEFAULT'].get('title', 'Tranquil')
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
                methods = []
                mounted = ''
                if isinstance(children, Template):
                    children = [children]
                elif isinstance(children, dict):
                    if 'mounted' in children:
                        mounted = children['mounted']
                    if 'methods' in children:
                        methods += children['methods']
                    if 'template' in children:
                        children = children['template']
                for c in self.methods:
                    method = f'{c.__name__}(data){{store.__update__("{url_for(c.__name__)}", data)}}'
                    methods.append(method)
                components = utils.find_components(children)
                return render_template(
                    'index.html',
                    children=children,
                    state=self.state,
                    methods=methods,
                    mounted=mounted,
                    components=components,
                )

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

            self.methods.append(func)
            decorated_func.__name__ = func.__name__
            self.server.route(rule, **options)(decorated_func)
            return func

        return decorator

    @property
    def api(self):
        return SimpleNamespace(route=self.api_route, version='1')
