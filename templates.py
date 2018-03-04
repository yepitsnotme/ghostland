from aiohttp import web
import os
import mimetypes
import logging

class Template:
    def __init__(self, filename, text):
        self.filename = filename
        self.text = text

    def __str__(self):
        return self.text

    def format(self, *args, **kwargs):
        return self.text.format(*args, **kwargs)

    def response(self, *args, **kwargs):
        content_type = mimetypes.guess_type(self.filename)
        if content_type:
            content_type = content_type[0]
        else:
            content_type = 'application/octet-stream'

        return web.Response(
            body=self.format(*args, **kwargs),
            content_type=content_type)

class MultiTemplate:
    def __init__(self, app):
        self.templates = {}
        self.app = app
        for name in self.template_names:
            ext = name.split('.')[1]
            self.templates[ext] = self.app.templates[name]

    def render(self, name):
        return self.templates[name].format(**self.d)

    def response(self, name):
        return self.templates[name].response(**self.d)

def setup_templates(app):
    app.templates = {}
    for fn in filter(lambda c: c[0] is not '.', os.listdir('./template/')):
        logging.info('Loading template {} to cache'.format(fn))
        with open('template/{}'.format(fn), 'r') as f:
            text = f.read()
            app.templates[fn] = Template(fn, text)
