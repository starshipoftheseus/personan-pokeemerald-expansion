# CLAUDE.md — pokeemerald-expansion hack

This is a ROM hack built on Pokémon Heart & Soul 2.0.6 (PokemonHnS-Development/pokehns-expansion), a Johto + Kanto game built on rh-hideout/pokeemerald-expansion 1.15.2 (a C decompilation of Pokémon Emerald for GBA). Goal: add Hoenn so all three regions are in one ROM.

## Read first
- `design/` holds the plan for this hack. Check it before inventing story, names, teams or balance numbers. If it doesn't cover something, ask.
- `docs/` holds the upstream tutorials. Prefer them over guesses about how a system works.

## Build & verify
- Build: `make hns -j$(nproc)` → `pokehns.gba` (plain `make` builds vanilla Emerald maps, not this game). Switching between build targets needs `make clean`. Run it after every change and fix all errors and new warnings before reporting done.
- Tests: `make check -j$(nproc)` runs the battle/engine test suite. Run it after any battle, move, ability or item change.
- Never say a change works unless it built. You can't playtest; tell me exactly what to check in the emulator.
- Smoke test (headless, ~1 s per map): `python3 hack_scripts/smoke_test.py MAP_LITTLEROOT_TOWN ...` or `--all emerald|hns|frlg`. It starts a new game on each map in tools/mgba/mgba-rom-test, runs the overworld for 300 frames and reports `ok` / `moved` / `timeout` (crash or hang). Run it on the maps a change touches. MAP_BATTLE_FRONTIER_BATTLE_PIKE_ROOM_NORMAL(_HNS) and MAP_UNION_ROOM(_HNS) always time out: they need a Frontier challenge / link session.
- I work only in cloud sessions. A SessionStart hook (`.claude/hooks/session-start.sh`) installs the ARM toolchain. After a successful build, send me the ROM zipped (it's over the upload limit unzipped) with SendUserFile so I can playtest on my device. Never commit the ROM.

## Where things live
- Config toggles: `include/config/*.h` (battle gen mechanics, features). Prefer flipping a config over editing engine code.
- Species data: `src/data/pokemon/species_info/`; learnsets: `src/data/pokemon/`
- Trainers: `src/data/trainers.party` (text format)
- Moves / abilities / items: `src/data/moves_info.h`, `src/data/abilities.h`, `src/data/items.h`
- Wild encounters: `src/data/wild_encounters.json`
- Maps & scripts: `data/maps/<Map>/` (Johto/HnS Kanto maps end in `_hns`, FireRed maps in `_Frlg`, Hoenn maps have no suffix; `game_version` in map.json picks which build includes a map) (`map.json`, `scripts.inc` or `scripts.pory`)
- Flags / vars: `include/constants/flags.h`, `include/constants/vars.h`

## Rules
- No Porymap: I'm cloud-only, so you edit maps by hand. Scripts, warps, NPCs/objects, connections and encounters in `map.json` and `scripts.inc` are fine. For new maps, copy an existing map of similar size/type as a template and register it the way upstream does (`data/maps/map_groups.json`, `data/layouts/layouts.json`); check `docs/` first. Hand-drawing tile layouts (`.bin`) is error-prone: reuse existing layouts and describe any layout you'd want drawn instead of guessing.
- New flags/vars: reuse an unused slot (`FLAG_UNUSED_*` / `VAR_UNUSED_*`) and `#define` a descriptive name for it. Never repurpose a flag the game still uses.
- Regions: Johto + second-era Kanto (Heart & Soul, `_hns` maps), Hoenn (Emerald maps, no suffix) and first-era FireRed Kanto (`_Frlg` maps) build into one ROM (`MAP_VERSION := hns+emerald+firered`, `MAPS_<SET>` defines). FireRed's flag names and clashing labels mean FireRed's own inside FireRed's scripts and map data (`frlg_context.h`, from `hack_scripts/gen_frlg_constants.py`; re-run it like the Hoenn generator). Hoenn's flags, vars and trainers are moved clear of Heart & Soul's by `hack_scripts/gen_hoenn_constants.py`; re-run it after changing flag/var/trainer headers or Hoenn scripts, and never edit its generated headers (`include/constants/hoenn_*.h`). Names both regions use for their own story (badges, champion, ...) mean Hoenn's copy inside Hoenn's scripts (`hoenn_script_names.h`, list in the generator).
- New scripts: write Poryscript (`.pory`) if this repo uses it; otherwise follow existing `.inc` style.
- Keep engine changes minimal and isolated so upstream expansion updates still merge. Don't reformat or rename upstream code.
- Don't touch `tools/`, the Makefile or generated files unless asked.
- One task at a time; small diffs. Summarise what you changed and which files.

## Git
- I commit before each task. Don't commit or push unless I ask.
