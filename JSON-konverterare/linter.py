#!/usr/bin/env python3

import os, re

warning_count = 0

# TODO: add check for font size changes inside of tags, as well as manual vspaces.
# TODO: Search for "% TODO: Digitalize"
# Perhaps also look for noindents
# Note that this does not catch everything. (eg. missing lyrics tags, etc.)
def analyze(path: str):
    global warning_count
    with open(path, "r") as file:
        i = 0
        for line in file:
            i += 1
            if re.search(r"\\huge{(\w{0,2}(\$.*?\$)?) (.*)}", line) is not None:
                print(path+":"+str(i), "\t-\tChapter title uses old syntax: ", line.strip())
                warning_count += 1
            elif (re.search(r"\\Large\s([\$]\\[a-z]+?[,\d\.]*?\$[a-z]?)\.\s([^\\]*).*", line) is not None)\
                or (re.search(r"\\Large\s[\$]\\[\w\/]+?\\[a-z]+?\$\.", line) is not None)\
                or (re.search(r"\\Large\so\d+?[a-z]?\. ", line) is not None):
                print(path+":"+str(i), "\t-\tSong title uses old syntax: ", line.strip())
                warning_count += 1
            elif re.search(r"\\begin\{flushright\}", line) is not None:
                print(path+":"+str(i), "\t-\tAuthor probably uses old syntax (see the next line): ", line.strip())
                warning_count += 1

if __name__ == "__main__":
    for d in sorted(os.listdir("..")):
        if d[0:2].isdigit() and int(d[0:2]) > 0 and os.path.isdir(d):
            for f in os.listdir(d):
                if f.lower().endswith(".tex"):
                    analyze(d+"/"+f)
    print("Total warnings: ", warning_count)