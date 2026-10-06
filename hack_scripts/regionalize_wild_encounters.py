#!/usr/bin/env python3
"""Superseded by hack_scripts/build_wild_encounters.py, which rebuilds the tables and imports the
helpers here. Kept for those helpers; running it on its own adds species to rare slots only.

Make every Pokémon of a region's generations catchable in that region (design/balance.md):

    Kanto (FireRed and Heart & Soul's Kanto): Gen 1, 4, 7
    Johto:                                   Gen 2, 5, 8
    Hoenn:                                   Gen 3, 6, 9

Pokémon already in src/data/wild_encounters.json stay catchable (a slot is only reused if its
Pokémon also appears elsewhere in the region). Each on-region family that can't yet be
caught in its region is added to the rare encounter slots (land 5%/4%/1%, surfing and rock smash
5%/4%/1%, Super Rod 4%/1%) of that region's maps, preferring maps whose Pokémon share a type with
it (so Water types go to water, Rock types to caves). Each family gets up to SLOTS_PER_FAMILY slots.
Legendaries, Mythicals, Ultra Beasts, Paradox Pokémon and starters are left for events
(design/story.md). Pseudo-legendaries only go to slots of level 25+.

Other areas (Sinjoh, Alola, Hisui, Battle Frontier) are left alone. Run it once on the original
table; the additions are listed in design/wild_species_added.md.

    python3 hack_scripts/regionalize_wild_encounters.py [--dry-run]
"""
import argparse, collections, glob, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import subprocess
from region_constants import ROOT

ENCOUNTERS = os.path.join(ROOT, "src/data/wild_encounters.json")
REPORT = os.path.join(ROOT, "design/wild_species_added.md")
REGION_GENS = {"Kanto": {1, 4, 7}, "Johto": {2, 5, 8}, "Hoenn": {3, 6, 9}}
FORM_GEN = {"isAlolanForm": 7, "isGalarianForm": 8, "isHisuianForm": 8, "isPaldeanForm": 9}
STARTERS = {f"SPECIES_{n}" for n in (
    "BULBASAUR CHARMANDER SQUIRTLE CHIKORITA CYNDAQUIL TOTODILE TREECKO TORCHIC MUDKIP TURTWIG CHIMCHAR "
    "PIPLUP SNIVY TEPIG OSHAWOTT CHESPIN FENNEKIN FROAKIE ROWLET LITTEN POPPLIO GROOKEY SCORBUNNY SOBBLE "
    "SPRIGATITO FUECOCO QUAXLY PIKACHU EEVEE").split()}
RARE_SLOTS = {"land_mons": (6, 7, 8, 9, 10, 11), "water_mons": (2, 3, 4), "rock_smash_mons": (2, 3, 4),
              "fishing_mons": (8, 9)}
SLOTS_PER_FAMILY = 2
# Pseudo-legendary lines only appear at higher levels.
PSEUDO = {f"SPECIES_{n}" for n in "DRATINI LARVITAR BAGON BELDUM GIBLE DEINO GOOMY JANGMO_O DREEPY FRIGIBAX".split()}
EXCLUDE = ("isLegendary", "isSubLegendary", "isRestrictedLegendary", "isMythical", "isUltraBeast",
           "isParadox", "isMegaEvolution", "isGigantamax", "isTotem", "isPrimalReversion",
           "isUltraBurst", "isTeraForm")


GEN_STARTS = [1, 152, 252, 387, 494, 650, 722, 810, 906]  # first National Dex number of each generation


def national_dex_numbers():
    text = open(os.path.join(ROOT, "include/constants/pokedex.h")).read()
    body = text[text.index("NATIONAL_DEX_NONE"):]
    body = re.sub(r"//[^\n]*|/\*.*?\*/", "", body[:body.index("}")], flags=re.S)
    names = re.findall(r"\b(NATIONAL_DEX_\w+)\b", body)
    return {n: i for i, n in enumerate(names)}


def load_species():
    dexnum = national_dex_numbers()
    species = {}
    for gen in range(1, 10):
        text = open(os.path.join(ROOT, f"src/data/pokemon/species_info/gen_{gen}_families.h")).read()
        for m in re.finditer(r"^    \[(SPECIES_\w+)\]\s*=\s*\{(.*?)^    \},", text, re.M | re.S):
            name, body = m.group(1), m.group(2)
            stats = [int(x) for x in re.findall(r"\.base(?:HP|Attack|Defense|Speed|SpAttack|SpDefense)\s*=\s*(\d+)", body)[:6]]
            types = (re.findall(r"\.types\s*=\s*MON_TYPES\(([^)]*)\)", body) or [None])[-1]
            flags = set(re.findall(r"\.(is\w+)\s*=\s*TRUE", body))
            evo_list = re.findall(r"\{\s*(EVO_\w+)\s*,\s*([^,{}]+),\s*(SPECIES_\w+)", body)
            evos = [t for _, _, t in evo_list]
            dex = re.search(r"\.natDexNum\s*=\s*(NATIONAL_DEX_\w+)", body)
            if dex and dex.group(1) in dexnum:   # the family files group families, not generations
                gen = sum(dexnum[dex.group(1)] >= start for start in GEN_STARTS)
            g = next((FORM_GEN[f] for f in FORM_GEN if f in flags), gen)
            species[name] = {
                "dex": dex.group(1) if dex else None,
                "gen": g,
                "bst": sum(stats),
                "types": [t.strip() for t in types.split(",")] if types else [],
                "flags": flags,
                "evos": [e for e in evos if e != name],
                # level each evolution happens at (non-level evolutions: 36, as in src/level_scaling.c)
                "evo_level": {t: (int(p) if m == "EVO_LEVEL" and p.strip().isdigit() and int(p) > 0 else 36)
                              for m, p, t in evo_list},
            }
    return species


def mark_default_forms(species):
    """The first species listed for each National Dex number is its default form."""
    seen = set()
    for name, info in species.items():
        info["default"] = info["dex"] is not None and info["dex"] not in seen
        seen.add(info["dex"])


def is_candidate(name, info):
    if info["flags"] & set(EXCLUDE) or not info["types"]:
        return False
    return info["default"] or bool(info["flags"] & set(FORM_GEN))


def families(species):
    """Map each species to (base species, stage) and each base to its stage lists."""
    pre = {}
    for name, info in species.items():
        for e in info["evos"]:
            if e in species and e not in pre:
                pre[e] = name
    base_of, stage_of = {}, {}
    for name in species:
        n, depth = name, 0
        while n in pre and depth < 4:
            n, depth = pre[n], depth + 1
        base_of[name], stage_of[name] = n, depth
    lines = collections.defaultdict(lambda: collections.defaultdict(list))
    for name in species:
        lines[base_of[name]][stage_of[name]].append(name)
    return base_of, stage_of, lines


def mapsec_values():
    """Map section numbers as the combined build sees them (the enum, run through cpp)."""
    pp = subprocess.run(["arm-none-eabi-gcc", "-E", "-P", "-x", "c", "include/constants/region_map_sections.h",
                         "-iquote", "include", "-DPOKEMON_HNS", "-DMAPS_HNS", "-DMAPS_EMERALD", "-DMAPS_FIRERED"],
                        capture_output=True, text=True, check=True, cwd=ROOT).stdout
    vals, n = {}, 0
    body = pp[pp.index("MAPSEC_"):]
    body = body[:body.index("}")]
    for item in body.split(","):
        item = item.strip()
        if not item:
            continue
        if "=" in item:
            name, expr = (x.strip() for x in item.split("=", 1))
            n = vals[expr] if expr in vals else int(expr, 0)
        else:
            name = item
        vals[name] = n
        n += 1
    text = open(os.path.join(ROOT, "include/constants/region_map_sections.h")).read()
    hns = text[:text.index("#else")]
    for macro in ("KANTO_MAPSEC_START", "KANTO_MAPSEC_END", "JOHTO_MAPSEC_START", "JOHTO_MAPSEC_END"):
        vals[macro] = vals[re.search(rf"#define {macro}\s+(\w+)", hns).group(1)]
    return vals


def map_regions():
    """Return {MAP_X: region} for every map in a region with a generation rule."""
    maps = {}
    secs = {}
    for path in glob.glob(os.path.join(ROOT, "data/maps/*/map.json")):
        d = json.load(open(path))
        maps[d["id"]] = (d.get("game_version", "emerald"), d.get("region_map_section", ""))
        secs[d.get("region_map_section", "")] = True
    vals = mapsec_values()
    regions = {}
    for map_id, (version, sec) in maps.items():
        if version == "emerald":
            regions[map_id] = "Hoenn"
        elif version == "frlg":
            regions[map_id] = "Kanto"
        elif sec in vals:
            v = vals[sec]
            if vals["KANTO_MAPSEC_START"] <= v <= vals["KANTO_MAPSEC_END"]:
                regions[map_id] = "Kanto"
            elif vals["JOHTO_MAPSEC_START"] <= v <= vals["JOHTO_MAPSEC_END"]:
                regions[map_id] = "Johto"
    return regions


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--dry-run", action="store_true", help="print the swaps, don't write files")
    args = parser.parse_args()

    species = load_species()
    mark_default_forms(species)
    base_of, stage_of, lines = families(species)
    regions = map_regions()
    data = json.load(open(ENCOUNTERS))
    headers = next(g for g in data["wild_encounter_groups"] if g["label"] == "gWildMonHeaders")

    present = collections.defaultdict(set)
    occurrences = collections.defaultdict(collections.Counter)  # region -> species -> slots holding it
    slots = collections.defaultdict(list)   # region -> [(types nearby, field, mon)]
    for enc in headers["encounters"]:
        region = regions.get(enc.get("map"))
        if not region:
            continue
        map_types = collections.Counter()
        for field in enc.values():
            if isinstance(field, dict) and "mons" in field:
                for mon in field["mons"]:
                    occurrences[region][mon["species"]] += 1
                    if mon["species"] in species:
                        present[region].add(base_of[mon["species"]])
                        map_types.update(species[mon["species"]]["types"])
        for name, field in enc.items():
            if isinstance(field, dict) and "mons" in field:
                field_types = collections.Counter()
                for mon in field["mons"]:
                    field_types.update(species.get(mon["species"], {"types": []})["types"])
                for i in RARE_SLOTS.get(name, ()):
                    if i < len(field["mons"]):
                        slots[region].append((map_types if name == "land_mons" else field_types, name, field["mons"][i]))

    changed = 0
    report = ["# Wild Pokémon added", "",
              "Generated by `hack_scripts/regionalize_wild_encounters.py`: families added to each region's",
              "rare wild encounter slots so every Pokémon of its generations can be caught there.", ""]
    for region in ("Kanto", "Johto", "Hoenn"):
        gens = REGION_GENS[region]
        missing = sorted(b for b in lines if b in species and species[b]["gen"] in gens and b not in STARTERS
                         and is_candidate(b, species[b]) and b not in present[region]
                         and all(is_candidate(x, species[x]) for st in lines[b].values() for x in st))
        free = list(slots[region])
        added = collections.defaultdict(list)
        for _round in range(SLOTS_PER_FAMILY):
            for fam in missing:
                types = set(species[fam]["types"])
                water = "TYPE_WATER" in types
                best, best_score = None, None
                for k, (near, name, mon) in enumerate(free):
                    if fam in PSEUDO and mon["min_level"] < 25:
                        continue
                    if water != (name in ("water_mons", "fishing_mons")):
                        continue
                    if occurrences[region][mon["species"]] <= 1:
                        continue  # the last place this Pokémon appears in the region: keep it
                    sc = (sum(near[t] for t in types), -k)
                    if best_score is None or sc > best_score:
                        best, best_score = k, sc
                if best is None:
                    continue
                near, name, mon = free.pop(best)
                occurrences[region][mon["species"]] -= 1
                mon["species"] = fam
                added[fam].append(name.replace("_mons", ""))
                changed += 1
        report += [f"## {region} (Gen {', '.join(map(str, sorted(gens)))})", "",
                   f"{len(missing)} families added; {len(free)} rare slots kept as they were.", "",
                   "| Family | Slots |", "|---|---|"]
        report += [f"| {f[8:].title()} | {', '.join(added[f]) or 'no slot found'} |" for f in missing]
        report.append("")

    print(f"{changed} encounter slots changed")
    if args.dry_run:
        print("\n".join(report))
        return
    if changed == 0:
        return  # already done; keep the existing report
    with open(ENCOUNTERS, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    open(REPORT, "w").write("\n".join(report))


if __name__ == "__main__":
    main()
