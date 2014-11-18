import tornado.ioloop
import tornado.web
import tornado.websocket


class IndexHandler(tornado.web.RequestHandler):

    def get(self):
        self.render("index.html")


class WSHandler(tornado.websocket.WebSocketHandler):

    connections = set()
    history = []

    def open(self):
        self.connections.add(self)
        for msg in self.history:
            self.write_message(msg)
        print('Total of clients: {0}'.format(len(self.connections)))

    def on_close(self):
        self.connections.remove(self)
        print('Total of clients: {0}'.format(len(self.connections)))

    def on_message(self, msg):
        self.history.append(msg)
        for c in self.connections:
            c.write_message(msg)


app = tornado.web.Application([
    (r'/', IndexHandler),
    (r'/echo', WSHandler),
])

if __name__ == '__main__':
    print('Listening on http://146.185.130.80:8000')
    app.listen(8000)
    tornado.ioloop.IOLoop.instance().start()
