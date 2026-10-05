# Task list
Small, specific tasks for Claude. One per request.

- [x] Get a clean unmodified build (Emerald and `make firered` both build in the cloud)
- [ ] Change starters to:

## Merge Kanto into the Emerald build (one ROM, both regions)
Upstream expansion already ports all of Kanto (`*_Frlg` maps, tilesets, scripts), but
picks one region per build via `IS_FRLG` (`include/constants/global.h`).
- [ ] Map filtering: `tools/mapjson/mapjson.cpp` drops maps whose `region` doesn't match the build. Include both.
- [x] Flags/vars (done): `hack_scripts/gen_kanto_constants.py` generates `include/constants/flags_kanto.h` (1352 Kanto-only flags at 0x960-0x125F, same layout as FireRed + 0x960) and `vars_kanto.h` (211 Kanto vars moved to 0x41xx). Re-run it after upstream merges. Was: `flags.h` swaps in `flags_frlg.h` and `vars.h` swaps in `vars_frlg.h` under `IS_FRLG`, so both regions reuse the same IDs. Biggest job: give Kanto its own non-overlapping range (check save space for flags/vars first).
- [ ] Shared flag names (81): names both games use keep their Hoenn value, so Kanto scripts would share them. Fine for engine flags (FLAG_SYS_POKEMON_GET, FLAG_SYS_POKEDEX_GET, FLAG_SYS_NATIONAL_DEX, FLAG_SYS_B_DASH, safari/cruise/repel...). Decided (see overview.md): give Kanto its own FLAG_BADGE01-08_GET, FLAG_IS_CHAMPION and FLAG_PENDING_DAYCARE_EGG; FLAG_SYS_GAME_CLEAR stays shared but is only set after all three Champions.
- [ ] Kanto trainers: Kanto trainer IDs overlap Hoenn's (`opponents.h` switches on IS_FRLG). Kanto trainer flags already have room (FireRed's trainer range is inside the Kanto block) once Kanto trainers get their own IDs.
- [ ] Other `IS_FRLG` switches: about 207 across ~65 files (trainer tower, event object graphics, field specials, doors, daycare, new game, trainer card...). Decide per site: keep both, Hoenn only, or Kanto only.
- [x] Save space check (done): Emerald SaveBlock1 is 15568/15872 bytes (304 free). Merging needs roughly 1 KB more:
  Kanto flags ~288 B, Kanto vars 512 B (vars_frlg.h is a full second 256-var set), extra trainer flags ~80 B
  (855 Hoenn + 624 Kanto trainers > MAX_TRAINERS_COUNT 864), plus Kanto-only fields below.
  Done: in `include/config/save.h` set FREE_MYSTERY_GIFT (876 B) and FREE_MYSTERY_EVENT_BUFFERS (1104 B) to TRUE.
  Both are link/e-Reader features that do nothing on an emulator. That frees ~2 KB, enough with margin. After the flag/var move SaveBlock1 is 14488/15872 bytes (1384 free).
- [ ] Save data: `SaveBlock1` adds Kanto-only fields under `IS_FRLG` (rival name, Route 5 daycare, Trainer Tower). Check they fit alongside Hoenn's.
- [ ] Map groups: maps in a Kanto map group can't be warped/connected to from Hoenn ones (see `docs/tutorials/how_to_frlg.md`). Plan the travel link (ship/train) around that.
- [ ] ROM space: each build is ~80% of 32 MB (~6.5 MB free). Rough estimate: Kanto region data is 2–4 MB, so it probably fits but is tight. Measure after the first merge and decide what to trim.
- [ ] First milestone: reach Pallet Town from Hoenn in one ROM (debug-menu warp is fine).
