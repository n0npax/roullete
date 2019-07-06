#!/usr/bin/env python3
from base import app, parser
import random
from flask import jsonify


@app.route("/api/v1/random/float")
@app.route("/api/v1/random/float/")
def index():
    data = {'random': random.random()}
    return jsonify(data)


if __name__ == "__main__":
    args = parser.parse_args()
    app.run(port=args.port, host="0.0.0.0")