#!/usr/bin/env python3

import os, re, sys
from main import *

if __name__ == "__main__":
    unparseable_song_count = 0
    chapters: [Chapter] = []
    for d in sorted(os.listdir("..")):
        if d[0:2].isdigit() and 0 < int(d[0:2]) < 16 and os.path.isdir("../"+d):
            # print("[\033[36mINFO\033[m] Reading chapter {}.".format(int(d[0:2])))
            for f in os.listdir("../"+d):
                if f.lower().endswith(".tex"):
                    unparseable_song_count += sum(s is None for s in parse("../" + d + "/" + f).songs)
    if unparseable_song_count > 0:
        print("[\033[31mERROR\033[m] Unparseable songs: {}".format(unparseable_song_count))
        sys.exit(1)
    else:
        print("All clean, no errors.")
    