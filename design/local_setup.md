# Working on this hack on your own computer

Cloud sessions do everything in a fresh Linux container. To work locally instead (with Claude Code
on the desktop app, the CLI, or by hand), set up the same toolchain once.

## 1. Get the code

Repository: `https://github.com/starshipoftheseus/personan-pokeemerald-expansion`
Work branch: `claude/focused-bohr-vobh1a` (everything from the cloud sessions is pushed there).

```
git clone https://github.com/starshipoftheseus/personan-pokeemerald-expansion.git
cd personan-pokeemerald-expansion
git checkout claude/focused-bohr-vobh1a
```

## 2. Install the toolchain

- **Windows**: install WSL (Ubuntu) and do everything below inside WSL, in a folder under your
  Linux home (not `/mnt/c/...`, which is very slow). Porymap and mGBA run on Windows itself and can
  open the files through `\\wsl$\`.
- **macOS / Linux**: follow `INSTALL.md` in the repository (upstream's guide).

Packages (Ubuntu/WSL), as the cloud setup uses (`.claude/hooks/session-start.sh` has the exact list):

```
sudo apt update
sudo apt install build-essential binutils-arm-none-eabi gcc-arm-none-eabi libnewlib-arm-none-eabi \
                 git libpng-dev python3 sox
```

`sox` is needed for the lower-quality cries (`audio_rules.mk`).

## 3. Build and check

```
make hns -j$(nproc)                 # builds pokehns.gba (the combined Johto + Hoenn + FireRed Kanto ROM)
make tools                          # once, if the smoke test can't find tools/mgba/mgba-rom-test
python3 hack_scripts/smoke_test.py --all hns --jobs 8        # every Johto map loads (also: emerald, frlg)
python3 hack_scripts/smoke_test.py --trainers 1 MAP_NEW_BARK_TOWN_HNS   # every trainer's team builds
```

Expected: 558/560, 516/518 and 416/417 maps (the misses need a link cable or the Battle Pike),
and `0 bad` trainers.

Play `pokehns.gba` in **mGBA** (recommended) or any GBA emulator. Saves from older test ROMs may
not match; start a new game after big changes.

## 4. Editing

- **Maps, warps, connections, objects**: Porymap (https://github.com/huderlem/porymap). Open the
  repository folder. This is how the planned links between regions (Pallet west, Littleroot south,
  a crossroads route) and Littleroot's new houses get built (`todo.md`).
- **Scripts**: `data/maps/<Map>/scripts.inc` (text). Hoenn's and FireRed's scripts run in their
  own flag "context" (see `CLAUDE.md` and `hack_scripts/gen_*_constants.py`).
- **Generated data**: re-run after changing the inputs, then rebuild:
  - `python3 hack_scripts/build_wild_encounters.py` (wild Pokémon, from the original tables)
  - `python3 hack_scripts/regionalize_trainers.py` (trainers; restore `src/data/trainers*.party`
    from commit `ce11ab767~1` first if re-running from scratch; bosses in `hack_scripts/boss_teams.py`)
  - `python3 hack_scripts/gen_hoenn_constants.py`, `gen_frlg_constants.py` (after flag/var changes)

## 5. Claude Code locally

Open the repository folder in Claude Code (desktop app, CLI `claude`, or an IDE extension). It
reads `CLAUDE.md` and the `design/` folder the same way. The cloud-only SessionStart hook
(`.claude/hooks/session-start.sh`) installs packages with apt; locally you can leave it (it skips
what is already installed) or remove it from `.claude/settings.json` if it causes prompts.

Good first message for a new session: "Read design/todo.md and continue with 'Next session' item 1."

## 6. Sharing a build

`pokehns.gba` is a full ROM; don't commit it (the repository ignores `*.gba`). To share, zip it,
or make a patch against a clean Emerald ROM with a tool like Flips.
