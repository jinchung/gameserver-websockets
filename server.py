import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import uuid

import gameshandler 

clients = {}

def sendMessage(cid, msg):
    clients[cid].write_message(msg)

class GameServerHandler(tornado.websocket.WebSocketHandler):

    def open(self):
        self.id = uuid.uuid1()
        clients[self.id] = self
        print "WebSocket opened!"

    def on_message(self, message):
        print "Received a message %s from %d" % (message, self.id)
        gameshandler.handleIncomingMsg(message, self.id)

    def on_close(self):
        del clients[self.id]
        print "WebSocket closed."
    

application = tornado.web.Application([
    (r"/gameserver", GameServerHandler),
])

if __name__ == "__main__":
    port = 8888
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(port)
    print 'server is listening on port 0.0.0.0:%d' % (port,)
    tornado.ioloop.IOLoop.instance().start()
