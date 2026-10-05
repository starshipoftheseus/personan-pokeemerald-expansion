# Task list
Small, specific tasks for Claude. One per request.

- [x] Get a clean unmodified build (Emerald and `make firered` both build in the cloud)
- [ ] Change starters to:

## Merge Kanto into the Emerald build (one ROM, both regions)
Upstream expansion already ports all of Kanto (`*_Frlg` maps, tilesets, scripts), but
picks one region per build via `IS_FRLG` (`include/constants/global.h`).
- [ ] Map filtering: `tools/mapjson/mapjson.cpp` drops maps whose `region` doesn't match the build. Include both.
- [ ] Flags/vars: `flags.h` swaps in `flags_frlg.h` and `vars.h` swaps in `vars_frlg.h` under `IS_FRLG`, so both regions reuse the same IDs. Biggest job: give Kanto its own non-overlapping range (check save space for flags/vars first).
- [ ] Other `IS_FRLG` switches: about 207 across ~65 files (trainer tower, event object graphics, field specials, doors, daycare, new game, trainer card...). Decide per site: keep both, Hoenn only, or Kanto only.
- [ ] Save data: `SaveBlock1` adds Kanto-only fields under `IS_FRLG` (rival name, Route 5 daycare, Trainer Tower). Check they fit alongside Hoenn's.
- [ ] Map groups: maps in a Kanto map group can't be warped/connected to from Hoenn ones (see `docs/tutorials/how_to_frlg.md`). Plan the travel link (ship/train) around that.
- [ ] ROM space: each build is ~80% of 32 MB (~6.5 MB free). Rough estimate: Kanto region data is 2–4 MB, so it probably fits but is tight. Measure after the first merge and decide what to trim.
- [ ] First milestone: reach Pallet Town from Hoenn in one ROM (debug-menu warp is fine).
