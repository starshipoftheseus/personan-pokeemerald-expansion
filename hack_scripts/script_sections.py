#!/usr/bin/env python3
"""Split data/event_scripts.s into its sections and list the files each one includes.

Sections: hoenn_maps (unconditional Emerald map scripts before the FRLG block), frlg (.if IS_FRLG),
common (unconditional, after the FRLG block, before the HnS block), hns (.if IS_HNS / MAPS_HNS block)."""
import os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def sections():
    lines = open(os.path.join(ROOT, "data/event_scripts.s")).read().split("\n")
    out = {"hoenn_maps": [], "frlg": [], "common": [], "hns": []}
    inline = {k: [] for k in out}
    state = "hoenn_maps"; seen_frlg = False; depth = 0; block = None
    for l in lines:
        s = l.strip()
        if s.startswith("#ifdef MAPS_FIRERED"):
            state = "frlg"; seen_frlg = True; continue
        if s.startswith("#endif // MAPS_FIRERED"):
            state = "common"; continue
        m = re.match(r"\.if\s+(\S+)", s)
        if m and depth == 0:
            cond = m.group(1)
            if cond in ("IS_FRLG",) and not seen_frlg and state == "hoenn_maps":
                block = "frlg"; seen_frlg = True; depth = 1; state = "frlg"; continue
            if cond in ("IS_FRLG",) and state == "hoenn_maps":
                block = "frlg"; depth = 1; state = "frlg"; continue
            if cond == "IS_HNS":
                prev = state; block = "hns"; depth = 1; state = "hns"; continue
        elif m:
            depth += 1
        if s == ".endif" and depth > 0:
            depth -= 1
            if depth == 0:
                state = "common"
            continue
        inc = re.match(r'\.include\s+"([^"]+)"', s)
        if inc:
            path = inc.group(1)
            sec = state
            if state in ("common",) and path.startswith("data/maps/") and not seen_frlg:
                sec = "hoenn_maps"
            out[sec].append(path)
        else:
            inline[state].append(l)
    return out, inline

if __name__ == "__main__":
    out, inline = sections()
    for k, v in out.items():
        print(k, len(v), v[:3], "...")
