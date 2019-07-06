#!/usr/bin/env python3
import requests
import json

from base import app, parser, getForwardHeaders
from flask import jsonify, request



@app.route("/api/v1/random/field")
@app.route("/api/v1/random/field/")
def random_field():
    tracking_headers = getForwardHeaders(request)

    num = requests.get(random_api, headers=tracking_headers).content
    num =int(json.loads(num)["random"]*37)
    
    colour_api_ = colour_api.strip("/")
    c = requests.get(f'{colour_api_}/{num}', headers=tracking_headers).content
    colour = json.loads(c)["colour"]

    return jsonify({"colour": colour, "field": num})

if __name__ == "__main__":
    parser.add_argument("--random-num-api", action="store", required=True, dest="random_api")
    parser.add_argument("--colour-api", action="store", required=True, dest="colour_api")

    args = parser.parse_args()
    colour_api, random_api = args.colour_api, args.random_api
    app.run(port=args.port, host="0.0.0.0")