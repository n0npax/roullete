import requests
import argparse
import sys

from flask import Flask
from flask_cors import CORS


app_name = sys.argv[0]
parser = argparse.ArgumentParser(description=f'app: {app_name}')
parser.add_argument("--port", action="store", type=int, default="80")

def getForwardHeaders(request):
    headers = {}
    incoming_headers = [ 'x-request-id',
                         'x-b3-traceid',
                         'x-b3-spanid',
                         'x-b3-parentspanid',
                         'x-b3-sampled',
                         'x-b3-flags',
                         'x-ot-span-context'
    ]

    for ihdr in incoming_headers:
        val = request.headers.get(ihdr)
        if val is not None:
            headers[ihdr] = val
            print("incoming: "+ihdr+":"+val)
    return headers

app = Flask(__name__)
CORS(app)

