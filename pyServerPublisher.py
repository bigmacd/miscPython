#!/usr/bin/env python
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import redis

PORT_NUMBER = 8888

redis = redis.Redis(host='192.168.1.18', port=6379)

def publishMessage(channel, message):
    """ """
    error = False
    try:
        x = redis.publish(channel, message)
    except redis.exceptions.ConnectionError:
        error = True
        print("error in publishing")
    return error

class RequestHandler(BaseHTTPRequestHandler):

    def __init__(self, request, clientAddress, server):
        """ """
        print("in init")
        super().__init__(request, clientAddress, server)

    def do_GET(self):
        """ Handler for the requests """
        print("in do get")
        query = urlparse(self.path).query
        queryItems = query.split('&')
        message = None
        channel = None
        error=None
        for item in queryItems:
            if len(item) > 0:
                name, value = item.split('=')
                if name == "message":
                    message = value
                if name == "channel":
                    channel = value

        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()

        if channel is not None and message is not None:
            print("publishing...")
            error = publishMessage(channel, message)
        else:
            print("not publishing")

        if message is not None and channel is not None and not error:
            self.wfile.write(
                bytes("<div>Successfully sent message to {}</div>".format(channel),
                      'utf-8'))
        else:
            if error:
                self.wfile.write(
                    b"<div>Failed to connect to Redis Server</div>")
            else:
                self.wfile.write(
                    b"<div>You must supply both the channel and the message to publish</div>")
        return


if __name__ == "__main__":

    try:
	#handle requests
        server = HTTPServer(('localhost', PORT_NUMBER), RequestHandler)
        print('listening on {0} '.format(PORT_NUMBER))

        server.serve_forever()

    except KeyboardInterrupt:
        server.socket.close()
		
