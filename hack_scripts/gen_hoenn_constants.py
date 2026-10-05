#!/usr/bin/env python3
"""Generate include/constants/hoenn_flags.h and hoenn_vars.h for the Heart & Soul build with Hoenn maps (MAPS_EMERALD).

Heart & Soul stubs Hoenn's flag names to 0 and gives its own vars the same numbers as Hoenn's
(0x4000-0x40FF), because upstream builds only one game at a time. This moves Hoenn's flags and vars
somewhere they don't collide with Johto's:

  flags: HOENN_FLAGS_START + <Emerald value>, a copy of Emerald's whole flag layout above Heart & Soul's
         flags. Hoenn trainer flags land in the same block (HOENN_TRAINER_FLAGS_START).
  vars:  <Emerald value> + 0x100 (0x4120-0x41FF), stored in SaveBlock2 (see GetVarPointer).
  trainers: HOENN_TRAINERS_START + <Emerald id>, right after Heart & Soul's trainers in gTrainers.
            Their defeated flags use Emerald's layout in the Hoenn flag block (TRAINER_FLAG in opponents.h).

A flag is moved when Heart & Soul stubs it (value 0), or when no Heart & Soul map or script uses it and
it isn't one of the engine flags both regions share (KEEP_SHARED_FLAGS). A var is moved when its number
clashes with a Heart & Soul var, or when Hoenn maps use it and Heart & Soul doesn't.

Names both regions use for different things (badges, champion, ...) are NOT handled here; see
design/todo.md. Re-run after changing flag/var headers or Hoenn scripts:
    python3 hack_scripts/gen_hoenn_constants.py
"""
import os, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from region_constants import names_in, evaluate, ROOT
from name_usage import usage_index

OUT_FLAGS = os.path.join(ROOT, "include/constants/hoenn_flags.h")
OUT_VARS = os.path.join(ROOT, "include/constants/hoenn_vars.h")
OUT_TRAINERS = os.path.join(ROOT, "include/constants/hoenn_trainers.h")
OUT_SCRIPT_NAMES = os.path.join(ROOT, "include/constants/hoenn_script_names.h")
OUT_SCRIPT_NAMES_END = os.path.join(ROOT, "include/constants/hoenn_script_names_end.h")
VAR_OFFSET = 0x100
FIRST_MOVABLE_VAR = 0x4020  # 0x4000-0x401F are temp vars and object graphics vars, shared by every map

# Flags both regions use for their own story. Inside Hoenn's scripts these names are redirected to
# FLAG_HOENN_<name> (a copy in the Hoenn flag block); everywhere else they keep Heart & Soul's meaning.
REGION_SPECIFIC_FLAGS = [
    "FLAG_BADGE01_GET", "FLAG_BADGE02_GET", "FLAG_BADGE03_GET", "FLAG_BADGE04_GET",
    "FLAG_BADGE05_GET", "FLAG_BADGE06_GET", "FLAG_BADGE07_GET", "FLAG_BADGE08_GET",
    "FLAG_SYS_GAME_CLEAR", "FLAG_IS_CHAMPION",
    "FLAG_ADVENTURE_STARTED", "FLAG_RECEIVED_RUNNING_SHOES", "FLAG_RECEIVED_POKENAV", "FLAG_RECEIVED_BIKE",
    "FLAG_RECEIVED_HM_CUT", "FLAG_RECEIVED_HM_FLASH", "FLAG_RECEIVED_HM_ROCK_SMASH",
    "FLAG_RECEIVED_HM_STRENGTH", "FLAG_RECEIVED_HM_SURF",
    "FLAG_DEFEATED_SUDOWOODO", "FLAG_RECEIVED_REVIVED_FOSSIL_MON",
    "FLAG_GOOD_LUCK_SAFARI_ZONE", "FLAG_DAILY_PICKED_LOTO_TICKET",
]

# Engine flags both regions share, even when only one side's scripts mention them.
KEEP_SHARED_PREFIXES = ("FLAG_SYS_", "FLAG_DECORATION_", "FLAG_TEMP_")
KEEP_SHARED_FLAGS = {
    "FLAG_HIDDEN_ITEMS_START",
    "FLAG_SHOWN_BOX_WAS_FULL_MESSAGE",
    "FLAG_NURSE_UNION_ROOM_REMINDER",
    "FLAG_POKERUS_EXPLAINED",
    "FLAG_SET_WALL_CLOCK",
}


def is_range_macro(name):
    return name.endswith(("_START", "_END", "_COUNT")) or name.startswith("NUM_")


def flag_moves(em, hn, idx):
    hns_count = hn["FLAGS_COUNT"]
    emerald_count = em["FLAGS_COUNT"]
    moved = {}
    for name, value in em.items():
        if not name.startswith("FLAG_") or is_range_macro(name):
            continue
        if value == 0 or value >= emerald_count:
            continue  # stubs and special (non-saved) flags
        hv = hn.get(name)
        if hv == value:
            continue  # same flag in both builds
        if hv in (None, 0):
            moved[name] = value
            continue
        used_by_hns = "hns" in idx.get(name, ())
        shared = name.startswith(KEEP_SHARED_PREFIXES) or name in KEEP_SHARED_FLAGS
        if not used_by_hns and not shared:
            moved[name] = value
    return moved, hns_count, emerald_count


def var_moves(ev, emerald_names, hns_names, idx):
    em = {n: ev[n] for n in emerald_names if n in ev and n.startswith("VAR_") and 0x4000 <= ev[n] <= 0x40FF}
    hns_unique_values = {ev[n] for n in hns_names if n in ev and n not in em and n.startswith("VAR_")}
    moved = {}
    for name, value in em.items():
        if name in hns_names or value < FIRST_MOVABLE_VAR:
            continue
        uses = idx.get(name, ())
        clash = value in hns_unique_values
        hoenn_only = "hoenn_maps" in uses and "hns" not in uses
        if clash or hoenn_only:
            moved[name] = value
    return moved


def main():
    idx = usage_index()
    flag_names = sorted(set(names_in("include/constants/flags.h")) | set(names_in("include/constants/flags_hns.h")))
    em_flags = evaluate("EMERALD", flag_names, ["flags.h"])
    hn_flags = evaluate("POKEMON_HNS", flag_names, ["flags.h"])
    flags, hns_count, emerald_count = flag_moves(em_flags, hn_flags, idx)

    emerald_var_names = names_in("include/constants/vars.h")
    hns_var_names = set(names_in("include/constants/vars_hns.h"))
    ev = evaluate("POKEMON_HNS", sorted(set(emerald_var_names) | hns_var_names), ["vars.h"])
    var_names = var_moves(ev, emerald_var_names, hns_var_names, idx)

    start = (hns_count + 7) // 8 * 8
    header = ["// Generated by hack_scripts/gen_hoenn_constants.py. Do not edit by hand."]
    lines = header + [
        "// Hoenn's flags, moved clear of Heart & Soul's for the combined build.",
        "#ifndef GUARD_CONSTANTS_HOENN_FLAGS_H",
        "#define GUARD_CONSTANTS_HOENN_FLAGS_H",
        "",
        "// A copy of Emerald's flag layout, above Heart & Soul's flags.",
        f"#define HOENN_FLAGS_START             0x{start:X}",
        f"#define HOENN_FLAGS_COUNT             0x{emerald_count:X}",
        "#define HOENN_FLAGS_END               (HOENN_FLAGS_START + HOENN_FLAGS_COUNT - 1)",
        f"#define HOENN_TRAINER_FLAGS_START     (HOENN_FLAGS_START + 0x{em_flags['TRAINER_FLAGS_START']:X})",
        f"#define HOENN_DAILY_FLAGS_START       (HOENN_FLAGS_START + 0x{em_flags['DAILY_FLAGS_START']:X})",
        f"#define HOENN_DAILY_FLAGS_END         (HOENN_FLAGS_START + 0x{em_flags['DAILY_FLAGS_END']:X})",
        "",
        f"// {len(flags)} flags",
    ]
    for name in sorted(flags, key=lambda n: (flags[n], n)):
        lines += [f"#undef {name}", f"#define {name} (HOENN_FLAGS_START + 0x{flags[name]:X})"]
    lines += ["", "// Hoenn's own copy of flags both regions use (see hoenn_script_names.h)"]
    for name in REGION_SPECIFIC_FLAGS:
        if name in flags or name not in em_flags or em_flags[name] == 0:
            raise SystemExit(f"{name}: expected a shared flag with an Emerald value")
        lines.append(f"#define FLAG_HOENN_{name[len('FLAG_'):]} (HOENN_FLAGS_START + 0x{em_flags[name]:X})")
    lines += ["", "#undef FLAGS_COUNT", "#define FLAGS_COUNT (HOENN_FLAGS_END + 1)", "",
              "#endif // GUARD_CONSTANTS_HOENN_FLAGS_H", ""]
    open(OUT_FLAGS, "w").write("\n".join(lines))

    begin = header + [
        "// Included before Hoenn's scripts in data/event_scripts.s: inside Hoenn's scripts these",
        "// names mean Hoenn's own flag. hoenn_script_names_end.h restores them. No include guard.",
    ]
    end = header + ["// Included after Hoenn's scripts: restores the names hoenn_script_names.h redirected."]
    for name in REGION_SPECIFIC_FLAGS:
        begin += [f'#pragma push_macro("{name}")', f"#undef {name}",
                  f"#define {name} FLAG_HOENN_{name[len('FLAG_'):]}"]
        end.append(f'#pragma pop_macro("{name}")')
    open(OUT_SCRIPT_NAMES, "w").write("\n".join(begin) + "\n")
    open(OUT_SCRIPT_NAMES_END, "w").write("\n".join(end) + "\n")

    lines = header + [
        "// Hoenn's vars, moved clear of Heart & Soul's for the combined build.",
        "#ifndef GUARD_CONSTANTS_HOENN_VARS_H",
        "#define GUARD_CONSTANTS_HOENN_VARS_H",
        "",
        "// Emerald's var number + 0x100, kept in SaveBlock2 (see GetVarPointer).",
        f"#define HOENN_VARS_START              0x{FIRST_MOVABLE_VAR + VAR_OFFSET:X}",
        f"#define HOENN_VARS_END                0x{0x40FF + VAR_OFFSET:X}",
        "#define HOENN_VARS_COUNT              (HOENN_VARS_END - HOENN_VARS_START + 1)",
        "",
        f"// {len(var_names)} vars",
    ]
    for name in sorted(var_names, key=lambda n: (var_names[n], n)):
        lines += [f"#undef {name}", f"#define {name} 0x{var_names[name] + VAR_OFFSET:X}"]
    lines += ["", "#endif // GUARD_CONSTANTS_HOENN_VARS_H", ""]
    open(OUT_VARS, "w").write("\n".join(lines))
    # Trainers: every Emerald trainer constant in opponents.h (TRAINER_NONE stays 0).
    import re
    opp = open(os.path.join(ROOT, "include/constants/opponents.h")).read()
    trainers = [(n, int(v)) for n, v in re.findall(r"#define\s+(TRAINER_\w+)\s+(\d+)\b", opp) if n != "TRAINER_NONE"]
    lines = header + [
        "// Hoenn's trainers, numbered after Heart & Soul's for the combined build.",
        "#ifndef GUARD_CONSTANTS_HOENN_TRAINERS_H",
        "#define GUARD_CONSTANTS_HOENN_TRAINERS_H",
        "",
        "#define HOENN_TRAINERS_START          TRAINERS_COUNT_HNS",
        "",
        f"// {len(trainers)} trainers",
    ]
    for name, value in trainers:
        lines += [f"#undef {name}", f"#define {name} (HOENN_TRAINERS_START + {value})"]
    lines += ["",
              "#undef TRAINERS_COUNT",
              "#define TRAINERS_COUNT                (HOENN_TRAINERS_START + TRAINERS_COUNT_EMERALD)",
              "#undef MAX_TRAINERS_COUNT",
              "#define MAX_TRAINERS_COUNT            TRAINERS_COUNT",
              "",
              "#endif // GUARD_CONSTANTS_HOENN_TRAINERS_H", ""]
    open(OUT_TRAINERS, "w").write("\n".join(lines))
    print(f"hoenn_trainers.h: {len(trainers)} trainers moved after Heart & Soul's")

    print(f"hoenn_flags.h / hoenn_vars.h: {len(flags)} flags moved to 0x{start:X}-0x{start + emerald_count - 1:X}, "
          f"{len(var_names)} vars moved to 0x{FIRST_MOVABLE_VAR + VAR_OFFSET:X}-0x{0x40FF + VAR_OFFSET:X}")


if __name__ == "__main__":
    main()
