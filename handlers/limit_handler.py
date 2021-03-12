from threading import Thread
from handlers.account_handler import accounts

import time

def clear():
    while True:
        accounts.update_many({}, {"$set": {"uses":0}})
        print("Uses were reset")
        time.sleep(60)

def start():
    timer = Thread(target=clear)
    timer.start()