#!/usr/bin/env python3
"""Shared helpers: evaluate flag/var/trainer constants as each game build sees them."""
import os, re, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CC = "arm-none-eabi-gcc"

def names_in(path):
    out = []
    for line in open(os.path.join(ROOT, path)):
        m = re.match(r"\s*#define\s+(\w+)\s+\S", line)
        if m:
            out.append(m.group(1))
    return out

def evaluate(game, names, headers, extra_defines=()):
    """Return {name: int} for names that are numeric constants when built as `game`."""
    src = '#include "constants/global.h"\n' + "".join(f'#include "constants/{h}"\n' for h in headers)
    src += "".join(f'@@ "{n}" = {n}\n' for n in names)
    args = [CC, "-E", "-P", "-x", "c", "-", "-iquote", "include", "-DMODERN=1", "-DTESTING=0",
            f"-D{game}", "-std=gnu17"] + [f"-D{d}" for d in extra_defines]
    pp = subprocess.run(args, input=src, capture_output=True, text=True, check=True, cwd=ROOT).stdout
    vals = {}
    for line in pp.splitlines():
        if not line.startswith("@@ "):
            continue
        name, expr = line[3:].split(" = ", 1)
        name = name.strip('"')
        if name == expr:
            continue
        try:
            vals[name] = eval(expr.replace("/", "//").replace("&&", " and ").replace("||", " or "), {})
        except Exception:
            pass
    return vals
