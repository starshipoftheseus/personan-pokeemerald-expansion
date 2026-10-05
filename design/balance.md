# Balance
## Level curve
| Milestone | Ace level |
|---|---|
| Gym 1 | |
| Gym 2 | |

## Rules
- **Region rule** (decided 2026-10-05): until a region's Elite Four is beaten, use only Pokémon from
  that region: Kanto = Gen 1, 4, 7; Johto = Gen 2, 5, 8; Hoenn = Gen 3, 6, 9. Honour system for now
  (not enforced by the game). Later: make each region's wild Pokémon match these generations.
- **Level caps**: on when the player picks a level cap in Heart & Soul's challenge menu (Normal, or
  Hard = 2 lower). Each region uses its own badges until its league is beaten, then its cap lifts:
  - FireRed Kanto: 14, 21, 24, 29, 43, 43, 47, 50, league 63 (`src/level_scaling.c`)
  - Hoenn: 15, 19, 24, 29, 31, 33, 42, 46, league 58
  - Johto and Heart & Soul's Kanto: Heart & Soul's own caps (`src/caps.c`)
- **Level scaling** (`B_LEVEL_SCALING`, approach from Pokémon R.O.W.E.): only when revisiting a
  region whose league is beaten. Trainers and wild Pokémon are raised (never lowered) to a level set
  by total badges across all regions; raised Pokémon evolve to match. Provisional numbers.
- EV/IV handling:
- Items in battle for trainers:

## Trainer teams
(Name — location — team)
