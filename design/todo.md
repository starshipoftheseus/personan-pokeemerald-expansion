# Task list
Small, specific tasks for Claude. One per request.

## Base switched to Heart & Soul 2.0.6
The earlier Emerald + FireRed-Kanto flag work (hack_scripts/gen_kanto_constants.py) is in git history
(commit 6c9cd023). The same method applies to separating Hoenn's flags from HnS's.

- [ ] Confirm `make hns` builds from this repo and the ROM plays
- [ ] Decide which Kanto: HnS's GSC-style Kanto (`_hns`, already wired into the story) or FireRed's full Kanto (`_Frlg`, bigger)
- [ ] Decide the Pokémon list (frees ROM space; cries are ~10 MB)
- [ ] Hoenn: map filtering. `tools/mapjson/mapjson.cpp` keeps only maps whose `game_version` matches the build. Include Hoenn (emerald) maps in the `hns` build.
- [ ] Hoenn: flags/vars. Separate Hoenn's story flags/vars from HnS's (adapt the generator)
- [ ] Hoenn: trainers, scripts and engine code that HnS changed or removed
- [ ] Per region: own badges, Elite Four, Champion, Day Care; end game after all three Champions
- [ ] First milestone: warp from Johto to Littleroot Town in one ROM
