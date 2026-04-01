from collections.abc import Mapping
from urllib.parse import urlsplit, unquote

from flask import url_for
from flask_frozen import Freezer
from flask_app import app


def _patched_generate_all_urls(self):
    """Patched to pass full FREEZER_BASE_URL to test_request_context.

    Fixes compatibility with Flask 3.x / Werkzeug 3.x where passing only
    the path portion to test_request_context(base_url=...) fails.
    """
    script_name = self._script_name()
    url_generators = list(self.url_generators)
    url_generators += [self.url_for_logger.iter_calls]
    base_url = self.app.config.get('FREEZER_BASE_URL') or None

    with self.app.test_request_context(base_url=base_url):
        for generator in url_generators:
            for generated in generator():
                if isinstance(generated, str):
                    url = generated
                    endpoint = None
                    last_modified = None
                else:
                    if isinstance(generated, Mapping):
                        values = generated
                        endpoint = generator.__name__
                        last_modified = None
                    else:
                        if len(generated) == 2:
                            endpoint, values = generated
                            last_modified = None
                        else:
                            endpoint, values, last_modified = generated
                    url = url_for(endpoint, **values)
                    if script_name:
                        assert url.startswith(script_name), (
                            f'url_for returned URL {url} not starting with '
                            f'script_name {script_name!r}'
                        )
                        url = url[len(script_name):]
                url = unquote(url)
                parsed_url = urlsplit(url)
                if parsed_url.scheme or parsed_url.netloc:
                    raise ValueError(f'External URLs not supported: {url}')
                yield url, endpoint, last_modified


Freezer._generate_all_urls = _patched_generate_all_urls

freezer = Freezer(app)
app.config.from_pyfile('settings.py')

if __name__ == '__main__':
    freezer.freeze()
