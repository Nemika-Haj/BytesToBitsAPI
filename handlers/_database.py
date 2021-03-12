from pymongo import MongoClient

from PyJS import JSON
from PyJS.modules import fs

client = MongoClient(JSON.parse(fs.createReadStream('data/config.json'))['mongo'])["database"]

def get_col(col_name):
    return client[col_name]