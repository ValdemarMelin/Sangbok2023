#!/usr/bin/env python3
# Standalone script

import json
from utils import warning, err, info

def normalize_lyrics(lyrics: str) -> str:
    return lyrics.replace(".", "").replace(",", "").replace("!","").lower()

def gender_neutralize(lyrics: str) -> str:
    return lyrics.replace("han", "hen").replace("hon", "hen").replace("man", "en")

def compare_lyrics(lyrics1: str, lyrics2: str) -> bool:
    n1 = normalize_lyrics(lyrics1)
    n2 = normalize_lyrics(lyrics2)
    id = tgt_song["index"] + ". " + tgt_song["title"]
    if n1 == n2:
        return
    elif len(n1) == 0 or 0 == len(n2):
        err(id + " has \033[31mempty\033[m lyrics.")
    elif n1.replace("\n", "") == n2.replace("\n", ""):
        info(id + " has \033[34mline-break\033[m problems.")
    elif n1.replace("\n", "").replace(" ", "") == n2.replace("\n", "").replace(" ", ""):
        info(id + " has \033[34mspacing\033[m problems.")
    elif gender_neutralize(n1) == gender_neutralize(n2):
        info(id + " has \033[34mpronoun\033[m inconsistencies.")
    elif n1.startswith(n2) or n2.startswith(n1):
        warning(id + " has missing \033[36mverses\033[m.")
    else:
        warning(id + " has some \033[33mother\033[m problem.")

with open("target.json", "r") as file:
    target = json.load(file)

with open("out.json", "r") as file:
    output = json.load(file)

for (tgt_chapter, out_chapter) in zip(target, output):
    assert tgt_chapter["chapter"] == out_chapter["chapter"]
    for tgt_song in tgt_chapter["songs"]:
        try:
            out_song = next(filter(lambda s: s["index"]==tgt_song["index"], out_chapter["songs"]))
        except StopIteration:
            err("Index not found: " + tgt_song["index"])
            continue
            
        compare_lyrics(tgt_song["text"], out_song["text"])
