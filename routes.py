import pathlib
from views import *

PROJECT_ROOT = pathlib.Path(__file__).parent

def setup_routes(app):
    app.router.add_get('/', index)
    app.router.add_get('/list', chat_list)
    app.router.add_get('/stats', client_list)
    app.router.add_get('/chat/{chat_id}', get_chat)
    app.router.add_get('/chat/{chat_id}/post', get_form)
    app.router.add_post('/chat/{chat_id}/post', post)
    app.router.add_get('/chat/{chat_id}/stream', chat)
    app.router.add_get('/video', video)
    app.router.add_static('/static',
            path=str(PROJECT_ROOT / 'static'),
            name='static')
