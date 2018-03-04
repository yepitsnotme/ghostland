import os
import math
import time
from templates import MultiTemplate

class MsgBody(MultiTemplate):
    template_names = ['msg.html']
    def __init__(self, app, msg):
        self.msg = msg 
        super(MsgBody, self).__init__(app)

        self.space_count = 2
        if self.msg.count >= 10:
            self.space_count = 2*math.floor(math.log(self.msg.count, 10))

        self.d = {
            'count': self.msg.count,
            'spacing': '&nbsp;'*self.space_count,
            'time': int(self.msg.time),
            'name': self.msg.name,
            'msg': self.msg.msg
        }

class Msg:
    def __init__(self, req, chat):
        self.valid = True
        self.remote = req.rid 
        self.time = time.time()

        self.name = req.body.get('name', '')[:256]
        self.msg = req.body.get('msg', '')[:2000]

        if self.msg is '':
            self.valid = False
            return 

        self.name = ''.join(filter(lambda c: c not in '<>\n', self.name))
        self.msg = ''.join(filter(lambda c: c not in '<>', self.msg))

        self.chat = chat
        self.count = len(self.chat)
        self.body = MsgBody(req.app, self)

class ChatView(MultiTemplate):
    template_names = ['chat.html']
    def __init__(self, app, chat):
        self.chat = chat
        super(ChatView, self).__init__(app)

        self.d = {
            'chat_id': self.chat.chat_id
        }

class ChatLink(MultiTemplate):
    template_names = ['chat_link.html']
    def __init__(self, app, chat):
        self.chat = chat
        super(ChatLink, self).__init__(app)

        self.d = {
            'chat_id': self.chat.chat_id
        }

class ChatListLink(ChatLink):
    template_names = ['chat_list_link.html']
        
class ChatBody(MultiTemplate):
    template_names = ['chat_body.html']
    delim = '\n'
    def __init__(self, app, chat):
        self.chat = chat
        super(ChatBody, self).__init__(app)

        self.d = {
            'msgs': self.delim.join(msg.body.render('html') for msg in self.chat)
        }

    def update(self, msg):
        self.d['msgs'] += self.delim + msg.body.render('html')

    def remove(self, msg):
        self.d['msgs'].replace(self.delim + msg.body.render('html'), '')

class Chat(list):
    def __init__(self, app, chat_id, max_posts=None):
        self.chat_id = chat_id
        self.max_posts = None
        self.view = ChatView(app, self)
        self.link = ChatLink(app, self)
        self.list_link = ChatListLink(app, self)
        self.body = ChatBody(app, self)

    def append(self, msg):
        super(Chat, self).append(msg)
        self.body.update(msg)

    def pop(self, i=None):
        msg = super(Chat, self).pop(i)
        self.body.remove(msg)

class ChatList(MultiTemplate):
    template_names = ['chat_list.html']
    delim = '\n'
    def __init__(self, app, chats):
        self.chats = chats 
        super(ChatList, self).__init__(app)

        self.d = {
            'chats': self.delim.join(chat.list_link.render('html') for chat in self.chats.values())
        }

    def update(self, chat):
        self.d['chats'] += self.delim + chat.list_link.render('html')

    def remove(self, msg):
        self.d['chats'].replace(self.delim + chat.list_link.render('html'), '')

class Chats(dict):
    def __init__(self, app):
        super(Chats, self).__init__()
        self.app = app
        self.list = ChatList(app, self)

    def __setitem__(self, chat_id, chat):
        super(Chats, self).__setitem__(chat_id, chat)
        self.list.update(chat)

    def __delitem__(self, chat_id, chat):
        super(Chats, self).__delitem__(chat_id)
        self.list.remove(chat)

def setup_chats(app):
    app.chats = Chats(app)
    for chat_id in os.listdir('./chats'):
        app.chats[chat_id] = Chat(app, chat_id)
