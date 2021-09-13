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
    
    def toJSON(self) -> str: # TODO: Escape formatted strings
        return "\t\t\t{\n" + \
            '\t\t\t\t"title": "' + self.title + '",\n' + \
            '\t\t\t\t"author": "' + self.author + '",\n' + \
            '\t\t\t\t"melody": "' + self.melody + '",\n' + \
            '\t\t\t\t"lyrics": "' + self.text + '",\n' + \
            '\t\t\t\t"index": "' + self.prefix + '"\n' + \
            "\t\t\t}"

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
        return "\t{" + "\n\t\t\"chapter\": \"{}\",\n\t\t\"prefix\": \"{}\",\n\t\t\"songs\": [\n{}\t\t\n]".format(self.name, self.prefix, ",\n".join([s.toJSON() for s in self.songs if s is not None])) + r"}"