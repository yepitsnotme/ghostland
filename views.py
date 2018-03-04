import asyncio
import aiohttp
from aiohttp import web
from client import Client
from db import Msg, Chat 
from video import Video
import hashlib
import time
import uuid

async def index(req):
    return web.FileResponse('./static/index.html')

async def chat_list(req):
    return req.app.chats.list.response('html')

async def client_list(req):
    return req.app.clients.list.response('html')

async def get_chat(req):
    chat_id = req.match_info['chat_id']
    if not chat_id in req.app.chats:
        raise web.HTTPNotFound()
    return req.app.chats[chat_id].view.response('html')

async def chat(req):
    stream = web.StreamResponse(headers={
        'content-type': 'text/html'})

    uid = uuid.uuid4()
    client = Client(req, stream)
    req.app.clients[uid] = client

    await client.open()
    await client.send_stream()

    del req.app.clients[uid]

async def get_form(req):
    return req.app.templates['msg_new.html'].response(
            chat_id=req.match_info['chat_id'],
            name='')

async def post(req):
    chat_id = req.match_info['chat_id']

    req.body = await req.post()
    msg = Msg(req, req.app.chats[chat_id])

    if msg.valid:
        req.app.chats[chat_id].append(msg)

    return req.app.templates['msg_new.html'].response(
            chat_id = req.match_info['chat_id'],
            name = msg.name)

async def video(req):
    stream = web.StreamResponse(headers={
        'content-type': 'text/plain'})

    await stream.prepare(req)

    video = Video(req.app)

    await stream.write(video.head)

    req.app.video = frames

    for frame in video.frames():
        await stream.write(frame.encode('utf-8'))
        await asyncio.sleep(video.framerate**-1)
