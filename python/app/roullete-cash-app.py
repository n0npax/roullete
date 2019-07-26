#!/usr/bin/env python3
import requests
import json
import redis
import redis_opentracing
from base import app, parser, getForwardHeaders
from flask import jsonify, request
from json import dumps
from collections import defaultdict


@app.route("/api/v1/cash/", methods=["GET"])
@app.route("/api/v1/cash", methods=["GET"])
def cash_app_get():
    redis_cash = rdb.get("cash")
    cash = json.loads(redis_cash)

    return jsonify(dumps(cash))


if __name__ == "__main__":
    parser.add_argument(
        "--redis-endpoint", action="store", required=True, dest="redis_endpoint"
    )

    args = parser.parse_args()

    rdb = redis.Redis(args.redis_endpoint, port=6379, db=0, password="bets")
    redis_opentracing.trace_client(rdb)

    app.run(port=args.port, host="0.0.0.0")
