#!/usr/bin/env python3

# Digital Ocean IP 85.159.4.138:8000

# BaseHTTPRequestHandler
from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO
import json

class HTTPReqHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'TODO GET response!')

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        response.write(body)

        # Task
        data = json.loads(response.getvalue())

        # 1. Prefixes sg_ removing
        for dic in data:
            for d in dic:
                if d.startswith('sg_'):
                    dic[d[3:]] = dic.pop(d)

        # 2. Predefined fields removing
        for dic in data:
            for k in ['useragent', 'tls', 'smtp-id', 'url_offset', 'cert_err']:
                dic.pop(k, None)

        # 3. MongoDB saving TODO...

        # 4. 

        print(data)

        self.wfile.write(response.getvalue())

def run(server_class=HTTPServer, handler_class=HTTPReqHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

if __name__ == '__main__':
    print("serving at port 8000")
    run()

# SimpleHTTPRequestHandler
# import http.server
# import socketserver

# PORT = 8000

# Handler = http.server.SimpleHTTPRequestHandler

# with socketserver.TCPServer(("", PORT), Handler) as httpd:
#     print("serving at port", PORT)
#     httpd.serve_forever()