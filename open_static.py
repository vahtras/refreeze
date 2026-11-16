#!/usr/bin/env python

import flask
import random
import pathlib


root = str(pathlib.Path(__file__).parent.parent.resolve())
stem = pathlib.Path(__file__).parent.parent.stem

app = flask.Flask(
    __name__,
    static_folder=root,
    static_url_path=f'/{stem}',
    template_folder=root
)


@app.route('/')
def index():
    return flask.render_template('index.html')


port = random.randint(8001,8999)
app.run(host='0.0.0.0', debug=True, port=port)
