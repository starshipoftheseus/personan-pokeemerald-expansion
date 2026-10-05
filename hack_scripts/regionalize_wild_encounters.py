#!/usr/bin/env python3
"""Make each region's wild Pokémon come from that region's generations (design/balance.md):

    Kanto (FireRed and Heart & Soul's Kanto): Gen 1, 4, 7
    Johto:                                   Gen 2, 5, 8
    Hoenn:                                   Gen 3, 6, 9

Every off-region species in src/data/wild_encounters.json is swapped for an on-region one. Swaps
are made per evolution family, so a family is replaced by one family of the same length and each
stage maps to the same stage (Pidgey -> X, Pidgeotto -> X's evolution). Families are matched on
shared types first, then on similar base stat totals, spreading swaps over different families.
The same swap is used everywhere in a region. Legendaries, Mythicals, Ultra Beasts and Paradox
Pokémon are never picked.

Other areas (Sinjoh, Alola, Hisui, Battle Frontier) are left alone. Re-running is safe: on-region
species are never changed. The swaps made are listed in design/wild_species_swaps.md.

    python3 hack_scripts/regionalize_wild_encounters.py [--dry-run]
"""
import argparse, collections, glob, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import subprocess
from region_constants import ROOT

ENCOUNTERS = os.path.join(ROOT, "src/data/wild_encounters.json")
REPORT = os.path.join(ROOT, "design/wild_species_swaps.md")
REGION_GENS = {"Kanto": {1, 4, 7}, "Johto": {2, 5, 8}, "Hoenn": {3, 6, 9}}
FORM_GEN = {"isAlolanForm": 7, "isGalarianForm": 8, "isHisuianForm": 8, "isPaldeanForm": 9}
STARTERS = {f"SPECIES_{n}" for n in (
    "BULBASAUR CHARMANDER SQUIRTLE CHIKORITA CYNDAQUIL TOTODILE TREECKO TORCHIC MUDKIP TURTWIG CHIMCHAR "
    "PIPLUP SNIVY TEPIG OSHAWOTT CHESPIN FENNEKIN FROAKIE ROWLET LITTEN POPPLIO GROOKEY SCORBUNNY SOBBLE "
    "SPRIGATITO FUECOCO QUAXLY PIKACHU EEVEE").split()}
# Pseudo-legendary lines only replace each other.
PSEUDO = {f"SPECIES_{n}" for n in "DRATINI LARVITAR BAGON BELDUM GIBLE DEINO GOOMY JANGMO_O DREEPY FRIGIBAX".split()}
EXCLUDE = ("isLegendary", "isSubLegendary", "isRestrictedLegendary", "isMythical", "isUltraBeast",
           "isParadox", "isMegaEvolution", "isGigantamax", "isTotem", "isPrimalReversion",
           "isUltraBurst", "isTeraForm")


def load_species():
    species = {}
    for gen in range(1, 10):
        text = open(os.path.join(ROOT, f"src/data/pokemon/species_info/gen_{gen}_families.h")).read()
        for m in re.finditer(r"^    \[(SPECIES_\w+)\]\s*=\s*\{(.*?)^    \},", text, re.M | re.S):
            name, body = m.group(1), m.group(2)
            stats = [int(x) for x in re.findall(r"\.base(?:HP|Attack|Defense|Speed|SpAttack|SpDefense)\s*=\s*(\d+)", body)[:6]]
            types = (re.findall(r"\.types\s*=\s*MON_TYPES\(([^)]*)\)", body) or [None])[-1]
            flags = set(re.findall(r"\.(is\w+)\s*=\s*TRUE", body))
            evos = re.findall(r"\{\s*EVO_\w+\s*,\s*[^,{}]+,\s*(SPECIES_\w+)", body)
            g = next((FORM_GEN[f] for f in FORM_GEN if f in flags), gen)
            dex = re.search(r"\.natDexNum\s*=\s*(NATIONAL_DEX_\w+)", body)
            species[name] = {
                "dex": dex.group(1) if dex else None,
                "gen": g,
                "bst": sum(stats),
                "types": [t.strip() for t in types.split(",")] if types else [],
                "flags": flags,
                "evos": [e for e in evos if e != name],
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

    # Count which off-region families appear where, most common first.
    wanted = collections.defaultdict(collections.Counter)
    for enc in headers["encounters"]:
        region = regions.get(enc.get("map"))
        if not region:
            continue
        for field in enc.values():
            if isinstance(field, dict) and "mons" in field:
                for mon in field["mons"]:
                    s = mon["species"]
                    if s in species and species[s]["gen"] not in REGION_GENS[region]:
                        wanted[region][base_of[s]] += 1

    swaps = {}
    report = ["# Wild Pokémon swaps", "",
              "Generated by `hack_scripts/regionalize_wild_encounters.py`: off-region families in each",
              "region's wild encounters and the on-region family that replaces them. Edit the script",
              "(or the JSON afterwards) to change a choice.", ""]
    for region in ("Kanto", "Johto", "Hoenn"):
        gens = REGION_GENS[region]
        pool = [b for b in lines if b in species and b not in STARTERS and species[b]["gen"] in gens and is_candidate(b, species[b])
                and all(is_candidate(s, species[s]) for st in lines[b].values() for s in st)]
        used = collections.Counter()
        swaps[region] = {}
        report += [f"## {region} (Gen {', '.join(map(str, sorted(gens)))})", "", "| Was | Now |", "|---|---|"]
        for base, _ in wanted[region].most_common():
            length = len(lines[base])
            final = lines[base][length - 1][0]
            types = set(species[base]["types"])

            def score(cand):
                clen = len(lines[cand])
                cfinal = lines[cand][clen - 1][0]
                shared = len(types & set(species[cand]["types"]))
                primary = bool(types) and species[cand]["types"][0] == species[base]["types"][0]
                return (-shared, used[cand], -primary, -(clen == length),
                        abs(species[cfinal]["bst"] - species[final]["bst"]), cand)

            options = [c for c in pool if (c in PSEUDO) == (base in PSEUDO)] or pool
            choice = min(options, key=score)
            used[choice] += 1
            for stage, members in lines[base].items():
                target_stage = min(stage, len(lines[choice]) - 1)
                for i, s in enumerate(members):
                    options = lines[choice][target_stage]
                    swaps[region][s] = options[i % len(options)]
            report.append(f"| {base[8:].title()} line | {choice[8:].title()} line |")
        report.append("")

    changed = 0
    for enc in headers["encounters"]:
        region = regions.get(enc.get("map"))
        if not region:
            continue
        for field in enc.values():
            if isinstance(field, dict) and "mons" in field:
                for mon in field["mons"]:
                    new = swaps[region].get(mon["species"])
                    if new and new != mon["species"]:
                        mon["species"] = new
                        changed += 1

    print(f"{changed} encounter slots changed; "
          + ", ".join(f"{r}: {len(wanted[r])} families swapped" for r in ("Kanto", "Johto", "Hoenn")))
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
