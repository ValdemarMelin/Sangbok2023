#!/usr/bin/env python3

import os, re
from typing import Union
from utils import warning, info, err

from classes import *

import pylatexenc.latexwalker as lw
import pylatexenc.macrospec as ms
import pylatexenc.latex2text as l2t
from contexts import LW_CTX, L2T_CTX

def parse(path: str) -> Chapter:
    global LW_CTX
    chapter = None

    with open(path, "r") as file:
        song = None

        # TODO: Use L2T_CTX for this instead.
        raw = file.read()
        raw = re.sub(r"\\\\\n", r"\n", raw)
        raw = re.sub(r"\\vspace{\dpt}", r"\n", raw)
        raw = re.sub(r"\\vspace{\d\dpt}", r"\n\n", raw)
        raw = raw.replace('\|', "||")

        w = lw.LatexWalker(raw, latex_context=LW_CTX)
        (nodelist, pos, len_) = w.get_latex_nodes(pos=0)
        root = getFirstEnvNode(nodelist)
        for node in root.nodelist:
            chapter, song = recurse_node(node, chapter, song)

    if song is not None:
        chapter.songs.append(song)
    
    return chapter

# May mutate chapter & song.
# Have you ever seen such beautiful code? <3
def recurse_node(node, chapter, song) -> (Chapter, Song):
    if node.isNodeType(lw.LatexMacroNode):
        if node.macroname.startswith('chaptertitle'):
            chapter = parse_chapter_title(node)
        elif node.macroname == 'songtitle':
            newSong = parse_song_title(node)
            if newSong is not None:
                if song is not None:
                    chapter.songs.append(song)
                    if len(song.text) == 0:
                        err("Song " + song.prefix + " has unparseable lyrics.")
                song = newSong
            else:
                err("Unparseable songtitle.")
        elif node.macroname.startswith('songsubtitle'):
            song.setSubtitle(parse_singular_macro_node(node).strip('()'))
        elif node.macroname.startswith('sheetmusicnotice'):
            song.setSheetMusicNotice(parse_singular_macro_node(node))
        # TODO: A lot of these are very similar (redundant).
        elif node.macroname == 'auth':
            if song is not None:
                song.setAuthor(parse_singular_macro_node(node))
            else:
                warning("Tried to set the author of song, which is set to None.")
        elif node.macroname == 'mel':
            if song is not None:
                song.setMelody(parse_singular_macro_node(node))
            else:
                warning("Cannot assign melody to empty song.")
        elif node.macroname == 'digitalonly':
            chapter, song = recurse_node(node.nodeargd.argnlist[0], chapter, song)
        elif node.macroname == 'course':
            song.setCourse(parse_singular_macro_node(node))
    elif node.isNodeType(lw.LatexEnvironmentNode):
        if node.environmentname == 'lyrics':
            song.setLyrics(parse_song_lyrics(node))
        elif node.environmentname in ['figure', 'minipage', 'subfigure', 'table', 'center']:
            for n in node.nodelist:
                chapter, song = recurse_node(n, chapter, song)
        elif node.environmentname in ['flushright']:
            warning("Recursing a(n) " + node.environmentname + " environment. You may want to check the tex source, to see if you really want to use this environment here.")
            for n in node.nodelist:
                chapter, song = recurse_node(n, chapter, song)
        elif node.environmentname == 'comment':
            warning("Handler for environment " + node.environmentname + " is not implemented.")
        else:
            warning("Unhandled environment: " + node.environmentname)
    elif node.isNodeType(lw.LatexGroupNode):
        for n in node.nodelist:
            chapter, song = recurse_node(n, chapter, song)
        if len(node.nodelist) > 1:
            # This error is most likely caused by usage of macros that are not defined in the context.
            warning("Recursing a GroupNode of length > 1. This may cause unexpected behavior, since it's principally meant for parsing the contents of \digitalonly macros.")
    return chapter, song





L2T = l2t.LatexNodes2Text(L2T_CTX)

def parse_singular_macro_node(node: lw.LatexMacroNode) -> str:
    return L2T.node_to_text(node.nodeargd.argnlist[0]).replace(" \n", "\n").replace("\n\n\n","\n\n").replace("\n\n\n","\n\n")

def parse_song_lyrics(node: lw.LatexEnvironmentNode) -> str:
    return L2T.node_to_text(node).strip().replace(" \n", "\n").replace("\n\n\n","\n\n").replace("\n\n\n","\n\n")

def parse_chapter_title(node: lw.LatexMacroNode) -> Chapter:
    return Chapter(*map(L2T.node_to_text, node.nodeargd.argnlist))

def parse_song_title(node: lw.LatexMacroNode) -> Song:
    n2t = L2T.node_to_text
    regex = r"\s\((.*)\)"

    title = n2t(node.nodeargd.argnlist[1])
    song = Song(n2t(node.nodeargd.argnlist[0]), re.sub(regex, "", title))
    subtitle_raw = re.search(regex, title)
    if subtitle_raw is not None:
        song.setSubtitle(subtitle_raw.group(1))
    return song

def getFirstEnvNode(nodelist):
    for node in nodelist:
        if node.isNodeType(lw.LatexEnvironmentNode) and node.environmentname == 'document':
            return node

# Run through all files and run parse() on each one.
if __name__ == "__main__":
    chapters: [Chapter] = []
    for d in sorted(os.listdir("..")):
        if d[0:2].isdigit() and 0 < int(d[0:2]) < 16 and os.path.isdir("../"+d):
            info("Reading chapter {}.".format(int(d[0:2])))
            for f in os.listdir("../"+d):
                if f.lower().endswith(".tex"):
                    chapters.append(parse("../" + d + "/" + f))
    with open("out.json", "w") as f:
        info("Exporting to out.json (overwrite mode).")
        f.write("[\n" + ",".join([c.toJSON() for c in chapters if c is not None]) + "\n]")
    