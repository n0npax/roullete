#!/usr/bin/env python3
import requests
import json
import random
import redis
from base import app, parser, getForwardHeaders
from flask import jsonify, request
from pymongo import MongoClient
import redis_opentracing



@app.route("/api/v1/spin/",methods=['POST'])
def spin():
    spin_id = rdb.get("id")
    if not spin_id:
        spin_id = 0
    else:
        spin_id = int(spin_id)
    
    spin_lock = rdb.get("spinning")
    if spin_lock:
        return jsonify({"error": f"spinning {spin_id} already in progress. No bets"}), 425
    
    rdb.set("spinning", "True", ex=5)
    spin_id+=1
    rdb.set("id", str(spin_id))

    # get winner
    tracking_headers = getForwardHeaders(request)
    winning_field = requests.get(args.random_field_api, headers=tracking_headers).content
    winning_field = json.loads(winning_field)

    # notify payout
    requests.post(args.payout_api,
        headers=tracking_headers,
        json=winning_field)
    app.logger.info(winning_field, "winning field")

    return jsonify(winning_field)

if __name__ == "__main__":
    parser.add_argument("--redis-endpoint", action="store", required=True, dest="redis_endpoint")
    parser.add_argument("--random-field-api", action="store", required=True, dest="random_field_api")
    parser.add_argument("--payout-api", action="store", required=True, dest="payout_api")

    args = parser.parse_args()
    rdb = redis.Redis(args.redis_endpoint, port=6379, db=0, password='bets')
    redis_opentracing.trace_client(rdb)

    app.run(port=args.port, host="0.0.0.0")