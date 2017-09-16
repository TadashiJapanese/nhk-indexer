#!/usr/bin/env python3

import sqlite3, sys

""" 
Given a file containing some japanese text, and a level,
this script tells you the kanji in the text that you would
know, or not know, if you were that level.
"""

def get_known_kanji_code_points(level):
    conn = sqlite3.connect('wk_corpus.db')
    c = conn.cursor()
    codePoints = []
    for row in c.execute("select character from kanji where level <= ?", (level,)):
        codePoints.append(ord(row[0]))
    conn.close()
    return codePoints

def is_kanji(char):
    return ord(char) in range(19968,40879)

def get_unknown_kanji(text, level):
    corpus = get_known_kanji_code_points(level)
    kanjis = set([char for char in text if is_kanji(char)])
    unknown = [k for k in kanjis if ord(k) not in corpus]
    known   = [k for k in kanjis if ord(k) in corpus]
    return (known, unknown)

def for_single_level():
    
    filename, level = (sys.argv[1], sys.argv[2])
    
    text = open(filename).read()
    knownKanji, unknownKanji = get_unknown_kanji(text, level)
    percent = int(len(knownKanji)/(len(knownKanji)+len(unknownKanji))*100)
    
    print("known/unknown kanji in %s for level %s" % (filename, level))
    print("known: " + " ".join(knownKanji))    
    print("unknown: " + " ".join(unknownKanji))
    print("%s%%" % percent)

def for_all_levels(levelMax=50):

    filename = sys.argv[1]    
    text = open(filename).read()
    
    for level in range(1, levelMax+1):
        knownKanji, unknownKanji = get_unknown_kanji(text, level)
        percent = int(len(knownKanji)/(len(knownKanji)+len(unknownKanji))*100)
        print("level %s: %s%%" % (level, percent))

def for_all_levels_dict(text, levelMax=50):

    out = {}
    
    for level in range(1, levelMax+1):
        knownKanji, unknownKanji = get_unknown_kanji(text, level)
        percent = int(len(knownKanji)/(len(knownKanji)+len(unknownKanji))*100)
        out[level] = percent

    return out
        
if __name__ == "__main__":

    if len(sys.argv) == 3:
        for_single_level()
    elif len(sys.argv) == 2:
        for_all_levels()
    else:
        print("usage: %s filename [level]" % sys.argv[0])
