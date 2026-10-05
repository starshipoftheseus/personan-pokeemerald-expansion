# Hack overview
- Working title:
- Type: multi-region game across Hoenn, Kanto and Johto (story still being worked out)
- Base: Pokémon Heart & Soul 2.0.6 (Johto + GSC-style Kanto, finished and playtested; open source, credit the HnS team). Plan: add Hoenn back in (its maps are still in the tree, excluded from the `hns` build).
- ROM budget: 32 MB hard limit. HnS uses 29.7 MB; Hoenn region data is ~1.6 MB. Trim Pokémon families / cries to fit.
- Target: (player level, length, difficulty)
- Generation of mechanics: (e.g. Gen 9 battle mechanics, physical/special split, etc.)
- Pokémon available: every species already coded (Gen 1–9, as HnS ships: megas, Gigantamax and Tera forms off). Distribution per region decided later.
- What must NOT change:

## Decisions
- Badges: each region has its own 8 badges (24 total). Badge checks (HMs, obedience) must count per region.
- League: each region has its own Elite Four and Champion. "End game" (FLAG_SYS_GAME_CLEAR, credits, post-game) only after all three Champions are beaten.
- Day Care: one per region, each with its own egg/state.
- Kanto: both. FireRed's Kanto (`_Frlg` maps) is the first era; Heart & Soul's GSC-style Kanto (`_hns` Kanto maps and its post-game) is kept as the second era, after a time jump in the story. The game is meant to be open world.
- Sevii Islands may share map-section names with Kanto areas if needed (u8 map-section limit).
- Surfing on your own Pokémon is cut (`OW_SURF_ON_PARTY_MON` FALSE): the generic surf blob is used.
