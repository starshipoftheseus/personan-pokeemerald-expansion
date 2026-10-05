# Emerald Extended Cut: how its open world is built

Notes from reading the Classic+ Hotfix 1.5 ROM (32 MB, game code BPEE) with
`hack_scripts`-style scripts; no source code is published. Permission and credit: `credits/README.md`.

## Size and content

- 43 map groups, 1,065 maps (vanilla Emerald: 34 groups, ~518 maps).
- 238 map sections. Johto's sections reuse FireRed's spare section slots
  (e.g. 154 ROUTE 47, 156 ROUTE 38, 171-174 ROUTE 30-33), then new ones from 213 (Crossgate Town)
  to 237 (Union Cave).
- New Hoenn areas: Route 98, Route 99, Route 100, Crossgate Town (+ shipyard), Outcast Island,
  Embedded Tower. Extras: The Moon / Mt. Unknown / Cydonia, Cobalt Beach, Bill's Garden.

## How the regions join: one continuous overworld

The regions are stitched together with ordinary map connections, so you can walk (or surf) between them.
There are no portal tricks:

| From | To | How |
|---|---|---|
| Hoenn Route 98 | Johto New Bark Town, Cherrygrove, Route 27 | Walking connection |
| Hoenn Route 99 | Johto Cherrygrove, Route 32 | Walking connection |
| Hoenn Route 115 | Johto Route 41 (sea) | Surf connection |
| Hoenn Route 125 | Kanto Cinnabar Island (sea) | Surf connection |
| Kanto Route 22 / 23 | Johto Route 26 / 28 | Walking connection (as in HGSS) |
| Sevii Green Path | Outcast Island | Connection |
| Harbors (Slateport, Lilycove, Vermilion, Olivine) and Sevii ferries | Each other | Ferry scripts |

So Hoenn sits "south" of Johto (Routes 98/99 off New Bark/Cherrygrove) and "west" of Kanto by sea
(Route 125 to Cinnabar). The story starts in Littleroot; other regions open up as HMs (Surf etc.)
and story gates allow.

## What we can learn for our hack

- **Connections over portals.** Our regions are separate map sets, but nothing stops us adding
  Porymap connections between edge maps (e.g. a new route from New Bark south to Hoenn, and a sea
  route from Hoenn to FireRed's Cinnabar). That gives a real open world, and ferries cover the rest.
- **Gating by field moves**, not region locks: Surf opens the sea links, so region order emerges
  from what you can traverse.
- **Single start**: like Extended Cut (Littleroot), ours starts in one place, Pallet Town
  (`story.md`).

# Pokémon R.O.W.E. (BelialClover)

Open-world Emerald (Hoenn only), source at github.com/BelialClover/RoweSource (v1.9.4, Jan 2024)
and github.com/BelialClover/PokemonROWE (older, 2022). Built on a 2021-era pokeemerald-expansion,
so its code doesn't drop into our current expansion without porting. **No licence file in either
repo**: ask BelialClover before copying code or assets; ideas are free to use.

Worth studying:
- `src/level_scaling.c`: trainers' and wild Pokémon levels scale with badge count (with evolutions
  applied to scaled mons), per-difficulty tables, boss minimum levels. This is what makes "any order"
  work. Our version would need to count all regions' badges.
- Soft level caps per badge count (`sLevelCaps`, hard mode).
- `data/scripts/flying_taxi.inc`: fly to visited towns from the start, without the HM.
- Quests (`src/quests.c`), game modes (randomised, inverse, double battles), DexNav.
Already in our expansion base: following Pokémon, Gen 8+ mechanics, physical/special split.
