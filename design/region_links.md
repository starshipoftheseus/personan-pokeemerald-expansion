# Region links (plan, for Porymap)

Goal: walk/surf between the regions instead of the ferry (`data/scripts/rumours.inc`, which can
stay as a fast-travel option). Design follows Emerald Extended Cut (Francis III, credited in
`credits/README.md`), which joins its regions with ordinary map connections.

## Extended Cut's links (from its ROM, `extended_cut_notes.md`)

| Extended Cut map (group.num in its ROM) | Connects to |
|---|---|
| Route 98 (0.25), new | Johto New Bark Town, Cherrygrove City, Route 27 |
| Route 99 (0.26), new | Johto Cherrygrove City, Route 32 |
| Hoenn Route 115 (sea edge) | Johto Route 41 |
| Hoenn Route 125 (sea) | Kanto Cinnabar Island |
| Kanto Route 22 / 23 | Johto Route 26 / 28 (as in HGSS) |

Its map data (layout, events, connections) can be read from the ROM with the scripts in this
session's history (map table at 0x66463C, 43 groups); it uses Emerald tilesets plus its own
edits, so copying needs its tileset changes too. Simpler: draw our own versions in Porymap.

## Our plan

| New map | Type | Joins | Notes |
|---|---|---|---|
| `Route98` "Crossroads Route" | land route, ~40x60 | north: New Bark Town (HnS, west edge via Route 27?) ; west: FireRed Pallet Town (west edge) ; south-east: Littleroot Town (south edge) | Hub between the three hometowns. Use Emerald route tilesets (General + Petalburg) for the Hoenn half, FireRed's for the Kanto half, or one style throughout |
| `Route99` "Hoenn Sea Route" | ocean route | Hoenn Route 125 (or 134) <-> FireRed Cinnabar Island (south/east edge) | Surf required: natural progression gate |

Steps in Porymap:
1. New map `Route98` (map type Route, a new map section, e.g. MAPSEC "CROSSROADS"), layout of
   matching size; draw paths with ledges/trees.
2. Add connections: New Bark (left edge) <-> Route98 (right edge); Pallet (left edge) <->
   Route98; Littleroot (bottom edge) <-> Route98 (top edge of a southern arm). Porymap adds both
   directions when "mirror connections" is on.
3. Route99: ocean layout; connect Route 125 edge <-> Route99 <-> Cinnabar edge.
4. Wild encounters for both: add entries to `src/data/wild_encounters.json` (region "crossroads"
   could mix all generations), or let `hack_scripts/build_wild_encounters.py` fill them by adding
   the map's region to `map_regions()`.
5. Build (`make hns`), then `python3 hack_scripts/smoke_test.py MAP_ROUTE98 MAP_ROUTE99`.

Notes:
- Each region keeps its own map style; a connection between different tileset styles works but
  shows a seam: a gate house (indoor map with two warps) at each region border hides it nicely.
- Region rules (level caps, scaling) follow the map's layout version, so the crossroads route
  counts as whichever region's layout style it uses.
