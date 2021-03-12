from PyJS import JSON
from PyJS.modules import fs

def route(query):
    return JSON.parse(fs.createReadStream('data/routes.json'))[query]