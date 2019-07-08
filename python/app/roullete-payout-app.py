#!/usr/bin/env python3
import requests
import json
import random
import redis
import redis_opentracing
from base import app, parser, getForwardHeaders
from flask import jsonify, request
from pymongo import MongoClient
from json import dumps



@app.route("/api/v1/payout/",methods=['POST'])
def payout():
    payload = request.json
    app.logger.info(payout, "winning field")

    field = payload["field"]
    colour = payload["colour"]

    spin_id = int(rdb.get("id"))-1
    coll = bets[str(spin_id)]

    cursor = coll.find({})
    saved_bets = []
    for document in cursor:
        d = dict(document)
        del d['_id']
        saved_bets.append(d)
    print(saved_bets)
    print(colour, field)
    return jsonify(dumps(saved_bets))


if __name__ == "__main__":
    parser.add_argument("--mongo-endpoint", action="store", required=True, dest="mongo_endpoint")
    parser.add_argument("--redis-endpoint", action="store", required=True, dest="redis_endpoint")

    args = parser.parse_args()
    client = MongoClient(args.mongo_endpoint,
        username='bets',
        password='bets',
        authSource='bets')
    bets = client.bets

    rdb = redis.Redis(args.redis_endpoint, port=6379, db=0, password='bets')
    redis_opentracing.trace_client(rdb)

    app.run(port=args.port, host="0.0.0.0")