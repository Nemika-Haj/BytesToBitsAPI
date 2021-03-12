from flask import Blueprint, render_template, session, redirect, url_for, request

from handlers import route_handler as routes
from handlers.account_handler import Account

from PyJS import JSON
from PyJS.modules import fs

import string, random

account_routes = Blueprint('account_routes', __name__)

@account_routes.route(**routes.route("account"))
def index():
    if not 'authorized' in session:
        return redirect(url_for('index'))

    account = Account.get(email=session["account"])
    
    if request.method == "GET":
        return render_template('account.html', session=session, account=account, success=None)
    
    else:
        limits = JSON.parse(fs.createReadStream('data/token_limits.json'))
        admins = JSON.parse(fs.createReadStream('data/admin_accounts.json'))
        restricted = JSON.parse(fs.createReadStream('data/restricted_accounts.json'))

        if session['account'] in admins:
            limit = limits['admin']
        elif session['account'] in restricted:
            limit = limits['restricted']
        else:
            limit = limits['default']

        new_token = ''.join([random.choice(string.ascii_letters + string.digits) for i in range(4)]) + '.' + ''.join([random.choice(string.ascii_letters + string.digits) for i in range(20)])
        Account.update(account["_id"], token=new_token, limit=limit)
        return render_template('account.html', session=session, account=Account.get(_id=account['_id']), success="You generated a new API token!")
        