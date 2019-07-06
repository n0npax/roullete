#!/usr/bin/env python3
from base import app, parser
import random
from flask import jsonify


@app.route("/api/v1/colour/<int:field_num>")
@app.route("/api/v1/colour/<int:field_num>/")
def index(field_num):
    black = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
    red = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
    green = [0]
    if field_num in red:
        colour = "red"
    elif field_num in black:
        colour = "black"
    elif field_num in green:
        colour = "green"
    else:
        colour = "unknown"
    data = {'colour': colour}
    return jsonify(data)



if __name__ == "__main__":
    args = parser.parse_args()
    app.run(port=args.port, host="0.0.0.0")