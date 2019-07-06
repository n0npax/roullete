#!/usr/bin/env python3
import requests
import json
import random
from base import app, parser, getForwardHeaders
from flask import jsonify, request
from pymongo import MongoClient



@app.route("/api/v1/random/field",methods=['POST'])
@app.route("/api/v1/bet/",methods=['POST'])
def bet():
    payload = request.json
    amount = payload.get("amount",10)
    user = payload.get("user", "anonymous")
    field = payload.get("field", random.randint(1,36))
    spin = payload.get("spin", True)
    
    if spin:
        tracking_headers = getForwardHeaders(request)

        pass
        #call spin #TODO
    coll = bets[user]
    coll.save({"user": user, "amount": amount, "field": field})
    cursor = coll.find({})
    for document in cursor:
          print(document)
    return jsonify(spin)

if __name__ == "__main__":
    parser.add_argument("--mongo-endpoint", action="store", required=True, dest="mongo_endpoint")

    args = parser.parse_args()
    client = MongoClient(args.mongo_endpoint,
        username='bets',
        password='bets',
        authSource='bets')
    bets = client.bets
    app.run(port=args.port, host="0.0.0.0")