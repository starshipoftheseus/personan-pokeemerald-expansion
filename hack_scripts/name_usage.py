#!/usr/bin/env python3
"""Report which parts of the game reference each constant name: Hoenn map scripts, common scripts,
HnS scripts, FRLG scripts, and C code. Used to decide how to merge per-region flags/vars."""
import os, re, sys, glob, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from script_sections import sections, ROOT

WORD = re.compile(r"\b[A-Z][A-Z0-9_]{2,}\b")

def words_in(path):
    try:
        return set(WORD.findall(open(os.path.join(ROOT, path), errors="ignore").read()))
    except FileNotFoundError:
        return set()

def usage_index():
    files, inline = sections()
    idx = collections.defaultdict(set)
    for sec, paths in files.items():
        for p in paths:
            for w in words_in(p):
                idx[w].add(sec)
        for w in WORD.findall("\n".join(inline[sec])):
            idx[w].add(sec)
    # map.json files reference flags too (hidden items, object visibility), per map set.
    import json
    for mj in glob.glob(os.path.join(ROOT, "data/maps/*/map.json")):
        ver = json.load(open(mj)).get("game_version", "emerald")
        sec = {"emerald": "hoenn_maps", "hns": "hns", "frlg": "frlg"}[ver]
        for w in words_in(os.path.relpath(mj, ROOT)):
            idx[w].add(sec)
    for p in glob.glob(os.path.join(ROOT, "src/**/*.c"), recursive=True) + glob.glob(os.path.join(ROOT, "src/**/*.h"), recursive=True):
        for w in words_in(os.path.relpath(p, ROOT)):
            idx[w].add("c")
    return idx

if __name__ == "__main__":
    idx = usage_index()
    for n in sys.argv[1:]:
        print(n, sorted(idx.get(n, [])))
