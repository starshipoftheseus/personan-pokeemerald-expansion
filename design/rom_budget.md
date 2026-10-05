# ROM budget

Hard limit: 32 MB (33,554,432 bytes), set by the GBA's cartridge address space. Emulators have the same limit.
Measured from the unmodified Heart & Soul 2.0.6 build (`make hns`) on 2026-10-05: 31.71 MB used, about 1.85 MB free.
After resampling cries to 10,512 Hz: 30.36 MB used, about 3.19 MB free.
After adding Hoenn (maps 0.97 MB, trainers 0.31 MB): 31.65 MB used, about 1.9 MB free.
After cutting surf sprites: 29.62 MB used, about 3.9 MB free.
After adding FireRed Kanto (1.7 MB) and shrinking the empty trainer slide table (0.36 MB): 30.97 MB used, about 2.6 MB free.
Re-measure after each big change: `make hns` prints `ROM: ... %` at the end of the build.

## What fills the ROM

| MB | What | Notes |
|---:|---|---|
| 7.98 | Pokémon cries | 1,058 cries for Gen 1–9. Biggest single item. |
| 1.95 | Music instrument samples | Shared by all songs. |
| 1.41 | Song and sound-effect sequences | 398 songs: HGSS-style (176), FRLG (75), Hoenn and others. |
| 1.99 | Surf sprites (`src/surfable.o`) | HnS feature: when surfing, the player rides their own Pokémon. ~190 species × normal + shiny + palette. |
| 1.89 | Overworld sprites | NPCs plus HnS overworld Pokémon (followers, visible encounters). |
| 1.39 | Pokémon front sprites | |
| 1.31 | Pokémon menu icons | |
| 0.79 | Pokémon back sprites | |
| 0.42 | Species data table | Stats, types, abilities etc. for every species. |
| 1.73 | Tilesets | Johto + HnS Kanto (+ shared). |
| 1.29 | Maps, map events | Johto + HnS Kanto. |
| 1.03 | Battle engine | Needed. |
| 0.43 | Fonts | Includes Japanese glyph sets (~0.1 MB) the English game never shows. |
| ~6 | Everything else | Engine code, text, items, moves, trainers, menus. |

### Optional features (code + data)

| MB | Feature | Used in this game? |
|---:|---|---|
| 0.51 | Link cable, Union Room, e-Reader, Mystery Gift, Berry Crush, Pokémon Jump, Dodrio Berry Picking, record mixing, Colosseum multiboot | No on emulators. Link trades/battles need a second player and link emulation. |
| 0.31 | Battle Frontier, Battle Tower, Trainer Hill | Hoenn post-game. Keep, cut, or replace later. |
| 0.29 | Bard, Lilycove, TV shows, Dewford trends, easy-chat | Hoenn flavour features. |
| 0.12 | Contests | Hoenn. |
| 0.08 | PokéNav, Match Call | Hoenn. |
| 0.04 | Secret Bases, decorations | Hoenn. |

## Space needed for the plan

| MB | Change |
|---:|---|
| +1.6 | Hoenn maps, tilesets, events (measured from the Emerald build) |
| +~1.5 | FireRed Kanto maps (estimate: similar to Hoenn; FRLG tilesets may already be partly in HnS) |
| −? | Remove HnS's own Kanto maps (measure when removed) |
| +? | Hoenn scripts, text and trainers |

Expected shortfall: roughly 1–1.5 MB, possibly more once scripts and text are counted.

## Cut options (no species removed)

| Saves | Option | What you lose |
|---:|---|---|
| ~1.0 | Surf sprites: drop shiny variants | Shiny Pokémon surf with normal colours. |
| **2.02 (done)** | Surf sprites removed (`OW_SURF_ON_PARTY_MON` FALSE) | Player surfs on the standard blob instead of their Pokémon. |
| **1.34 (done)** | Cries resampled to 10,512 Hz (`CRY_SAMPLE_RATE` in `audio_rules.mk`) | Gen 4+ cries drop to the original Gen 3 cry quality. |
| 2.92 total | Cries at 8,000 Hz instead | Noticeably muffled. Measured; not chosen. |
| ~0.5 | Link / multiplayer features | Link trades and battles, Mystery Gift (no use on emulators). |
| **0.36 (done)** | Empty trainer slide table (`sTrainerSlides`) | Nothing: Heart & Soul defines no trainer slides, but the table takes 3 difficulties x every trainer. |
| ~0.1 | Japanese font glyphs | Nothing visible in an English game. Needs care: the code expects the tables to exist. |
| 0.3 | Battle Frontier etc. | Hoenn post-game facilities. |

Nothing here is decided yet. Pick cuts as the regions go in and the real numbers come in.
