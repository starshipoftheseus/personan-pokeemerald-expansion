# Events: legendaries, Mythicals and starters

Generated inventory (2026-10-05). Goal: every Pokémon obtainable. Wild Pokémon are handled by
`hack_scripts/regionalize_wild_encounters.py`; these need events instead:

- **Legendaries, Mythicals, Ultra Beasts, Paradox**: small events (design open).
- **Starters**: rumour encounters, built (`src/rumour.c`, `data/scripts/rumours.inc`). The
  gentleman in the Pokémon Centers of Viridian (Kanto), Cherrygrove (Johto) and Oldale (Hoenn)
  tells of the next starter of his region you haven't caught, and the route it was seen on. The
  next wild encounter in that route's grass is that starter, once (Emerald's mass outbreak with a
  rumour mark). Level: the region's level cap - 5 (Johto: 8 + 4 per Johto badge; 30 after its
  league). The routes are in the tables in `src/rumour.c`; more NPCs can call
  `Common_EventScript_TryStarterRumour`.

"In scripts" means some map or common script already names the species (an existing static
encounter or gift), so it may already be obtainable; check before building an event.

## Kanto (Gen 1, 4, 7)

| Pokémon | Kind | In scripts |
|---|---|---|
| Bulbasaur | Starter | yes |
| Charmander | Starter | yes |
| Squirtle | Starter | yes |
| Eevee | Starter | yes |
| Articuno | SubLegendary | yes |
| Zapdos | SubLegendary | yes |
| Moltres | SubLegendary | yes |
| Mewtwo | RestrictedLegendary | yes |
| Mew | Mythical | yes |
| Turtwig | Starter |  |
| Piplup | Starter |  |
| Uxie | SubLegendary |  |
| Mesprit | SubLegendary |  |
| Azelf | SubLegendary |  |
| Dialga | RestrictedLegendary |  |
| Palkia | RestrictedLegendary |  |
| Heatran | SubLegendary |  |
| Regigigas | SubLegendary | yes |
| Giratina_Altered | RestrictedLegendary |  |
| Cresselia | SubLegendary |  |
| Phione | Mythical |  |
| Manaphy | Mythical |  |
| Darkrai | Mythical |  |
| Shaymin_Land | Mythical |  |
| Snivy | Starter |  |
| Tepig | Starter |  |
| Rowlet | Starter |  |
| Type_Null | SubLegendary |  |
| Tapu_Koko | SubLegendary | yes |
| Tapu_Lele | SubLegendary | yes |
| Tapu_Bulu | SubLegendary | yes |
| Tapu_Fini | SubLegendary | yes |
| Cosmog | RestrictedLegendary |  |
| Cosmoem | RestrictedLegendary |  |
| Solgaleo | RestrictedLegendary |  |
| Lunala | RestrictedLegendary |  |
| Nihilego | UltraBeast |  |
| Buzzwole | UltraBeast |  |
| Pheromosa | UltraBeast |  |
| Xurkitree | UltraBeast |  |
| Celesteela | UltraBeast |  |
| Kartana | UltraBeast |  |
| Guzzlord | UltraBeast |  |
| Necrozma | RestrictedLegendary |  |
| Magearna | Mythical |  |
| Marshadow | Mythical |  |
| Poipole | UltraBeast |  |
| Naganadel | UltraBeast |  |
| Stakataka | UltraBeast |  |
| Blacephalon | UltraBeast |  |
| Zeraora | Mythical |  |
| Meltan | Mythical |  |
| Melmetal | Mythical |  |
| Scorbunny | Starter |  |
| Sobble | Starter |  |

## Johto (Gen 2, 5, 8)

| Pokémon | Kind | In scripts |
|---|---|---|
| Articuno_Galar | SubLegendary |  |
| Zapdos_Galar | SubLegendary |  |
| Moltres_Galar | SubLegendary |  |
| Chikorita | Starter | yes |
| Cyndaquil | Starter | yes |
| Totodile | Starter | yes |
| Raikou | SubLegendary | yes |
| Entei | SubLegendary | yes |
| Suicune | SubLegendary | yes |
| Lugia | RestrictedLegendary | yes |
| Ho_Oh | RestrictedLegendary | yes |
| Celebi | Mythical | yes |
| Victini | Mythical |  |
| Oshawott | Starter |  |
| Cobalion | SubLegendary |  |
| Terrakion | SubLegendary |  |
| Virizion | SubLegendary |  |
| Tornadus_Incarnate | SubLegendary |  |
| Thundurus_Incarnate | SubLegendary |  |
| Reshiram | RestrictedLegendary |  |
| Zekrom | RestrictedLegendary |  |
| Landorus_Incarnate | SubLegendary |  |
| Kyurem | RestrictedLegendary |  |
| Keldeo_Ordinary | Mythical |  |
| Meloetta_Aria | Mythical |  |
| Fennekin | Starter |  |
| Grookey | Starter |  |
| Zacian_Hero | RestrictedLegendary |  |
| Zamazenta_Hero | RestrictedLegendary |  |
| Eternatus | RestrictedLegendary |  |
| Kubfu | SubLegendary |  |
| Urshifu_Single_Strike | SubLegendary |  |
| Zarude | Mythical |  |
| Regieleki | SubLegendary | yes |
| Regidrago | SubLegendary | yes |
| Glastrier | SubLegendary |  |
| Spectrier | SubLegendary |  |
| Calyrex | RestrictedLegendary |  |
| Enamorus_Incarnate | SubLegendary |  |
| Fuecoco | Starter |  |
| Quaxly | Starter |  |

## Hoenn (Gen 3, 6, 9)

| Pokémon | Kind | In scripts |
|---|---|---|
| Treecko | Starter | yes |
| Torchic | Starter | yes |
| Mudkip | Starter | yes |
| Regirock | SubLegendary | yes |
| Regice | SubLegendary | yes |
| Registeel | SubLegendary | yes |
| Latias | SubLegendary | yes |
| Latios | SubLegendary | yes |
| Kyogre | RestrictedLegendary | yes |
| Groudon | RestrictedLegendary | yes |
| Rayquaza | RestrictedLegendary | yes |
| Jirachi | Mythical | yes |
| Deoxys_Normal | Mythical | yes |
| Chimchar | Starter |  |
| Chespin | Starter |  |
| Froakie | Starter |  |
| Xerneas_Neutral | RestrictedLegendary |  |
| Yveltal | RestrictedLegendary |  |
| Zygarde_50 | RestrictedLegendary |  |
| Diancie | Mythical |  |
| Hoopa_Confined | Mythical |  |
| Volcanion | Mythical |  |
| Litten | Starter |  |
| Popplio | Starter |  |
| Sprigatito | Starter |  |
| Great_Tusk | Paradox |  |
| Scream_Tail | Paradox |  |
| Brute_Bonnet | Paradox |  |
| Flutter_Mane | Paradox |  |
| Slither_Wing | Paradox |  |
| Sandy_Shocks | Paradox |  |
| Iron_Treads | Paradox |  |
| Iron_Bundle | Paradox |  |
| Iron_Hands | Paradox |  |
| Iron_Jugulis | Paradox |  |
| Iron_Moth | Paradox |  |
| Iron_Thorns | Paradox |  |
| Wo_Chien | SubLegendary |  |
| Chien_Pao | SubLegendary |  |
| Ting_Lu | SubLegendary |  |
| Chi_Yu | SubLegendary |  |
| Roaring_Moon | Paradox |  |
| Iron_Valiant | Paradox |  |
| Koraidon | RestrictedLegendary |  |
| Miraidon | RestrictedLegendary |  |
| Walking_Wake | Paradox |  |
| Iron_Leaves | Paradox |  |
| Okidogi | SubLegendary |  |
| Munkidori | SubLegendary |  |
| Fezandipiti | SubLegendary |  |
| Gouging_Fire | Paradox |  |
| Raging_Bolt | Paradox |  |
| Iron_Boulder | Paradox |  |
| Iron_Crown | Paradox |  |
| Terapagos_Normal | RestrictedLegendary |  |
| Pecharunt | Mythical |  |
