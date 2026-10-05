#!/usr/bin/env python3
"""Generate FireRed Kanto's constants for the combined build (MAPS_FIRERED with Heart & Soul + Hoenn).

FireRed's flag header reuses most of Emerald's and Heart & Soul's flag names for its own flags, and
FireRed's scripts reuse 100+ script labels that Heart & Soul's Kanto copied. So FireRed gets a
"context": inside FireRed's scripts and FireRed maps' event data, every FireRed flag name and every
clashing label is redirected. Everywhere else the names keep their usual meaning.

  include/constants/frlg_flags.h, frlg_vars.h, frlg_trainers.h  (end of flags.h, vars.h, opponents.h)
      FRLG_FLAGS_START: a copy of FireRed's flag layout above Hoenn's flags; FLAG_FRLG_BADGE0x_GET etc.
      FireRed-only vars moved from 0x40xx to 0x42xx (stored in SaveBlock2, see GetVarPointer).
      FireRed trainers numbered after Hoenn's (FRLG_TRAINERS_START + FireRed id).
  include/constants/frlg_context.h / frlg_context_end.h  (around FireRed scripts and map data)
      FireRed flag names -> FRLG_FLAGS_START + FireRed value; clashing labels -> <label>_Frlg.

Run after changing flag/var/trainer headers or FireRed scripts:
    python3 hack_scripts/gen_frlg_constants.py
"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from region_constants import names_in, evaluate, ROOT
from script_sections import sections

OUT_FLAGS = os.path.join(ROOT, "include/constants/frlg_flags.h")
OUT_VARS = os.path.join(ROOT, "include/constants/frlg_vars.h")
OUT_TRAINERS = os.path.join(ROOT, "include/constants/frlg_trainers.h")
OUT_CONTEXT = os.path.join(ROOT, "include/constants/frlg_context.h")
OUT_CONTEXT_END = os.path.join(ROOT, "include/constants/frlg_context_end.h")

VAR_OFFSET = 0x200
FIRST_MOVABLE_VAR = 0x4020

# Engine flags every region shares: FireRed's scripts keep using the common flag for these.
SHARED_ENGINE_FLAGS = {
    "FLAG_SYS_POKEMON_GET", "FLAG_SYS_POKEDEX_GET", "FLAG_SYS_NATIONAL_DEX", "FLAG_SYS_B_DASH",
    "FLAG_SYS_SAFARI_MODE", "FLAG_SYS_ENC_UP_ITEM", "FLAG_SYS_ENC_DOWN_ITEM", "FLAG_SYS_USE_STRENGTH",
    "FLAG_SYS_USE_FLASH", "FLAG_SYS_CTRL_OBJ_DELETE", "FLAG_SYS_RIBBON_GET", "FLAG_SYS_RESET_RTC_ENABLE",
    "FLAG_SYS_MYSTERY_GIFT_ENABLE", "FLAG_SYS_MYSTERY_EVENT_ENABLE", "FLAG_SYS_CLOCK_SET",
    "FLAG_NURSE_UNION_ROOM_REMINDER", "FLAG_SHOWN_BOX_WAS_FULL_MESSAGE",
}

# FireRed flags C code needs by name (badges for field moves/obedience, counted in menus).
C_COPIES = [f"FLAG_BADGE0{i}_GET" for i in range(1, 9)] + [
    # FireRed's HM gifts: HM01 Cut, 02 Fly, 03 Surf, 04 Strength, 05 Flash, 06 Rock Smash, 07 Waterfall
    "FLAG_GOT_HM01", "FLAG_GOT_HM02", "FLAG_GOT_HM03", "FLAG_GOT_HM04", "FLAG_GOT_HM05", "FLAG_GOT_HM06",
    "FLAG_HIDE_FOUR_ISLAND_ICEFALL_CAVE_1F_HM07",  # HM07 Waterfall is an item ball; set once it is picked up
    "FLAG_SYS_GAME_CLEAR", "FLAG_IS_CHAMPION",
]


def is_range_macro(name):
    return name.endswith(("_START", "_END", "_COUNT")) or name.startswith("NUM_")


def label_defs(path):
    try:
        text = open(os.path.join(ROOT, path), errors="ignore").read()
    except FileNotFoundError:
        return set()
    return set(re.findall(r"^([A-Za-z_]\w*)::?", text, re.M))


def main():
    # --- flags
    flag_names = sorted(set(names_in("include/constants/flags_frlg.h")) | set(names_in("include/constants/flags.h"))
                        | set(names_in("include/constants/flags_hns.h")))
    fr = evaluate("FIRERED", flag_names, ["flags.h"])
    merged = evaluate("POKEMON_HNS", flag_names, ["flags.h"], ["MAPS_HNS", "MAPS_EMERALD"])
    frlg_count = fr["FLAGS_COUNT"]
    start = (merged["FLAGS_COUNT"] + 7) // 8 * 8
    frlg_only_names = set(names_in("include/constants/flags_frlg.h"))
    context_flags = {}
    for name in sorted(frlg_only_names):
        v = fr.get(name, 0)
        if not name.startswith("FLAG_") or is_range_macro(name) or v < 0x20 or v >= frlg_count:
            continue
        if name in SHARED_ENGINE_FLAGS:
            continue
        context_flags[name] = v

    # --- vars
    frlg_vars = [n for n in names_in("include/constants/vars_frlg.h") if n.startswith("VAR_")]
    other_vars = set(names_in("include/constants/vars.h")) | set(names_in("include/constants/vars_hns.h"))
    fv = evaluate("FIRERED", frlg_vars, ["vars.h"])
    moved_vars = {n: v for n, v in fv.items() if n not in other_vars and FIRST_MOVABLE_VAR <= v <= 0x40FF}
    shared_vars_differ = sorted(n for n in frlg_vars if n in other_vars and n in fv
                                and fv[n] != evaluate("POKEMON_HNS", [n], ["vars.h"]).get(n))

    # --- trainers
    opp = open(os.path.join(ROOT, "include/constants/opponents_frlg.h")).read()
    trainers = [(n, int(v)) for n, v in re.findall(r"#define\s+(TRAINER_\w+)\s+(\d+)\b", opp) if n != "TRAINER_NONE"]

    # --- labels FireRed's scripts define that something else also defines
    files, _ = sections()
    frlg_labels, other_labels = set(), set()
    for p in files["frlg"]:
        frlg_labels |= label_defs(p)
    for sec in ("hoenn_maps", "common", "hns"):
        for p in files[sec]:
            other_labels |= label_defs(p)
    other_labels |= set(re.findall(r"^([A-Za-z_]\w*)::?", open(os.path.join(ROOT, "data/event_scripts.s")).read(), re.M))
    clashing_labels = sorted(frlg_labels & other_labels)

    header = ["// Generated by hack_scripts/gen_frlg_constants.py. Do not edit by hand."]
    def write(path, guard, title, body):
        open(path, "w").write("\n".join(header + [title, f"#ifndef {guard}", f"#define {guard}", ""] + body
                                         + ["", f"#endif // {guard}", ""]))

    body = [
        "// A copy of FireRed's flag layout, above Hoenn's flags. Inside FireRed's scripts every FireRed",
        "// flag name points here (frlg_context.h).",
        f"#define FRLG_FLAGS_START              0x{start:X}",
        f"#define FRLG_FLAGS_COUNT              0x{frlg_count:X}",
        "#define FRLG_FLAGS_END                (FRLG_FLAGS_START + FRLG_FLAGS_COUNT - 1)",
        f"#define FRLG_TRAINER_FLAGS_START      (FRLG_FLAGS_START + 0x{fr['TRAINER_FLAGS_START']:X})",
        f"#define FRLG_DAILY_FLAGS_START        (FRLG_FLAGS_START + 0x{fr['DAILY_FLAGS_START']:X})",
        f"#define FRLG_DAILY_FLAGS_END          (FRLG_FLAGS_START + 0x{fr['DAILY_FLAGS_END']:X})",
        "",
        "// FireRed's copy of flags C code reads by name",
    ]
    for name in C_COPIES:
        if fr.get(name, 0) == 0:
            raise SystemExit(f"{name} is not a real FireRed flag")
        body.append(f"#define FLAG_FRLG_{name[len('FLAG_'):]} (FRLG_FLAGS_START + 0x{fr[name]:X})")
    body += ["", "#undef FLAGS_COUNT", "#define FLAGS_COUNT (FRLG_FLAGS_END + 1)"]
    write(OUT_FLAGS, "GUARD_CONSTANTS_FRLG_FLAGS_H", "// FireRed Kanto's flags in the combined build.", body)

    body = ["// FireRed-only vars: FireRed's number + 0x200, kept in SaveBlock2 (see GetVarPointer).",
            f"#define FRLG_VARS_START               0x{FIRST_MOVABLE_VAR + VAR_OFFSET:X}",
            f"#define FRLG_VARS_END                 0x{0x40FF + VAR_OFFSET:X}",
            "#define FRLG_VARS_COUNT               (FRLG_VARS_END - FRLG_VARS_START + 1)", ""]
    for name in sorted(moved_vars, key=lambda n: (moved_vars[n], n)):
        body += [f"#undef {name}", f"#define {name} 0x{moved_vars[name] + VAR_OFFSET:X}"]
    write(OUT_VARS, "GUARD_CONSTANTS_FRLG_VARS_H", "// FireRed Kanto's vars in the combined build.", body)

    body = ["// FireRed trainers, numbered after Hoenn's.",
            "#define FRLG_TRAINERS_START           (HOENN_TRAINERS_START + TRAINERS_COUNT_EMERALD)", ""]
    for name, value in trainers:
        body += [f"#undef {name}", f"#define {name} (FRLG_TRAINERS_START + {value})"]
    body += ["", "#undef TRAINERS_COUNT", "#define TRAINERS_COUNT (FRLG_TRAINERS_START + TRAINERS_COUNT_FRLG)",
             "#undef MAX_TRAINERS_COUNT", "#define MAX_TRAINERS_COUNT TRAINERS_COUNT"]
    write(OUT_TRAINERS, "GUARD_CONSTANTS_FRLG_TRAINERS_H", "// FireRed Kanto's trainers in the combined build.", body)

    begin = header + ["// Included before FireRed's scripts and map data; frlg_context_end.h restores. No include guard."]
    end = header + ["// Restores the names frlg_context.h redirected."]
    for name in sorted(context_flags):
        begin += [f'#pragma push_macro("{name}")', f"#undef {name}",
                  f"#define {name} (FRLG_FLAGS_START + 0x{context_flags[name]:X})"]
        end.append(f'#pragma pop_macro("{name}")')
    for label in clashing_labels:
        begin += [f'#pragma push_macro("{label}")', f"#undef {label}", f"#define {label} {label}_Frlg"]
        end.append(f'#pragma pop_macro("{label}")')
    open(OUT_CONTEXT, "w").write("\n".join(begin) + "\n")
    open(OUT_CONTEXT_END, "w").write("\n".join(end) + "\n")

    print(f"FireRed flags 0x{start:X}-0x{start + frlg_count - 1:X} ({len(context_flags)} names in context), "
          f"{len(moved_vars)} vars to 0x42xx, {len(trainers)} trainers, {len(clashing_labels)} clashing labels")
    if shared_vars_differ:
        print("WARNING: FireRed vars sharing a name but not a value with other regions:", shared_vars_differ)


if __name__ == "__main__":
    main()
