from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return 'Hey, we have Flask in a Docker container!'
