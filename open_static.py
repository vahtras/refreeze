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


port = int(5000 + 5000*random.random())
app.run(host='0.0.0.0', debug=True, port=port)
