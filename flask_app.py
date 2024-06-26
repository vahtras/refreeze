import os
from flask import Flask, render_template
from jinja2 import Template
import webbrowser

app = Flask(__name__, template_folder='.', static_url_path='', static_folder='..')
app.config.from_pyfile('settings.py')

BASE = '/%s' % app.config['REPO_NAME']

@app.route('/')
def home():
    with open('talk.md', 'r') as f:
        template = Template(f.read())
        markdown = template.render(base=BASE)
        markdown = markdown.replace('---', '---\nlayout: false', 1)
        js_file = 'talk.js'
        if os.path.isfile(js_file):
            with open(js_file, 'r') as f_js:
                js = f_js.read()
        else:
            js = ''
        css_file = 'talk.css'
        if os.path.isfile(css_file):
            css = Template(open(css_file).read()).render(base=BASE)
        return render_template(
            'slides.html', markdown=markdown, js=js, css=css
        )


if __name__ == '__main__':
    BASE = ''
    port = int(os.environ.get('PORT', 5000))
    webbrowser.open_new('http://localhost:{}'.format(port))
    app.run(host='0.0.0.0', port=port)
