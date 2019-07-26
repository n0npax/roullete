#!/usr/bin/env python3
import requests
import json
import random
import redis
from base import app, parser, getForwardHeaders
from flask import jsonify, request
from pymongo import MongoClient
from bson.json_util import dumps
import redis_opentracing


@app.route("/api/v1/random/field", methods=["POST"])
@app.route("/api/v1/bet/", methods=["POST"])
def bet():
    payload = request.json

    amount = payload.get("amount", 10)
    user = payload.get("user", "anonymous")
    field = payload.get("field", None)
    colour = payload.get("colour", None)
    tracking_headers = getForwardHeaders(request)
    if field is None:
        field = random.randint(0, 36)
    else:
        colour_api_ = args.colour_api.strip("/")
        if (
            requests.get(f"{colour_api_}/{field}", headers=tracking_headers).status_code
            != 200
        ):
            return (
                jsonify({"error": f"field {field} cannot be associated with colour"}),
                400,
            )

    if colour and colour not in ["red", "black"]:
        return (jsonify({"error": "you need to bet red or black"}), 400)

    if amount < 0:
        return (jsonify({"error": "cannot bet negative amount"}), 400)

    spin_id = rdb.get("id")
    if not spin_id:
        spin_id = "0"
    spin_id = int(spin_id)

    spin_lock = rdb.get("spinning")
    if spin_lock:
        return (
            jsonify({"error": f"spinning {spin_id} already in progress. No bets"}),
            425,
        )

    coll = bets[f"spin{spin_id}bets"]
    coll.save({"user": user, "amount": amount, "field": field, "colour": colour})
    cursor = coll.find({})
    saved_bets = []
    for document in cursor:
        d = dict(document)
        del d["_id"]
        saved_bets.append(d)
    return jsonify(dumps(saved_bets))


if __name__ == "__main__":
    parser.add_argument(
        "--mongo-endpoint", action="store", required=True, dest="mongo_endpoint"
    )
    parser.add_argument(
        "--redis-endpoint", action="store", required=True, dest="redis_endpoint"
    )
    parser.add_argument(
        "--colour-api", action="store", required=True, dest="colour_api"
    )

    args = parser.parse_args()
    client = MongoClient(
        args.mongo_endpoint, username="bets", password="bets", authSource="bets"
    )
    bets = client.bets
    rdb = redis.Redis(args.redis_endpoint, port=6379, db=0, password="bets")
    redis_opentracing.trace_client(rdb)

    # rdb = redis.Redis(args.redis_endpoint, port=31682, db=0, password='bets')
    app.run(port=args.port, host="0.0.0.0")
