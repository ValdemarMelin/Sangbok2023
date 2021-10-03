#!/usr/bin/env python3

import os, re
from typing import Union
from utils import warning, info, err

from classes import *

import pylatexenc.latexwalker as lw
import pylatexenc.macrospec as ms
import pylatexenc.latex2text as l2t

ctx = lw.get_default_latex_context_db()
ctx.add_context_category(
    'digital',
    prepend=True,
    macros=[
        ms.MacroSpec("chaptertitle", r"{{"),
        ms.MacroSpec("chaptertitlenobr", r"{{"),

        ms.MacroSpec("songtitle", r"{{"),
        ms.MacroSpec("songsubtitle", "{"),
        ms.MacroSpec("songsubtitlelarge", "{"),
        
        ms.MacroSpec("sheetmusicnotice", "{"),
        ms.MacroSpec("sheetmusicnoticenormal", "{"),
        ms.MacroSpec("sheetmusicnoticefootnote", "{"),

        ms.MacroSpec("mel", "{"),
        ms.MacroSpec("auth", "{"),
        
    ],
    environments=[
        ms.EnvironmentSpec("lyrics", "")
    ]
)

def parse(path: str) -> Chapter:
    global ctx
    chapter = None

    with open(path, "r") as file:
        curSong = None

        raw = file.read()
        raw = re.sub(r"\\\\\n", r"\n", raw)
        raw = re.sub(r"\\newline", r"\n", raw)
        raw = re.sub(r"\\newpage", r"\n", raw)
        raw = re.sub(r"\\vspace{\dpt}", r"\n", raw)
        raw = re.sub(r"\\vspace{\d\dpt}", r"\n\n", raw)
        raw = raw.replace('\|', "||")

        w = lw.LatexWalker(raw, latex_context=ctx)
        (nodelist, pos, len_) = w.get_latex_nodes(pos=0)
        root = getFirstEnvNode(nodelist)
        for node in root.nodelist:
            if node.isNodeType(lw.LatexMacroNode):
                if node.macroname.startswith('chaptertitle'):
                    chapter = parse_chapter_title(node)
                elif node.macroname == 'auth':
                    if curSong is not None:
                        curSong.setAuthor(parse_singular_macro_node(node))
                    else:
                        warning("Tried to set the author of curSong, which is set to None.")
                elif node.macroname == 'mel':
                    pass
            elif node.isNodeType(lw.LatexEnvironmentNode):
                if node.environmentname == 'center':
                    newSong = parse_song_header(node)
                    if newSong is not None:
                        if curSong is not None:
                            chapter.songs.append(curSong)
                            if len(curSong.text) == 0:
                                err("Song " + curSong.prefix + " has unparseable lyrics.")
                        curSong = newSong
                    else:
                        warning("Found a center environment that is not a song header. It will be ignored for now.")
                elif node.environmentname == 'lyrics':
                    curSong.setLyrics(parse_song_lyrics(node))
                elif node.environmentname in ['figure', 'minipage']: # Check that this works properly. Not sure if its JS or Python it won't work in.
                    warning("Handler for environment " + node.environmentname + " is not implemented.")
                elif node.environmentname == 'comment':
                    warning("Handler for environment " + node.environmentname + " is not implemented.")
                else:
                    warning("Unhandled environment: " + node.environmentname)

    if curSong is not None:
        chapter.songs.append(curSong)
    
    return chapter



def parse_song_header(node: lw.LatexEnvironmentNode) -> Song:
    assert node.environmentname == 'center'
    song = None
    for n in node.nodelist:
        if n.isNodeType(lw.LatexMacroNode):
            if n.macroname == 'songtitle':
                song = parse_song_title(n)
            elif n.macroname == 'mel':
                if song is not None:
                    song.setMelody(parse_singular_macro_node(n))
                else:
                    warning("Cannot assign melody to empty song.")
            elif n.macroname.startswith('songsubtitle'):
                song.setSubtitle(parse_singular_macro_node(n).strip('()'))
            elif n.macroname.startswith('sheetmusicnotice'):
                song.setSheetMusicNotice(parse_singular_macro_node(n))
    return song

def parse_singular_macro_node(node: lw.LatexMacroNode) -> str:
    return l2t.LatexNodes2Text().node_to_text(node.nodeargd.argnlist[0]).replace(" \n", "\n").replace("\n\n\n","\n\n").replace("\n\n\n","\n\n")

def parse_song_lyrics(node: lw.LatexEnvironmentNode) -> str:
    return l2t.LatexNodes2Text().node_to_text(node).strip().replace(" \n", "\n").replace("\n\n\n","\n\n").replace("\n\n\n","\n\n")

def parse_chapter_title(node: lw.LatexMacroNode) -> Chapter:
    return Chapter(*map(l2t.LatexNodes2Text().node_to_text, node.nodeargd.argnlist))

def parse_song_title(node: lw.LatexMacroNode) -> Song:
    n2t = l2t.LatexNodes2Text().node_to_text
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
    