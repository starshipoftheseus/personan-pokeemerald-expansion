# Task list
Small, specific tasks for Claude. One per request.

## Done
- [x] Cloud build (`make hns`), SessionStart hook installs the toolchain and sox
- [x] Cries resampled to 10,512 Hz (design/rom_budget.md)
- [x] Base switched to Heart & Soul 2.0.6
- [x] Hoenn maps, layouts, tilesets and wild encounters built into the hns ROM (`MAP_VERSION := hns+emerald`)
- [x] Hoenn flags (1290) and vars (174) moved clear of Heart & Soul's; vars live in SaveBlock2 (`hack_scripts/gen_hoenn_constants.py`)
- [x] Hoenn trainers (854) numbered after Heart & Soul's; trainer-defeated flags via `TRAINER_FLAG()`
- [x] Hoenn map sections are real (names, met location); `MAPSEC_NONE` = 220
- [x] Region-specific flags inside Hoenn's scripts: badges, champion, game clear, adventure started, bike/HM/PokéNav/shoes gifts, fossil, safari, loto, Sudowoodo
- [x] Field moves and obedience accept either region's badges; save/continue screens count Hoenn badges
- [x] Headless smoke test (`hack_scripts/smoke_test.py`): 516/518 Hoenn maps and 558/560 Johto maps load and run

## Hoenn: still to do
- [ ] Travel link Johto <-> Hoenn (e.g. a ship between Olivine and Slateport/Lilycove). Right now Hoenn is only reachable with the debug menu warp.
- [ ] Hoenn's start: Hoenn's story expects a new trainer arriving by truck (Littleroot intro, Birch, starter). Decide how a player who arrives from Johto starts Hoenn's story.
- [x] Day Cares: one per region (GetActiveDaycare); mons in other regions' Day Cares keep making Eggs. FireRed's single-mon Route 5 Day Care is still FireRed-build-only.
- [ ] Rematches: Heart & Soul reuses the REMATCH_* table for its own trainers, so Hoenn's VS Seeker/Match Call rematches are off.
- [x] End game after all three champions: each Hall of Fame sets its region's game-clear flag; FLAG_SYS_GAME_CLEAR needs all three. Continue warp goes to that region's hometown.
- [ ] Trainer card shows 16 badges (Johto + Kanto); Hoenn's 8 are not shown yet.
- [ ] Town Map / Fly in Hoenn shows the Johto map; switch to Emerald's Hoenn region map when in Hoenn.
- [ ] Level caps, prize money and the catch malus count only Johto's 8 badges (gBadgeFlags). Open-world design decision.
- [ ] Hoenn and Johto share some story-gift flags where that seemed harmless (TM Attract/Torment gifts, running shoes effect, Pokédex). Revisit if it matters.

## FireRed Kanto (first era)
- [x] Built in (`MAP_VERSION := hns+emerald+firered`): FireRed context (`frlg_context.h`) for its flags and 146 clashing labels, vars in SaveBlock2, trainers after Hoenn's
- [x] Save space: dex/roamer padding removed and wireless trainer-name records cut to 1 in the combined build. SaveBlock1 15644/15872, SaveBlock2 3756/3968
- [x] Map sections: 31 own values, 31 share a name (`frlg_alias`); MAPSEC_NONE = 251 (limit 0xFC)
- [x] Field moves, obedience and badge totals count FireRed's badges and HM gifts
- [x] Smoke test 416/417 FireRed maps (Union Room needs a link)
- [ ] Getting there: no link to FireRed Kanto yet (debug warp only). Future Kanto vs. FireRed Kanto via a portal/time travel: to design later.
- [ ] FireRed's own start (Oak's lab, Pallet intro, rival name) and how it relates to the player arriving from another region
- [ ] FireRed-only features compiled for FireRed builds only (Fame Checker UI, Trainer Tower, Sevii pass, help system, teachy TV): check each FireRed script that uses them
- [ ] Trainer card shows neither Hoenn's nor FireRed's badges; region map/Fly shows Johto
- [x] ROM: 30.97 MB, ~2.6 MB free (empty trainer slide table shrunk)

## Your requests: status
| Request | Status |
|---|---|
| Johto, Hoenn and Kanto in one ROM | Done (all three load: smoke test) |
| FireRed Kanto (first era) + Heart & Soul Kanto (second era) | Both in; the switch between eras (portal / time travel) is to design later |
| Open world | Regions are separate maps; travel links between them still to build |
| Every coded Pokémon (Gen 1-9) | Done (as Heart & Soul ships) |
| Separate badges per region | Done (Johto 1-8, HnS Kanto 9-16, Hoenn, FireRed); trainer card shows only the first 16 |
| Separate Elite Four + Champion per region; end game after all three | Done |
| Multiple Day Cares | Done (one per region) |
| Cries at lower quality | Done (10,512 Hz) |
| Surf on generic blob | Done |
| Cloud-only workflow | Done (SessionStart hook, smoke test) |
| Johto source | Heart & Soul 2.0.6 (credit the HnS team) |
