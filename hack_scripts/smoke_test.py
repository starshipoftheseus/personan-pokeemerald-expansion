#!/usr/bin/env python3
"""Headless smoke test: start a new game on a map and check it loads and runs.

For each map, patches gSmokeTestMap in a copy of the built ROM and runs it in tools/mgba/mgba-rom-test
(see src/smoke_test.c). The game skips the intro, starts a new game on that map, runs the overworld
for a few seconds and reports where the player ended up. A crash or hang shows up as a timeout.

Build first (make hns), then for example:
    python3 hack_scripts/smoke_test.py MAP_LITTLEROOT_TOWN MAP_NEW_BARK_TOWN_HNS
    python3 hack_scripts/smoke_test.py --all emerald      # every Hoenn map (game_version emerald)
    python3 hack_scripts/smoke_test.py --all hns --jobs 8
    python3 hack_scripts/smoke_test.py --trainers 1 MAP_NEW_BARK_TOWN_HNS   # check every trainer's party

Results: ok (still on the map), moved (a script warped the player elsewhere: fine for cutscenes),
timeout (crash or hang), error (emulator failed). Exit status is 1 if any map timed out or errored.
"""
import argparse, glob, json, os, re, shutil, struct, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROMTEST = os.path.join(ROOT, "tools/mgba/mgba-rom-test")
RESULTS = {0: "ok", 1: "moved"}


def map_ids():
    text = open(os.path.join(ROOT, "include/constants/map_groups.h")).read()
    return {name: (int(group), int(num))
            for name, num, group in re.findall(r"(MAP_\w+)\s*=\s*\((\d+)\s*\|\s*\((\d+)\s*<<\s*8\)\)", text)}


def maps_for_version(version):
    names = []
    for path in sorted(glob.glob(os.path.join(ROOT, "data/maps/*/map.json"))):
        data = json.load(open(path))
        if data.get("game_version", "emerald") == version:
            names.append(data["id"])
    return names


def symbol_offset(elf, name):
    out = subprocess.run(["arm-none-eabi-nm", elf], capture_output=True, text=True, check=True).stdout
    for line in out.splitlines():
        parts = line.split()
        if len(parts) == 3 and parts[2] == name:
            return int(parts[0], 16) - 0x08000000
    raise SystemExit(f"{name} not found in {elf}: rebuild with make hns")


def run_one(rom_bytes, offset, name, group, num, timeout):
    with tempfile.NamedTemporaryFile(suffix=".gba", delete=False) as f:
        patched = bytearray(rom_bytes)
        patched[offset:offset + 2] = struct.pack("<H", (group << 8) | num)
        f.write(patched)
        path = f.name
    try:
        proc = subprocess.run(["stdbuf", "-oL", ROMTEST, "-l15", "-ClogLevel.gba.dma=16", "-Rr0", path], capture_output=True, text=True, timeout=timeout)
        values = dict(re.findall(r"SMOKE (\w+)=(\d+)", proc.stdout))
        result = RESULTS.get(proc.returncode, "error")
        if not values:
            result = "error"
        if "rumour" in values:
            values["trainers"] = (f"rumour species {values['rumour_species']} on map "
                                  f"{values['rumour_group']}.{values['rumour_num']} level {values['rumour_level']}")
        if "trainers_checked" in values:
            values["trainers"] = f"{values['trainers_checked']} checked, {values['trainers_bad']} bad, lowest level {values.get('lowest_level')}"
            bad = re.findall(r"SMOKE bad_trainer=(\d+)", proc.stdout)
            return name, result, values, ("bad trainer ids: " + " ".join(bad)) if bad else ""
        return name, result, values, proc.stdout[-500:] if result == "error" else ""
    except subprocess.TimeoutExpired as e:
        out = e.stdout.decode(errors="ignore") if isinstance(e.stdout, bytes) else (e.stdout or "")
        frames = re.findall(r"SMOKE frame=(\d+)", out)
        where = "while loading" if "SMOKE loaded=" not in out else f"after frame {frames[-1] if frames else 0}"
        return name, "timeout", {"hung": where}, ""
    finally:
        os.unlink(path)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("maps", nargs="*", help="map constants, e.g. MAP_LITTLEROOT_TOWN")
    parser.add_argument("--all", metavar="VERSION", help="every map with this game_version (emerald, hns, frlg)")
    parser.add_argument("--rom", default=os.path.join(ROOT, "pokehns.gba"))
    parser.add_argument("--elf", default=os.path.join(ROOT, "pokehns.elf"))
    parser.add_argument("--timeout", type=float, default=30)
    parser.add_argument("--trainers", type=int, choices=(1, 2, 3, 4), metavar="MODE",
                        help="build every trainer's party on the first map given and check it "
                             "(2: with every badge and league won, so level scaling applies; "
                             "3: start a starter rumour there and report it)")
    parser.add_argument("--jobs", type=int, default=os.cpu_count() or 1)
    args = parser.parse_args()

    ids = map_ids()
    names = list(args.maps)
    if args.all:
        # --all skips map folders that aren't in any map group (unused maps).
        names += [n for n in maps_for_version(args.all) if n in ids]
    if not names:
        parser.error("give map names or --all VERSION")
    unknown = [n for n in names if n not in ids]
    if unknown:
        raise SystemExit(f"unknown maps (not in this build?): {', '.join(unknown)}")

    rom = open(args.rom, "rb").read()
    offset = symbol_offset(args.elf, "gSmokeTestMap")
    if args.trainers:
        rom = bytearray(rom)
        t = symbol_offset(args.elf, "gSmokeTestTrainers")
        rom[t:t + 2] = bytes([args.trainers, 0])
        names = names[:1]
        RESULTS[2] = "BAD TRAINERS"
    failed = 0
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        jobs = [pool.submit(run_one, rom, offset, n, *ids[n], args.timeout) for n in names]
        for job in jobs:
            name, result, values, log = job.result()
            if result in ("timeout", "error", "BAD TRAINERS"):
                failed += 1
            detail = " ".join(f"{k}={v}" for k, v in values.items()
                              if k in ("map_group", "map_num", "mapsec", "x", "y", "controls_locked", "script_running", "hung", "trainers"))
            print(f"{result:8} {name:50} {detail}")
            if log:
                print("         " + log.replace("\n", "\n         "))
    print(f"{len(names) - failed}/{len(names)} maps loaded without crashing")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
