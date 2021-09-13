#!/usr/bin/env python3

import os, re
from classes import *
from preprocessors import *
from typing import Union

def parse(path: str, none_on_warn = False) -> Chapter:
    chapter = None
    with open(path, "r") as file:
        # Match uncommented \songtitle commands.
        songs_raw = re.split(r"\n[^%\n]*\\songtitle", file.read())

        # Parse chapter title
        chapter_title = re.search(r"\\chaptertitle\{(.*)\}\{(.*)\}", songs_raw[0])
        if chapter_title is None:
            raise Exception("Chapter title cannot be parsed from: {}".format(songs_raw[0]))
        chapter = Chapter(*[clean_latex(chapter_title.group(i)) for i in [1,2]])
        chapter.songs = [parse_song(song_raw, none_on_warn=none_on_warn) for song_raw in songs_raw[1:]]
    return chapter

# TODO: Cleanup
def parse_song(song_raw: str, none_on_warn = False) -> Union[Song, None]:
    title_raw = re.search(r"\{(.*)\}\{(.*)\}", song_raw) # TODO: This means that songtitle cannot be more than one line...
    song = Song(*[clean_latex(title_raw.group(i)) for i in [1,2]])
    lyrics_raw = re.search(r"(\\begin\{lyrics\})\n?(.+(?:\n+.+)*?)\n?(\\end\{lyrics\})", song_raw)
    if lyrics_raw is None:
        lyrics_digital = re.search(r"(\\begin\{comment\}@digitallyrics\n)(.+(?:\n+.+)*)\n?(\\end\{comment\})", song_raw)
        if lyrics_digital is None:
            print("[\033[33mWARNING\033[m] Could not parse lyrics for {} - {}. Skipping.".format(song.prefix, song.title))
            return None
        else:
            song.text = clean_lyrics(lyrics_digital.group(2))
    else:
        song.text = clean_lyrics(lyrics_raw.group(2))
    if "\\auth" in song.text:
        print("[\033[33mWARNING\033[m] Author tag in lyrics environment for song {} - {}.".format(song.prefix, song.title))
        if none_on_warn:
            return None
    if len(song.text) < 3:
        print("[\033[33mWARNING\033[m] Lyrics is broken for song {} - {}.".format(song.prefix, song.title))
        if none_on_warn:
            return None
    return song

# Run through all files and run parse() on each one.
if __name__ == "__main__":
    chapters: [Chapter] = []
    for d in sorted(os.listdir("..")):
        if d[0:2].isdigit() and 0 < int(d[0:2]) < 16 and os.path.isdir("../"+d):
            print("[\033[36mINFO\033[m] Reading chapter {}.".format(int(d[0:2])))
            for f in os.listdir("../"+d):
                if f.lower().endswith(".tex"):
                    chapters.append(parse("../" + d + "/" + f))
    with open("out.json", "w") as f:
        print("[\033[36mINFO\033[m] Exporting to out.json (overwrite mode).")
        f.write("[\n" + ",".join([c.toJSON() for c in chapters if c is not None]) + "\n]")
    