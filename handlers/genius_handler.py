import lyricsgenius

from flask_restful import abort

from PyJS import JSON
from PyJS.modules import fs

genius = lyricsgenius.Genius(JSON.parse(fs.createReadStream("data/config.json"))["genius"])

def get(name, author):
    song = genius.search_song(name, author if author else "")
    if not song:
        return abort(400, message="Song not found!")
    
    return {
        "title": song.title,
        "artist": song.artist,
        "lyrics": song.lyrics
    }