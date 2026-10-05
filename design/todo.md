# Task list
Small, specific tasks for Claude. One per request.

## Base switched to Heart & Soul 2.0.6
The earlier Emerald + FireRed-Kanto flag work (hack_scripts/gen_kanto_constants.py) is in git history
(commit 6c9cd023). The same method applies to separating Hoenn's flags from HnS's.

- [ ] Confirm `make hns` builds from this repo and the ROM plays
- [x] Kanto = FireRed's (`_Frlg`). HnS's Kanto maps (`_hns` with REGION_KANTO) come out; check HnS Johto scripts that warp into or reference its Kanto.
- [x] Pokémon: keep every coded species (already the HnS setting).
- [x] ROM inventory: see design/rom_budget.md. ROM budget (measured): HnS ROM 31.7 MB, ~1.85 MB free. Hoenn adds ~1.6 MB (tilesets 0.69, maps 0.69, events/anims 0.2), FireRed Kanto roughly the same, minus HnS Kanto removed. Expect to be ~1–1.5 MB over.
  Candidates to cut (no species lost): `src/surfable.o` 2.0 MB (HnS surf sprites; check what it is), Colosseum multiboot 0.16 MB, bard music 0.17 MB, unused Battle Frontier/Ruby-only content, regional forms if needed.
- [ ] Hoenn: map filtering. `tools/mapjson/mapjson.cpp` keeps only maps whose `game_version` matches the build. Include Hoenn (emerald) maps in the `hns` build.
- [ ] Hoenn: flags/vars. Separate Hoenn's story flags/vars from HnS's (adapt the generator)
- [ ] Hoenn: trainers, scripts and engine code that HnS changed or removed
- [ ] Per region: own badges, Elite Four, Champion, Day Care; end game after all three Champions
- [ ] First milestone: warp from Johto to Littleroot Town in one ROM
