#!/usr/bin/env python3
import requests
import json
import random
import redis
from base import app, parser, getForwardHeaders
from flask import jsonify, request
from pymongo import MongoClient
from json import dumps
from collections import defaultdict


@app.route("/api/v1/payout/", methods=["POST"])
def payout():
    payload = request.json
    app.logger.info(payout, "winning field")

    field = payload["field"]
    colour = payload["colour"]

    spin_id = int(rdb.get("id")) - 1

    coll = bets[f"spin{spin_id}bets"]

    cursor = coll.find({})
    saved_bets = []
    for document in cursor:
        d = dict(document)
        del d["_id"]
        saved_bets.append(d)

    payout_status = defaultdict(int)
    for bet in saved_bets:
        amount = bet["amount"]
        if bet["field"] == field:
            payout_status[bet["user"]] += amount * 35
        elif bet["colour"] == colour:
            payout_status[bet["user"]] += amount
        else:
            payout_status[bet["user"]] -= amount

    redis_cash = rdb.get("cash")
    cash = {}
    if redis_cash:
        cash = json.loads(redis_cash)

    payload = request.json
    for user, amount in payout_status.items():
        cash.setdefault(user, 0)
        cash[user] += amount
    rdb.set("cash", json.dumps(cash))

    return jsonify(dumps(payout_status))


if __name__ == "__main__":
    parser.add_argument(
        "--mongo-endpoint", action="store", required=True, dest="mongo_endpoint"
    )
    parser.add_argument(
        "--redis-endpoint", action="store", required=True, dest="redis_endpoint"
    )
    parser.add_argument("--cash-api", action="store", required=True, dest="cash_api")
    args = parser.parse_args()
    client = MongoClient(
        args.mongo_endpoint, username="bets", password="bets", authSource="bets"
    )
    bets = client.bets

    rdb = redis.Redis(args.redis_endpoint, port=6379, db=0, password="bets")

    app.run(port=args.port, host="0.0.0.0")
