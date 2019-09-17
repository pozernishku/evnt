#!/usr/bin/env python3

# Digital Ocean IP 85.159.4.138:8000
# Run server in script directory ./srv.py

# BaseHTTPRequestHandler
from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO
import json
import os
from sendgrid import SendGridAPIClient
import requests

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
        zeroes = [0 for i in range(len(data))]

        # 1. Prefixes sg_ removing
        for i, dic in enumerate(data):
            for d in dic:
                if d.startswith('sg_'):
                    dic[d[3:]] = dic.pop(d)
                if d == 'country':
                    zeroes[i] = 1

        # 2. Predefined fields removing
        for dic in data:
            for k in ['useragent', 'tls', 'smtp-id', 'url_offset', 'cert_err']:
                dic.pop(k, None)

        # 3. MongoDB saving TODO...

        # 4. country and event
        if any(zeroes):
            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            sett_response = sg.client._('/user/webhooks/event/settings').get()
            if sett_response.status_code >= 200 and sett_response.status_code < 300:
                sett_dic = json.loads(sett_response.body)
                sett_dic.pop('url', None)
                for z in zeroes:
                    if z:
                        with_country = data[z]
                        country = with_country.get('country')
                        event = with_country.get('event')

                        if event not in sett_dic:
                            print('POST one original event...')
                            print(country, event)
                            print(data)
                            orig_data = json.loads(response.getvalue())
                            # TODO... Where can I find the domain for POST request?
                            response = requests.post(f'http://domain.{country}/sg_event', data=orig_data[z])
                        else:
                            print('No custom field: "country"' if not country else country, 
                                  'Predefined "event"' if event in sett_dic else event, 
                                  'No POST request sent.', sep=os.linesep)
            else:
                print('Non 200 response, sorry.')
        else:
            print('There is no custom field "country".')

        print(data)

        self.wfile.write(response.getvalue())

def run(server_class=HTTPServer, handler_class=HTTPReqHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

if __name__ == '__main__':
    print("serving at port 8000")
    run()
