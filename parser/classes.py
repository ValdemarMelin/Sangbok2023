import json
from utils import warning, err

class Song:
    """Represents a Song."""
    title:            str
    prefix:           str
    author:           str
    melody:           str
    text:             str
    subtitle:         str
    sheetmusicnotice: str
    course:           str
    instruction:      str

    def __init__(self, prefix: str, title: str):
        self.title            = title
        self.prefix           = prefix
        self.author           = ""
        self.melody           = ""
        self.text             = ""
        self.subtitle         = ""
        self.sheetmusicnotice = ""
        self.course           = ""
        self.instruction      = ""

    def toJSON(self) -> str: # TODO: Escape formatted strings
        return json.dumps(self.toDict(), ensure_ascii = False, indent = "\t")

    def toDict(self) -> dict:
        return {
            "title": self.title,
            "author": self.author,
            "melody": "\n".join(filter(lambda x: len(x) > 0, ["("+self.subtitle+")" if len(self.subtitle) > 0 else "", self.melody, self.course, self.sheetmusicnotice, self.instruction])),
            "text": self.text,
            "index": self.prefix
        }
    
    def toCSVRow(self):
        return '"{}", "{}", "{}", "{}"'.format(self.prefix,self.title, self.author, self.melody)

    # TODO: The below functions are VERY redundant.
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

    def setSheetMusicNotice(self, sheetmusicnotice) -> bool:
        if len(self.sheetmusicnotice) == 0:
            self.sheetmusicnotice = sheetmusicnotice
        else:
            err("Tried to assign sheetmusicnotice to a song with non-empty sheetmusicnotice: " + self.prefix)

    def setSubtitle(self, subtitle) -> bool:
        if len(self.subtitle) == 0:
            self.subtitle = subtitle
        else:
            err("Tried to assign subtitle to a song with non-empty subtitle: " + self.prefix)

    def setCourse(self, course) -> bool:
        if len(self.course) == 0:
            self.course = course
        else:
            err("Tried to assign course to a song with non-empty course: " + self.prefix)
    
    def setInstruction(self, instruction) -> bool:
        if len(self.instruction) == 0:
            self.instruction = instruction
        else:
            err("Tried to assign instruction to a song with non-empty instruction: " + self.prefix)





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

    def inject(self, json):
        for jsong in json:
            # TODO: Add more checks
            song = Song(jsong["index"], jsong["title"])
            song.setAuthor(jsong["author"])
            song.setMelody(jsong["melody"])
            song.setLyrics(jsong["text"])
            self.songs.append(song)
    
    def toJSON(self) -> str:
        return json.dumps(self.toDict(), ensure_ascii = False, indent = "\t")
    
    def toDict(self) -> dict:
        return {
            "chapter": self.name,
            "prefix": self.prefix,
            "songs": [s.toDict() for s in self.songs if s is not None]
        }