import asyncio
from aiohttp import web
from client import Clients
from db import setup_chats 
from routes import setup_routes
from middlewares import setup_middlewares
from templates import setup_templates
from log import AccessLogger
import logging
import os
import uvloop
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

def init():
    app = web.Application()
    app.remotes = {}
    app.cache = {}

    for fn in 'head.html', 'tail.html', 'video.html':
        logging.info('Loading {} to cache'.format(fn))
        with open('static/{}'.format(fn), 'rb') as f:
            app.cache[fn] = f.read()

    setup_templates(app)
    setup_routes(app)
    setup_middlewares(app)
    setup_chats(app)
    app.clients = Clients(app)

    async def on_shutdown(app):
        for client in app.clients.values():
            try:
                await client.close()
            except:
                pass

    app.on_shutdown.append(on_shutdown)

    return app

logging.basicConfig(level=logging.DEBUG)
access_log_format = '%t %s %r %A %bB/%Tfs'
app = init()
web.run_app(app, access_log_class=AccessLogger, access_log_format=access_log_format)
