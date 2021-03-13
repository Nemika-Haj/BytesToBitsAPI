"""
Import base modules needed
for endpoint operation
"""

from flask import request
from flask_restful import Resource, abort

import random, datetime

from PyJS import JSON
from PyJS.modules import fs

from handlers import account_handler, reddit_handler, genius_handler

"""
Load configuration &
create base functions
"""
def fetch(fp, text=False):
    with open(fp, "r") as f:
        return JSON.parse(fs.createReadStream(fp)) if not text else f.read()

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

reddit_client = reddit_handler.RedditHandler(**fetch("data/reddit_config.json"))

start_time = datetime.datetime.now()
next_reset = datetime.datetime.now()+datetime.timedelta(seconds=64)

def update_timers():
    global start_time, next_reset
    start_time = datetime.datetime.now()
    next_reset = datetime.datetime.now()+datetime.timedelta(seconds=60)

# Rate limit handler
def clear():
    if datetime.datetime.now()>= next_reset:
        account_handler.accounts.update_many({}, {"$set": {"uses":0}})
        print("Uses were reset")
        update_timers()

"""
Create endpoints
"""
class TokenInfo(Resource):
    def get(self):
        clear()
        if not 'Authorization' in request.headers:
            return abort(401, message="Not authorized")
        
        token = request.headers['Authorization']

        account = account_handler.Account.get(token=token)

        if not account:
            return abort(401, message="Invalid authorization")

        return {
            "uses": account["uses"],
            "limit": account["limit"],
            "next_reset": (next_reset-datetime.datetime.now()).seconds
        }

class Text(Resource):
    def get(self):
        clear()
        if not 'Authorization' in request.headers:
            return abort(401, message="Not authorized")

        token = request.headers['Authorization']

        if not account_handler.Account.get(token=token):
            return abort(401, message="Invalid authorization")
        
        if check_ratelimit(token):
            return abort(429, message="You have exceeded the maximum allowed requests for your account.")

        else:
            add_use(token)
            return random.choice(fetch("storage/texts.txt", text=True).split("\n\n"))

class Word(Resource):
    def get(self):
        clear()
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
        clear()
        if not 'Authorization' in request.headers:
            return abort(401, message="Not authorized")

        token = request.headers['Authorization']

        if not account_handler.Account.get(token=token):
            return abort(401, message="Invalid authorization")
        
        if check_ratelimit(token):
            return abort(429, message="You have exceeded the maximum allowed requests for your account.")

        else:
            add_use(token)
            return random.choice(fetch("storage/madlibs.json"))

class Meme(Resource):
    def get(self):
        clear()
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
        clear()
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
        clear()
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