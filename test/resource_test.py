import http.server
import json
import os
import socketserver
import sys

import ctypes
from ctypes.util import find_library
os.environ["COGITO_PATH"] = find_library("cogito")

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import handler

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_PUT(self):
        body = self.rfile.read(int(self.headers["content-length"]))

        self.send_response(200)
        self.end_headers()

        policy = json.loads(json.loads(body)["Data"]["PolicyDocument"])
        print(json.dumps(policy, indent=2), file=self.server.pipe)

if __name__ == "__main__":
    read, write = os.pipe()

    if os.fork() == 0:
        os.close(read)
        write = os.fdopen(write, "w")

        httpd = socketserver.TCPServer(("0.0.0.0", 8080), Handler)
        httpd.pipe = write

        httpd.handle_request()
    else:
        os.close(write)
        read = os.fdopen(read, "r")

        request = {
            "ResponseURL": "http://0.0.0.0:8080",
            "PhysicalResourceId": "physical-resource-id",
            "StackId": "stack-id",
            "RequestId": "request-id",
            "LogicalResourceId": "logical-resource-id",
            "ResourceProperties": {
                "Policy": "ALLOW service:action ON aws:${accountId}:${region}:resource;",
                "Substitutions": {
                    "accountId": "012345",
                    "region": "us-east-1"
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

        policy = json.loads("".join(lines))
        if (policy["Statement"][0]["Action"][0] == "service:action" and
            policy["Statement"][0]["Resource"][0] == "aws:012345:us-east-1:resource"):

            print("Passed")
        else:
            print("Failed")
            exit(1)
