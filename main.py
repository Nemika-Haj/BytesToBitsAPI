from flask import Flask, render_template, redirect, url_for, request, session
from flask_restful import Api

from PyJS.modules import fs

from handlers import route_handler as routes, _security as security
from handlers.account_handler import Account as accounts

import os

from account_routes import account_routes

from api.endpoints import Text, Word, Reddit, Meme, Lyrics, Madlibs, TokenInfo

app = Flask(__name__)
api = Api(app)

"""
Load API Endpoints
"""
api.add_resource(Text, *["/text", "/text/"])
api.add_resource(Word, *["/word", "/word/"])
api.add_resource(Reddit, *["/reddit", "/reddit/"])
api.add_resource(Meme, *["/meme", "/meme/"])
api.add_resource(Lyrics, *["/lyrics", "/lyrics/"])
api.add_resource(Madlibs, *["/madlibs", "/madlibs/"])
api.add_resource(TokenInfo, *["/info", "/info/"])

app.secret_key = os.urandom(24)

app.register_blueprint(account_routes)

@app.route("/")
def index():
    examples = {}
    for example in os.listdir("./data/examples"):
        examples[example] = fs.createReadStream(f"./data/examples/{example}").chunk()
    return render_template("index.html", examples=examples, session=session)

"""
Session Management
"""

@app.route(**routes.route("logout"))
def logout():
    if "authorized" in session: del session["authorized"]
    return redirect(url_for('index'))


@app.route(**routes.route("login"))
def login():
    if "authorized" in session:
        return redirect(url_for('account_routes.index'))
        
    if request.method == "GET":
        return render_template("login.html", error=None)

    else:
        form = request.form

        if not ("email" in form and "password" in form):
            return render_template("login.html", error="Something went wrong, please try again.")
        
        if not accounts.validate(form["email"]):
            return render_template("login.html", error="Invalid Email.")

        account = accounts.get(email=form["email"])

        if not account:
            return render_template("login.html", error=f"Account not found. [Register instead?]({url_for('register')})")

        password = security.decrypt(account["password"])

        if password == form["password"]:
            session["authorized"] = True
            session["account"] = form["email"]
            return redirect(url_for('index'))
        
        else:
            return render_template("login.html", error="Invalid Login.")


@app.route(**routes.route("register"))
def register():
    if "authorized" in session:
        return redirect(url_for('account_routes.index'))

    if request.method == "GET":
        return render_template("register.html", error=None)

    else:
        form = request.form

        if not ("email" in form and "password" in form):
            return render_template("login.html", error="Something went wrong, please try again.")
        
        if not accounts.validate(form["email"]):
            return render_template("register.html", error="Invalid Email.")

        if accounts.get(email=form["email"]):
            return render_template("register.html", error=f"Account already exists. [Click to login.]({url_for('login')})")
        
        password = security.encrypt(form["password"])

        accounts.create(email=form["email"], password=password)

        return redirect(url_for('login'))

app.run(debug=True)