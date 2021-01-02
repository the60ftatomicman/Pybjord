# Python Native
from http.server import (
    BaseHTTPRequestHandler,
    HTTPServer
)
def startServer():
    hostName = 'localhost'
    serverPort = 8080
    print("Server starting http://%s:%s" % (hostName, serverPort))
    httpd = HTTPServer((hostName, serverPort), KeyServer)
    httpd.serve_forever()
class KeyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<h1>Good job</h1>", "utf-8"))