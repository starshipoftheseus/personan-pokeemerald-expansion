#!/usr/bin/env python3
"""Give regular trainers Pokémon from their region's generations (design/balance.md):

    Kanto (FireRed and Heart & Soul's Kanto): Gen 1, 4, 7
    Johto:                                   Gen 2, 5, 8
    Hoenn:                                   Gen 3, 6, 9

A trainer's region is the region of the map whose script battles them; trainers no map refers
to use their file's region (trainers.party Hoenn, trainers_frlg.party Kanto, trainers_hns.party
Johto). Off-region Pokémon are swapped family for family (same stage, shared types, similar stats,
the same swap everywhere in the region). A swapped Pokémon loses its listed moves and ability, so it
gets its new species' level-up moves; its item, level and IVs stay.

Bosses keep their hand-picked teams: gym leaders, Elite Four, champions, rivals and villain
leaders/admins (their regional teams are designed by hand, see design/balance.md).
The swaps made are listed in design/trainer_species_swaps.md. Re-running is safe.

    python3 hack_scripts/regionalize_trainers.py [--dry-run]
"""
import argparse, collections, glob, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from regionalize_wild_encounters import (ROOT, REGION_GENS, STARTERS, PSEUDO, load_species,
                                         mark_default_forms, is_candidate, families, map_regions)

PARTY_FILES = {"src/data/trainers.party": "Hoenn", "src/data/trainers_frlg.party": "Kanto",
               "src/data/trainers_hns.party": "Johto"}
BOSS_CLASS = re.compile(r"Leader|Elite|Champion|Rival|Boss|Admin|Executive", re.I)
REPORT = os.path.join(ROOT, "design/trainer_species_swaps.md")
FIELD = re.compile(r"^(Level|IVs|EVs|Ability|Nature|Happiness|Shiny|Ball|Tera Type|Dynamax Level|Gigantamax|Gender|Friendship)\s*:", re.I)


def species_constant(name):
    """A display name as trainerproc turns it into a constant (Mr. Mime -> SPECIES_MR_MIME)."""
    if name.startswith("SPECIES_"):
        return name
    out = "".join(c.upper() if c.isalnum() else ("" if c == "'" else "_") for c in name)
    out = re.sub("_+", "_", out).strip("_")
    return "SPECIES_" + out.replace("♀", "F").replace("♂", "M")


def trainer_regions(regions):
    found = {}
    for path in glob.glob(os.path.join(ROOT, "data/maps/*/scripts.*")):
        map_json = os.path.join(os.path.dirname(path), "map.json")
        if not os.path.exists(map_json):
            continue
        map_id = re.search(r'"id":\s*"(MAP_\w+)"', open(map_json).read()).group(1)
        region = regions.get(map_id)
        if not region:
            continue
        for t in re.findall(r"\b(TRAINER_\w+)", open(path, errors="ignore").read()):
            found.setdefault(t, region)
    return found


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    species = load_species()
    mark_default_forms(species)
    base_of, stage_of, lines = families(species)
    by_trainer = trainer_regions(map_regions())

    pools = {}
    for region, gens in REGION_GENS.items():
        pools[region] = [b for b in lines if b in species and species[b]["gen"] in gens and b not in STARTERS
                         and is_candidate(b, species[b])
                         and all(is_candidate(x, species[x]) for st in lines[b].values() for x in st)]
    family_swap = {r: {} for r in REGION_GENS}
    used = {r: collections.Counter() for r in REGION_GENS}

    def swap_family(region, base):
        if base not in family_swap[region]:
            types = set(species[base]["types"])
            length = len(lines[base])
            final = lines[base][length - 1][0]

            def score(c):
                clen = len(lines[c])
                return (-len(types & set(species[c]["types"])), used[region][c],
                        -(bool(types) and species[c]["types"][0] == species[base]["types"][0]),
                        -(clen == length),
                        abs(species[lines[c][clen - 1][0]]["bst"] - species[final]["bst"]), c)

            options = [c for c in pools[region] if (c in PSEUDO) == (base in PSEUDO)] or pools[region]
            family_swap[region][base] = min(options, key=score)
            used[region][family_swap[region][base]] += 1
        return family_swap[region][base]

    def swap(region, s):
        choice = swap_family(region, base_of[s])
        stage = min(stage_of[s], len(lines[choice]) - 1)
        members = lines[choice][stage]
        return members[lines[base_of[s]][stage_of[s]].index(s) % len(members)] if s in lines[base_of[s]][stage_of[s]] else members[0]

    total = 0
    for rel, default_region in PARTY_FILES.items():
        path = os.path.join(ROOT, rel)
        out, changed = [], 0
        trainer, region, boss, in_header, drop = None, None, False, False, False
        for line in open(path).read().split("\n"):
            m = re.match(r"^=== (TRAINER_\w+) ===", line)
            if m:
                trainer = m.group(1)
                region = by_trainer.get(trainer, default_region)
                boss, in_header, drop = False, True, False
                out.append(line)
                continue
            if trainer is None:
                out.append(line)
                continue
            if in_header:
                if line.startswith("Class:") and BOSS_CLASS.search(line):
                    boss = True
                if not line.strip():
                    in_header = False
                out.append(line)
                continue
            if not line.strip():
                drop = False
                out.append(line)
                continue
            if drop and (line.lstrip().startswith("-") or line.lower().startswith("ability:")):
                continue  # the old species' moves and ability
            if line.lstrip().startswith("-") or FIELD.match(line):
                out.append(line)
                continue
            # First line of a Pokémon: "[Nickname (]Species[)] [(M/F)] [@ Item]"
            head, sep, item = line.partition(" @ ")
            nick = re.match(r"^(.*?)\s*\(([^()]+)\)\s*(\((?:M|F)\))?\s*$", head)
            name = nick.group(2) if nick and nick.group(2) not in ("M", "F") else re.sub(r"\s*\((?:M|F)\)\s*$", "", head).strip()
            const = species_constant(name)
            if not boss and const in species and species[const]["gen"] not in REGION_GENS[region]:
                new = swap(region, const)
                line = new + (sep + item if sep else "")
                drop = True
                changed += 1
            out.append(line)
        total += changed
        print(f"{rel}: {changed} Pokémon swapped")
        if not args.dry_run and changed:
            open(path, "w").write("\n".join(out))

    report = ["# Trainer Pokémon swaps", "",
              "Generated by `hack_scripts/regionalize_trainers.py`: regular trainers' off-region families and",
              "their on-region replacements. Bosses keep their teams.", ""]
    for region in ("Kanto", "Johto", "Hoenn"):
        report += [f"## {region}", "", "| Was | Now |", "|---|---|"]
        report += [f"| {b[8:].title()} line | {c[8:].title()} line |" for b, c in sorted(family_swap[region].items())]
        report.append("")
    if args.dry_run:
        print("\n".join(report[:40]))
    elif total:
        open(REPORT, "w").write("\n".join(report))


if __name__ == "__main__":
    main()
