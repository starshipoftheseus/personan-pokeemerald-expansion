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
- [ ] Day Care: Hoenn's Route 117 Day Care and Johto's share one Day Care slot and FLAG_PENDING_DAYCARE_EGG. Separate storage needs ~288 bytes of SaveBlock1 (108 free).
- [ ] Rematches: Heart & Soul reuses the REMATCH_* table for its own trainers, so Hoenn's VS Seeker/Match Call rematches are off.
- [ ] End game after all three champions (decided): FLAG_SYS_GAME_CLEAR is still set by Heart & Soul's Hall of Fame; Hoenn sets FLAG_HOENN_SYS_GAME_CLEAR. Needs a per-region champion check.
- [ ] Trainer card shows 16 badges (Johto + Kanto); Hoenn's 8 are not shown yet.
- [ ] Town Map / Fly in Hoenn shows the Johto map; switch to Emerald's Hoenn region map when in Hoenn.
- [ ] Level caps, prize money and the catch malus count only Johto's 8 badges (gBadgeFlags). Open-world design decision.
- [ ] Hoenn and Johto share some story-gift flags where that seemed harmless (TM Attract/Torment gifts, running shoes effect, Pokédex). Revisit if it matters.

## FireRed Kanto (next)
- [x] Decided: keep both Kantos. FireRed = first era, Heart & Soul's Kanto = second era after a time jump. Both sets of Kanto maps live in the ROM; the two eras need separate flags, badges (FireRed's 8 vs Heart & Soul's Kanto badges 9-16) and a way to switch era.
- [ ] Map sections: only 33 values are left below 0xFD; FireRed adds 62 sections of its own (Sevii Islands, Silph Co., S.S. Anne...). Reuse Heart & Soul's Kanto sections; Sevii may share names (decided).
- [ ] Save space: FireRed flags need ~288 bytes of SaveBlock1 (108 free). Candidates: dex padding (110), roamer padding (84), link-only trainer name records (240).
- [ ] ROM space: FireRed tilesets, scripts, text and trainers are not in the ROM yet; expect 2+ MB, ~1.9 MB free. Surf sprites cut (2.02 MB): ROM 29.62 MB, ~3.9 MB free.
- [ ] Same steps as Hoenn: MAPS_FIRERED in MAP_VERSION, flags/vars/trainers generator, region-specific names, smoke test.
