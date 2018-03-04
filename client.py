import asyncio
from templates import MultiTemplate

class ClientBody(MultiTemplate):
    template_names = ['client_body.html']
    def __init__(self, app, client):
        self.client = client
        super(ClientBody, self).__init__(app)

        self.d = {
            'remote': self.client.remote
        }

class Client:
    def __init__(self, req, stream):
        self.alive = True
        self.req = req
        self.app = req.app
        self.remote = req.rid
        self.chat_id = req.match_info['chat_id']
        self.stream = stream
        self.chats = self.app.chats[self.chat_id]
        self.max_chats = 50
        self.body = ClientBody(self.app, self)

    async def open(self):
        await self.stream.prepare(self.req)
        await self.stream.write(self.app.cache['head.html'])

    async def new_posts(self):
        for msg in self.chats[-self.max_chats:]:
            yield msg

        cur_len = len(self.chats)
        while self.alive:
            if len(self.chats) > cur_len:
                for msg in self.chats[cur_len:]:
                    yield msg
            cur_len = len(self.chats)

            await asyncio.sleep(0.01)

    async def send_stream(self):
        async for msg in self.new_posts():
            await self.stream.write(msg.body.render('html').encode('utf-8'))

    async def close(self):
        await self.stream.write(self.app.cache['tail.html'])
        await self.stream.write_eof()

class ClientList(MultiTemplate):
    template_names = ['client_list.html']
    delim = '\n'
    def __init__(self, app, clients):
        self.clients = clients
        super(ClientList, self).__init__(app)

        self.d = {
            'clients': self.delim.join(client.body.render('html') for client in self.clients.values())
        }

    def update(self, client):
        self.d['clients'] += self.delim + client.body.render('html')

    def remove(self, client):
        self.d['clients'] = self.d['clients'].replace(self.delim + client.body.render('html'), '')

class Clients(dict):
    def __init__(self, app):
        super(Clients, self).__init__()
        self.app = app
        self.list = ClientList(app, self)

    def __setitem__(self, name, client):
        super(Clients, self).__setitem__(name, client)
        self.list.update(client)

    def __delitem__(self, name):
        self.list.remove(self[name])
        super(Clients, self).__delitem__(name)
