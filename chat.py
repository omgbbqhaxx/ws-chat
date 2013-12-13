import tornado.ioloop
import tornado.web
import tornado.websocket


class IndexHandler(tornado.web.RequestHandler):

    def get(self):
        self.write("""
        <form action="#">
            <input type="text" />
            <button type="submit">Echo</button>
        </form>
        <br>
        <ul></ul>
        <script>
        var ws = new WebSocket("ws://chatsocial.me:8000/echo");
        ws.onmessage = function(msg) {
            var li = document.createElement("li")
            li.innerHTML = msg.data;
            document.querySelector("ul").appendChild(li);
        }

        document.querySelector("form").onsubmit = function () {
            var i = document.querySelector("input");
            ws.send(i.value);
            i.value = "";
            return false;
        }
        </script>
        """)


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
