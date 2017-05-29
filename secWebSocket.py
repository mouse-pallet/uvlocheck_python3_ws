#: http://stackoverflow.com/questions/5994549/how-can-i-implement-a-secure-websocket-wss-server-in-python

import os
import tornado.ioloop
import tornado.web
import tornado.websocket
import ssl

import stepMoterMethods as moter

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

class EchoWebSocket(tornado.websocket.WebSocketHandler):

    def check_origin(self, origin):
        return True

    def open(self):
        moter.setup() #setup steping moter
        print("WebSocket opened")
        self.write_message(u"I accepted ! " )

    def on_message(self, message):
	if( message >=0):
        	moter.mae(int(message))
	if( message < 0):
		moter.ushiro(int(message))
        self.write_message(u"You said: " + message)


    def on_close(self):
        print("WebSocket closed")


def setup_websocket():
    application = tornado.web.Application([
      (r"/", MainHandler),
      (r"/ws", EchoWebSocket),
    ])

    application.listen(9000, ssl_options={
        "certfile": os.path.join("./", "server.crt"),
        "keyfile": os.path.join("./", "server.key"),
    })
    tornado.ioloop.IOLoop.current().start()
