import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import gameshandler as gh
import uuid

class GameServerHandler(tornado.websocket.WebSocketHandler):
    clients = {}

    def open(self):
        gh.setServerHandler(self)
        self.id = uuid.uuid1()
        self.clients[self.id] = self
        print "WebSocket opened!"

    def on_message(self, message):
        print "Received a message %s from %d" % (message, self.id)
        gh.handleIncomingMsg(message, self.id)

    def on_close(self):
        del self.clients[self.id]
        print "WebSocket closed."
    
    def sendMessage(self, cid, msg):
        self.clients[cid].write_message(msg)

application = tornado.web.Application([
    (r"/gameserver", GameServerHandler),
])

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    print 'server is listening'
    tornado.ioloop.IOLoop.instance().start()
