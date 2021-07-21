import os
from os.path import join, exists, dirname, abspath

from reutils.config import load as config_loader

PROJECT_PATH = abspath(join(dirname(abspath(__file__)), '..'))

ENVIRONMENT = 'production'
CONFIG_PATH = join(PROJECT_PATH, 'config.prod.ini')

if not exists(CONFIG_PATH):
    ENVIRONMENT = 'development'
    CONFIG_PATH = join(PROJECT_PATH, 'config.dev.ini')

if not exists(CONFIG_PATH):
    ENVIRONMENT = 'default'
    CONFIG_PATH = join(PROJECT_PATH, 'config.ini')

config = config_loader(CONFIG_PATH)

config['DEFAULT']['project_path'] = PROJECT_PATH
config['DEFAULT']['templates_path'] = os.path.join(PROJECT_PATH, 'templates')
config['DEFAULT']['static_path'] = os.path.join(PROJECT_PATH, 'static')

ENV = ENVIRONMENT

if __name__ == '__main__':
    print('CONFIG_PATH: {}'.format(CONFIG_PATH))
