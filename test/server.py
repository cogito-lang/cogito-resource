import SimpleHTTPServer
import SocketServer

import json
import os
import sys

import ctypes
from ctypes.util import find_library
os.environ['COGITO_PATH'] = find_library('cogito')

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import handler

class Handler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_PUT(self):
        content_length = int(self.headers.getheader('content-length', 0))
        body = self.rfile.read(content_length)

        policy = json.loads(json.loads(body.split('\n')[0])['Data']['PolicyDocument'])
        print >>self.server.pipe, json.dumps(policy, indent=2)
        self.send_response(200)

if __name__ == "__main__":
    read, write = os.pipe()
    read, write = os.fdopen(read, 'r', 0), os.fdopen(write, 'w', 0)

    if os.fork() == 0:
        read.close()
        httpd = SocketServer.TCPServer(('0.0.0.0', 8080), Handler)
        httpd.pipe = write
        httpd.handle_request()
    else:
        write.close()
        request = {
            'ResponseURL': 'http://localhost:8080',
            'PhysicalResourceId': 'physical-resource-id',
            'StackId': 'stack-id',
            'RequestId': 'request-id',
            'LogicalResourceId': 'logical-resource-id',
            'ResourceProperties': {
                'Policy': 'ALLOW service:action ON aws:${accountId}:${region}:resource;',
                'Substitutions': {
                    'accountId': '012345',
                    'region': 'us-east-1'
                }
            }
        }
        handler.handle(request, None)

        lines = []
        while 1:
            line = read.readline()
            if not line:
                break
            lines.append(line)
        os.wait()

        policy = json.loads(''.join(lines))
        if (policy['Statement'][0]['Action'][0] == 'service:action' and
            policy['Statement'][0]['Resource'][0] == 'aws:012345:us-east-1:resource'):

            print 'Passed'
        else:
            print 'Failed'
            exit(1)
