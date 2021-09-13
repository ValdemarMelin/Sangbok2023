from enum import Enum

class ParserState(Enum):
    GENERIC = 1
    LYRICS = 2
    AUTHOR = 3

class Song:
    """Represents a Song."""
    title:  str
    prefix: str
    author: str
    melody: str
    text:   str

    def __init__(self, prefix: str, title: str):
        self.title = title
        self.prefix = prefix
        self.author = ""
        self.melody = ""
        self.text = ""
    
    def toJSON(self) -> str:
        return r"{" + \
            self.title + \
            r"}"

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
        # TODO: Escape formatted strings
        return r"{" + "chapter: \'{}\', prefix: \'{}\', songs: [{}]".format(self.name, self.prefix, ",".join([s.toJSON() for s in self.songs])) + r"}"