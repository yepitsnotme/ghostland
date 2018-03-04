from aiohttp import web
import hashlib
import logging
import time

@web.middleware
async def handle_error(req, handler):
    try:
        res = await handler(req)
        if res.status >= 400:
            return req.app.templates['error.html'].response(status=res.status)
        else:
            return res
    except web.HTTPException as e:
        return req.app.templates['error.html'].response(status=e)

@web.middleware
async def get_id(req, handler):
    req.rid = hashlib.sha256(req.remote.encode('utf-8')).hexdigest()
    resp = await handler(req)
    return resp


def setup_middlewares(app):
    app.middlewares.append(get_id)
    app.middlewares.append(handle_error)
