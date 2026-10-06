#!/usr/bin/env python3
"""Rebuild each region's wild encounters so every route feels its own and every Pokémon of the
region's generations can be caught there (design/balance.md):

    Kanto (FireRed and Heart & Soul's Kanto): Gen 1, 4, 7
    Johto:                                   Gen 2, 5, 8
    Hoenn:                                   Gen 3, 6, 9

Starts from the original tables (ORIGINAL_COMMIT) and:
- gives every outdoor map a day and a night table (a map with one table gets a night copy);
- keeps the region's own Pokémon where the original games put them ("anchors": Sentret stays on
  Route 29), and refills every other slot (grass, surfing, rock smash, fishing; common and rare)
  from the region's generations;
- themes each map: forests lean Bug/Grass, caves Rock/Ground/Ghost, mountains Fire/Rock, icy
  places Ice, the sea Water; each route also gets two signature types of its own, and night
  favours Dark/Ghost/Poison/Psychic/Fairy;
- keeps Unown in their ruins, and puts fossil Pokémon only in rock smash (dug up);
- covers every non-legendary family (babies and unevolved forms included) in at least one slot,
  spreads each family over a few maps, and never repeats a family within one encounter type of a table;
- keeps each slot's levels and shows the family member that fits them (Pidove early, Tranquill
  later); common slots get weaker families, rare slots stronger ones.

Legendaries, Mythicals, Ultra Beasts, Paradox Pokémon and starters are left for events
(design/events.md, design/legendary_events.md). Sinjoh, Alola, Hisui, the Battle Frontier and
LeafGreen's tables (not built) are left alone. The result is summarised in
design/wild_encounters.md. Deterministic: re-running gives the same tables.

    python3 hack_scripts/build_wild_encounters.py
"""
import collections, glob, hashlib, json, os, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from regionalize_wild_encounters import (ROOT, REGION_GENS, STARTERS, PSEUDO, load_species,
                                         mark_default_forms, is_candidate, families, map_regions)

ORIGINAL_COMMIT = "850d27bd6~1"   # wild_encounters.json before any regional changes
ENCOUNTERS = os.path.join(ROOT, "src/data/wild_encounters.json")
REPORT = os.path.join(ROOT, "design/wild_encounters.md")
OUTDOOR = {"MAP_TYPE_ROUTE", "MAP_TYPE_TOWN", "MAP_TYPE_CITY", "MAP_TYPE_OCEAN_ROUTE"}
TIME_WORDS = ("Morning", "Day", "Evening", "Night")
NIGHT_TYPES = {"TYPE_DARK", "TYPE_GHOST", "TYPE_POISON", "TYPE_PSYCHIC", "TYPE_FAIRY"}
DAY_TYPES = {"TYPE_GRASS", "TYPE_NORMAL", "TYPE_FLYING", "TYPE_FIRE", "TYPE_BUG", "TYPE_ELECTRIC"}
ALL_TYPES = ["TYPE_NORMAL", "TYPE_FIGHTING", "TYPE_FLYING", "TYPE_POISON", "TYPE_GROUND", "TYPE_ROCK",
             "TYPE_BUG", "TYPE_GHOST", "TYPE_STEEL", "TYPE_FIRE", "TYPE_WATER", "TYPE_GRASS",
             "TYPE_ELECTRIC", "TYPE_PSYCHIC", "TYPE_ICE", "TYPE_DRAGON", "TYPE_DARK", "TYPE_FAIRY"]
THEMES = [  # (words in the map name, types)
    (("FOREST", "WOODS", "PARK", "GARDEN", "MEADOW", "BUSH"), {"TYPE_BUG", "TYPE_GRASS", "TYPE_FAIRY", "TYPE_POISON"}),
    (("CAVE", "TUNNEL", "MT_", "MOUNT", "ROCK", "PATH", "HOLE", "RUINS", "CHAMBER", "WELL", "DEN"),
     {"TYPE_ROCK", "TYPE_GROUND", "TYPE_STEEL", "TYPE_DARK", "TYPE_GHOST", "TYPE_FIGHTING"}),
    (("CHIMNEY", "EMBER", "VOLCAN", "FIERY", "LAVA", "MAGMA", "BURNED", "CINNABAR"), {"TYPE_FIRE", "TYPE_ROCK", "TYPE_GROUND"}),
    (("ICE", "SNOW", "SEAFOAM", "SHOAL", "FROST"), {"TYPE_ICE", "TYPE_WATER"}),
    (("DESERT", "ROUTE111", "ROUTE113"), {"TYPE_GROUND", "TYPE_ROCK", "TYPE_FIRE", "TYPE_STEEL"}),
    (("TOWER", "PYRE", "MANSION", "LAVENDER", "GRAVE"), {"TYPE_GHOST", "TYPE_PSYCHIC", "TYPE_DARK", "TYPE_POISON"}),
    (("POWER_PLANT", "NEW_MAUVILLE", "SILPH"), {"TYPE_ELECTRIC", "TYPE_STEEL"}),
    (("DRAGON", "VICTORY", "SILVER", "METEOR", "SKY_PILLAR"), {"TYPE_DRAGON", "TYPE_FIGHTING", "TYPE_ROCK"}),
    (("SAFARI", "LAKE", "MARSH", "SWAMP", "ROUTE119", "ROUTE120"), {"TYPE_GRASS", "TYPE_WATER", "TYPE_BUG", "TYPE_POISON"}),
]
# Fossil Pokémon are only dug up (rock smash). Unown stay where they are (ruins and chambers).
FOSSILS = {f"SPECIES_{n}" for n in ("OMANYTE KABUTO AERODACTYL LILEEP ANORITH CRANIDOS SHIELDON TIRTOUGA ARCHEN "
                                    "TYRUNT AMAURA DRACOZOLT ARCTOZOLT DRACOVISH ARCTOVISH").split()}
ALWAYS_KEEP = {"SPECIES_UNOWN"}
MAX_ADDED_SLOTS = 10     # per family (anchors not counted): keeps families from spreading everywhere
MAX_FOSSIL_SLOTS = 3
FIELD_TYPES = {"rock_smash_mons": {"TYPE_ROCK", "TYPE_GROUND", "TYPE_STEEL"}}


def seed(text):
    return int(hashlib.md5(text.encode()).hexdigest()[:8], 16)


def map_types():
    out = {}
    for p in glob.glob(os.path.join(ROOT, "data/maps/*/map.json")):
        d = json.load(open(p))
        out[d["id"]] = d.get("map_type", "")
    return out


def time_of(label):
    return next((t for t in TIME_WORDS if f"_{t}" in label), None)


def main():
    species = load_species()
    mark_default_forms(species)
    base_of, stage_of, lines = families(species)
    regions = map_regions()
    mtypes = map_types()
    data = json.loads(subprocess.run(["git", "show", f"{ORIGINAL_COMMIT}:src/data/wild_encounters.json"],
                                     capture_output=True, text=True, check=True, cwd=ROOT).stdout)
    headers = next(g for g in data["wild_encounter_groups"] if g["label"] == "gWildMonHeaders")
    rates = {f["type"]: f["encounter_rates"] for f in headers["fields"]}

    # --- 1. Night tables for outdoor maps that have one table (LeafGreen's are not built: skip)
    by_shared = collections.defaultdict(list)
    for enc in headers["encounters"]:
        label = enc["base_label"]
        if "LeafGreen" in label:
            continue
        shared = label
        for t in TIME_WORDS:
            shared = shared.replace("_" + t, "")
        by_shared[shared].append(enc)
    added_nights = 0
    for shared, encs in by_shared.items():
        enc = encs[0]
        if (regions.get(enc["map"]) and mtypes.get(enc["map"]) in OUTDOOR
                and not any(time_of(e["base_label"]) == "Night" for e in encs)):
            night = json.loads(json.dumps(next((e for e in encs if time_of(e["base_label"]) in (None, "Day")), enc)))
            night["base_label"] = shared + "_Night"
            night["_copied"] = True
            headers["encounters"].insert(headers["encounters"].index(encs[-1]) + 1, night)
            added_nights += 1

    def pool_for(region):
        gens = REGION_GENS[region]
        return sorted(b for b in lines if b in species and species[b]["gen"] in gens and b not in STARTERS
                      and is_candidate(b, species[b])
                      and all(is_candidate(x, species[x]) for st in lines[b].values() for x in st))

    def member_for_level(fam, level):
        """The family member a wild Pokémon of this level would be."""
        current, best = fam, fam
        for _ in range(3):
            nexts = [t for t in species[current]["evos"] if t in species and base_of.get(t) == fam
                     and is_candidate(t, species[t])]
            if not nexts:
                break
            t = nexts[seed(fam + str(level)) % len(nexts)] if len(nexts) > 1 else nexts[0]
            if level < species[current]["evo_level"].get(t, 36) + 3:
                break
            current = best = t
        return best

    final_bst = {}
    for b in lines:
        st = lines[b]
        final_bst[b] = max(species[m]["bst"] for v in st.values() for m in v if m in species)

    report = ["# Wild encounters", "",
              "Generated by `hack_scripts/build_wild_encounters.py`. Per region: how many families can be caught,",
              "and where each family appears (map, day/night).", ""]
    total_changed = 0
    for region in ("Kanto", "Johto", "Hoenn"):
        gens = REGION_GENS[region]
        pool = pool_for(region)
        pool_set = set(pool)
        bst_rank = {f: i / max(1, len(pool) - 1) for i, f in enumerate(sorted(pool, key=lambda f: final_bst[f]))}
        placements = collections.Counter()
        added = collections.Counter()
        where = collections.defaultdict(set)
        tables = [e for e in headers["encounters"] if regions.get(e.get("map")) == region and "LeafGreen" not in e["base_label"]]
        # Early maps first, so coverage fills from the start of the region.
        def min_level(e):
            lv = [m["min_level"] for f in e.values() if isinstance(f, dict) and "mons" in f for m in f["mons"]]
            return min(lv) if lv else 0
        tables.sort(key=min_level)

        # anchors: on-region species in the original slots
        for enc in tables:
            for name, field in enc.items():
                if isinstance(field, dict) and "mons" in field:
                    for mon in field["mons"]:
                        s = mon["species"]
                        if s in species and species[s]["gen"] in gens and base_of[s] in pool_set:
                            placements[base_of[s]] += 1
                            where[base_of[s]].add(enc["map"])

        for enc in tables:
            label = enc["base_label"]
            night = time_of(label) == "Night"
            upper = enc["map"].upper()
            theme = set()
            for words, types in THEMES:
                if any(w in upper for w in words):
                    theme |= types
            sig = {ALL_TYPES[seed(enc["map"]) % 18], ALL_TYPES[seed(enc["map"] + "x") % 18]}
            for name, field in enc.items():
                if not (isinstance(field, dict) and "mons" in field):
                    continue
                # no family twice in one encounter type (grass, surfing, fishing, rock smash)
                in_table = {base_of[m["species"]] for m in field["mons"] if m["species"] in species}
                field_rates = rates.get(name, [])
                top = max(field_rates) if field_rates else 1
                water_field = name in ("water_mons", "fishing_mons")
                for i, mon in enumerate(field["mons"]):
                    s = mon["species"]
                    anchored = (s in species and species[s]["gen"] in gens and base_of[s] in pool_set) or s in ALWAYS_KEEP
                    if anchored and not (enc.get("_copied") and night and not set(species[s]["types"]) & NIGHT_TYPES):
                        continue
                    slot_rarity = 1 - (field_rates[i] / top if i < len(field_rates) else 0)
                    level = mon["max_level"]

                    def score(f, capped=True):
                        types = set(species[f]["types"])
                        aquatic = "TYPE_WATER" in types and f not in FOSSILS
                        if aquatic != water_field or f in in_table:
                            return None
                        if f in PSEUDO and level < 25:
                            return None
                        if (f in FOSSILS) != (name == "rock_smash_mons") and f in FOSSILS:
                            return None
                        sc = 0.0
                        sc += 3.0 * len(types & theme) + 2.0 * len(types & sig)
                        sc += 1.5 * len(types & FIELD_TYPES.get(name, set()))
                        if name == "rock_smash_mons" and not types & FIELD_TYPES[name] and f not in FOSSILS:
                            return None
                        if f in FOSSILS and added[f] >= MAX_FOSSIL_SLOTS:
                            return None
                        if capped and added[f] >= MAX_ADDED_SLOTS:
                            return None
                        sc += 1.5 * len(types & (NIGHT_TYPES if night else DAY_TYPES))
                        sc -= 4.0 * abs(bst_rank[f] - slot_rarity)
                        sc += 12.0 if placements[f] == 0 else -2.5 * placements[f]
                        if enc["map"] in where[f]:
                            sc -= 3.0
                        return (sc, -seed(f + label + str(i)) % 997)

                    scored = [x for x in ((score(f), f) for f in pool) if x[0] is not None]
                    if not scored:   # every fitting family is at its cap: let them go over it
                        scored = [x for x in ((score(f, False), f) for f in pool) if x[0] is not None]
                    if not scored:
                        continue
                    fam = max(scored)[1]
                    new = member_for_level(fam, level)
                    if mon["species"] != new:
                        total_changed += 1
                    if s in species:
                        in_table.discard(base_of[s])
                    mon["species"] = new
                    in_table.add(fam)
                    placements[fam] += 1
                    added[fam] += 1
                    where[fam].add(enc["map"] + (" (night)" if night else ""))

        missing = [f for f in pool if placements[f] == 0]
        report += [f"## {region} (Gen {', '.join(map(str, sorted(gens)))})", "",
                   f"{len(pool) - len(missing)} of {len(pool)} families catchable."
                   + (f" Not placed: {', '.join(m[8:].title() for m in missing)}." if missing else ""), "",
                   "| Family | Slots | Maps |", "|---|---|---|"]
        for f in pool:
            maps = sorted(where[f])
            report.append(f"| {f[8:].title()} | {placements[f]} | {', '.join(m[4:].title() for m in maps[:6])}"
                          + (f" +{len(maps) - 6}" if len(maps) > 6 else "") + " |")
        report.append("")
        print(f"{region}: {len(pool) - len(missing)}/{len(pool)} families placed")

    for enc in headers["encounters"]:
        enc.pop("_copied", None)
    with open(ENCOUNTERS, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    report.insert(4, f"{added_nights} night tables added; {total_changed} slots changed.\n")
    open(REPORT, "w").write("\n".join(report))
    print(f"{added_nights} night tables added, {total_changed} slots changed")


if __name__ == "__main__":
    main()
