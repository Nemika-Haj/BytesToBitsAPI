from flask import request
from flask_restful import Resource, abort

import random, requests, json

from PyJS import JSON
from PyJS.modules import fs

from handlers import account_handler, reddit_handler, genius_handler

reddit_config = JSON.parse(fs.createReadStream("data/reddit_config.json"))

reddit_client = reddit_handler.RedditHandler(**reddit_config)

def fetch(fp, text=True):
    with open(f"storage/{fp}", "r") as f:
        return json.load(f) if not text else f.read()

def check_ratelimit(token):
    account = account_handler.Account.get(token=token)
    if not account["limit"]:
        return False
    
    if not "uses" in account:
        account_handler.accounts.update_one({"token": token}, {
        "$set": {
            "uses": 0
        }
    })
        return False
    if account["uses"] >= account["limit"]:
        return True
    else:
        return False

def add_use(token):
    account_handler.accounts.update_one({"token": token}, {
        "$inc": {
            "uses": 1
        }
    })

class Text(Resource):
    def get(self):
        if not 'Authorization' in request.headers:
            return abort(401, message="Not authorized")

        token = request.headers['Authorization']

        if not account_handler.Account.get(token=token):
            return abort(401, message="Invalid authorization")
        
        if check_ratelimit(token):
            return abort(429, message="You have exceeded the maximum allowed requests for your account.")

        else:
            add_use(token)
            return random.choice(fetch("texts.txt").split("\n\n"))

class Word(Resource):
    def get(self):
        if not 'Authorization' in request.headers:
            return abort(401, message="Not authorized")

        token = request.headers['Authorization']

        if not account_handler.Account.get(token=token):
            return abort(401, message="Invalid authorization")
        
        if check_ratelimit(token):
            return abort(429, message="You have exceeded the maximum allowed requests for your account.")

        else:
            add_use(token)
            words = JSON.parse(fs.createReadStream("storage/words.json"))
            return random.choice(words)

class Madlibs(Resource):
    def get(self):
        if not 'Authorization' in request.headers:
            return abort(401, message="Not authorized")

        token = request.headers['Authorization']

        if not account_handler.Account.get(token=token):
            return abort(401, message="Invalid authorization")
        
        if check_ratelimit(token):
            return abort(429, message="You have exceeded the maximum allowed requests for your account.")

        else:
            add_use(token)
            return random.choice(fetch("madlibs.json", False))

class Meme(Resource):
    def get(self):
        if not 'Authorization' in request.headers:
            return abort(401, message="Not authorized")

        token = request.headers['Authorization']

        if not account_handler.Account.get(token=token):
            return abort(401, message="Invalid authorization")
        
        if check_ratelimit(token):
            return abort(429, message="You have exceeded the maximum allowed requests for your account.")

        else:
            add_use(token)
            return reddit_client.get(limit=50)

class Reddit(Resource):
    def get(self):
        if not 'Authorization' in request.headers:
            return abort(401, message="Not authorized")

        token = request.headers['Authorization']

        if not account_handler.Account.get(token=token):
            return abort(401, message="Invalid authorization")
        
        if check_ratelimit(token):
            return abort(429, message="You have exceeded the maximum allowed requests for your account.")

        else:
            add_use(token)

            subreddit = request.args.get('subreddit')

            if not subreddit:
                return abort(400, message="'subreddit' is a required argument")
            
            limit = request.args.get('limit')

            if limit: 
                try:
                    limit = int(limit)
                    if limit > 50:
                        return abort(400, message="'limit' cannot go above 50.")
                except ValueError:
                    return abort(400, message="'limit' must be int.")
            else: limit = 1

            return reddit_client.get(subreddit=subreddit, limit=limit, one_random=False)

class Lyrics(Resource):
    def get(self):
        if not 'Authorization' in request.headers:
            return abort(401, message="Not authorized")

        token = request.headers['Authorization']

        if not account_handler.Account.get(token=token):
            return abort(401, message="Invalid authorization")
        
        if check_ratelimit(token):
            return abort(429, message="You have exceeded the maximum allowed requests for your account.")

        else:
            add_use(token)
            name = request.args.get("song")

            if not name:
                return abort(400, message="'song' is a required argument.")

            artist = request.args.get("artist")

            return genius_handler.get(name, artist)