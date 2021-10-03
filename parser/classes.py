import json
from utils import warning, err

class Song:
    """Represents a Song."""
    title:  str
    prefix: str
    author: str
    melody: str
    text:   str

    def __init__(self, prefix: str, title: str):
        self.title  = title
        self.prefix = prefix
        self.author = ""
        self.melody = ""
        self.text   = ""
    
    def setLyrics(self, text) -> bool:
        if len(self.text) == 0:
            self.text = text
        else:
            err("Tried to assign lyrics to a song with non-empty lyrics: " + self.prefix)

    def setMelody(self, melody) -> bool:
        if len(self.melody) == 0:
            self.melody = melody
        else:
            err("Tried to assign melody to a song with non-empty melody: " + self.prefix)

    def setAuthor(self, author) -> bool:
        if len(self.author) == 0:
            self.author = author
        else:
            err("Tried to assign author to a song with non-empty author: " + self.prefix)

    def toJSON(self) -> str: # TODO: Escape formatted strings
        return json.dumps(self.toDict(), ensure_ascii = False, indent = "\t")

    def toDict(self) -> dict:
        return {
            "title": self.title,
            "author": self.author,
            "melody": self.melody,
            "text": self.text,
            "index": self.prefix
        }

class Chapter():
    name:   str
    prefix: str
    songs:  [Song]

    def __init__(self, prefix: str, name: str):
        self.name = name
        self.prefix = prefix
        self.songs = []
    
    def __str__(self) -> str: 
        return "Chapter: " + self.prefix + " " + self.name + " with " + str(len(self.songs)) + " songs."
    
    def toJSON(self) -> str:
        return json.dumps(self.toDict(), ensure_ascii = False, indent = "\t")
    
    def toDict(self) -> dict:
        return {
            "chapter": self.name,
            "prefix": self.prefix,
            "songs": [s.toDict() for s in self.songs if s is not None]
        }