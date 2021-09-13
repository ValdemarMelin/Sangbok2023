#!/usr/bin/env python3

import os, re
from classes import *

def parse(path: str) -> Chapter:
    state: ParserState = ParserState.GENERIC
    current_song = None
    chapter = None
    with open(path, "r") as file:
        for line in file:
            if line.strip().startswith("%"):
                continue
            elif line.strip().startswith("\chaptertitle"):
                params = re.search(r"\\chaptertitle\{(.*)\}\{(.*)\}", line)
                chapter = Chapter(params.group(1), params.group(2))
            elif line.strip().startswith("\songtitle"):
                if current_song is not None:
                    assert chapter is not None
                    chapter.songs.append(current_song)
                params = re.search(r"\\songtitle\{(.*)\}\{(.*)\}", line)
                current_song = Song(params.group(1), params.group(2))
    return chapter

if __name__ == "__main__":
    chapters: [Chapter] = []
    for d in sorted(os.listdir("..")):
        if d[0:2].isdigit() and int(d[0:2]) > 0 and os.path.isdir("../"+d):
            for f in os.listdir("../"+d):
                if f.lower().endswith(".tex"):
                    chapters.append(parse("../" + d + "/" + f))
    print("[" + ",".join([c.toJSON() for c in chapters if c is not None]) + "]")
    