# Legendary mini-events (proposal)

Every legendary, Mythical, Ultra Beast and Paradox Pokémon gets a small event in its region
(Kanto = Gen 1/4/7, Johto = Gen 2/5/8, Hoenn = Gen 3/6/9), drawn from the game or movie it is
known from. Those the base games already give (Kanto's birds and Mewtwo, Johto's beasts, Lugia
and Ho-Oh, Hoenn's Regis, weather trio, Eon duo...) keep their original events; see
`events.md` for which already exist in scripts. Unless noted, events open after that region's
Elite Four, so the region rule (`balance.md`) is never broken by a legendary.

Event types used below:
- **Scene**: a short scripted moment, then a static encounter.
- **Hunt**: collect or visit things around the region (items, cells, shrines).
- **Key item**: an item or condition unlocks a place.
- **Rumour**: as with starters (`src/rumour.c`): an NPC names a place for a one-time encounter.

## Kanto (Gen 1, 4, 7)

| Pokémon | Source | Event |
|---|---|---|
| Mew | FRLG/RBY truck legend; *Lucario and the Mystery of Mew* | **Scene**: after the league, Strength the truck by the S.S. Anne dock: under it, a glint. Mew leads you on a chase across Kanto's routes (3 sightings), ending at a tree on Route 21 (the Tree of Beginning) |
| Mewtwo | RBY/FRLG; *Mewtwo Strikes Back* | Keep Cerulean Cave. Add a Cinnabar Mansion journal trail (already in FRLG) as the lead-in |
| Articuno, Zapdos, Moltres | RBY/FRLG; *The Power of One* | Keep Seafoam, Power Plant, Mt Ember |
| Uxie, Mesprit, Azelf | Diamond/Pearl lakes | **Hunt**: three Sevii lakes (Icefall Cave pool, Berry Forest pond, Lost Cave spring). Mesprit roams after you first see it |
| Dialga, Palkia | DP Spear Pillar; *The Rise of Darkrai* | **Key item**: Adamant and Lustrous Orbs from Silph Co. vaults; meet each atop Mt Moon's summit (new area) at day / night |
| Giratina | Platinum Distortion World; *Giratina and the Sky Warrior* | **Scene**: Griseous Orb in Pokémon Tower's top floor opens a "reverse" Pokémon Tower |
| Darkrai | *The Rise of Darkrai*; Newmoon Island | **Scene**: a sleeping sailor in Vermilion has nightmares; a Member Card-style ticket to a new-moon islet off Route 20 |
| Cresselia | DP Fullmoon Island | Lunar Wing cures the sailor; Cresselia then roams Kanto |
| Heatran | Platinum Stark Mountain | Mt Ember's summit core after the Sevii story (Magma Stone from the Ruby event) |
| Regigigas | DP Snowpoint Temple | Icefall Cave depths; awakens only with Regirock, Regice and Registeel in your party (ties to Hoenn) |
| Shaymin | *Giratina and the Sky Warrior*; Flower Paradise | **Key item**: Gracidea from Celadon's flower shop opens a meadow on Five Isle |
| Arceus | *Arceus and the Jewel of Life*; Spear Pillar | Final Kanto event: all Kanto legendaries caught → Azure Flute at Indigo Plateau |
| Manaphy, Phione | *Pokémon Ranger and the Temple of the Sea* | **Scene**: a Ranger in Seafoam gives the Manaphy Egg; Phione in the Seafoam rapids |
| Type: Null, Silvally | Sun/Moon Aether | Gift from a Silph scientist after Silph Co. (Kanto's Aether) |
| Tapu Koko, Lele, Bulu, Fini | SM island guardians | One per Sevii island group (shrines on One, Three, Five and Seven Island) |
| Cosmog → Solgaleo/Lunala | SM Altar of the Sunne/Moone | Gift from Lillie-like NPC on Seven Island; evolves by level |
| Necrozma | Ultra Sun/Moon | Ultra Wormhole at Cerulean Cave's depths after Solgaleo/Lunala |
| Nihilego … Blacephalon (Ultra Beasts) | USUM Ultra Wormholes | **Rumour**: after Necrozma, an "Interpol" agent in Saffron names a route where one appears, one at a time |
| Magearna | *Volcanion and the Mechanical Marvel* | Silph Co. lab: a 500-year-old machine; fix it with parts found in the Rocket Hideout |
| Marshadow | *I Choose You!* | Rumour in Lavender's Pokémon Tower |
| Zeraora | *The Power of Us* | Power Plant after Zapdos: a "Fula City" festival scene |
| Meltan, Melmetal | Pokémon GO / Let's Go mystery box | Meltan appear around the Power Plant once you hold a Mystery Box (from Bill) |

## Johto (Gen 2, 5, 8)

| Pokémon | Source | Event |
|---|---|---|
| Raikou, Entei, Suicune | GSC/HGSS Burned Tower; *Spell of the Unown*; *Zoroark* | Keep Heart & Soul's events |
| Lugia, Ho-Oh | GSC/HGSS; *The Power of One*; *I Choose You!* | Keep Heart & Soul's events |
| Celebi | GSC GS Ball; *Voice of the Forest*; *Secrets of the Jungle* | **Scene**: GS Ball at the Ilex Forest shrine. **Proposal: Celebi is the time travel to the later-era Kanto** (the portal idea in `story.md`) |
| Victini | BW Liberty Garden; *Victini and the Black/White Hero* | Liberty Pass from the Goldenrod Radio Tower; a lighthouse islet near Olivine |
| Reshiram, Zekrom | BW Dragonspiral Tower; *Victini and Reshiram/Zekrom* | Light Stone / Dark Stone found in the Ruins of Alph; awaken at Tin Tower's roof (white) or Dragon's Den (black) |
| Kyurem | BW Giant Chasm | Ice Path's deepest floor; DNA Splicers from the Dragon's Den elder |
| Cobalion, Terrakion, Virizion | BW; *Kyurem vs. the Sword of Justice* | **Hunt**: Mt Silver cave, Route 45 cliffs, Ilex Forest |
| Keldeo | *Kyurem vs. the Sword of Justice* | With the three Swords in your party, Keldeo waits at Lake of Rage |
| Tornadus, Thundurus, Landorus | BW Abundant Shrine | Tornadus/Thundurus roam Johto; Reveal Glass at a new shrine on Route 47 calls Landorus |
| Meloetta | BW2 Relic Song | Goldenrod Theater: play the Relic Song (a piano NPC) after the league |
| Genesect | *Genesect and the Legend Awakened* | Rocket's lab under the Goldenrod Underground (they revived it, like Team Plasma) |
| Zacian, Zamazenta, Eternatus | Sword/Shield | **Scene**: "Darkest Day" over Mt Mortar's peak; Rusted Sword/Shield in the National Park |
| Kubfu → Urshifu | Isle of Armor | Gift from Chuck's dojo in Cianwood; Tower of Darkness/Waters = Whirl Islands or Cliff Edge |
| Regieleki, Regidrago | Crown Tundra Split-Decision Ruins | Ruins of Alph's sealed chamber: choose one (the other via rematch) |
| Glastrier, Spectrier, Calyrex | Crown Tundra | Mahogany's old woman: carrots grown at Route 43's farm |
| Zarude | *Secrets of the Jungle* | Rumour in Ilex Forest after Celebi |
| Enamorus | Legends: Arceus | Roams Johto in spring (month-based), after Tornadus/Thundurus |

## Hoenn (Gen 3, 6, 9)

| Pokémon | Source | Event |
|---|---|---|
| Regirock, Regice, Registeel | RSE braille | Keep Emerald's events |
| Latias, Latios | RSE; *Pokémon Heroes* (Alto Mare) | Keep the roamer; Southern Island via a "Soul Dew" scene instead of the Eon Ticket |
| Kyogre, Groudon, Rayquaza | RSE | Keep Emerald's events |
| Jirachi | *Jirachi: Wish Maker*; Millennium Comet | **Scene**: a festival at Fallarbor (a comet seen once each 1000 years: one night after the league) |
| Deoxys | *Destiny Deoxys*; FRLG Birth Island | **Scene**: a meteor falls near Mossdeep's Space Center; Birth Island triangle puzzle |
| Xerneas, Yveltal | XY; *Diancie and the Cocoon of Destruction* | Sky Pillar's twin: a new tree (Xerneas) and cocoon (Yveltal) at the Mirage Tower site |
| Zygarde | XY/SM cells | **Hunt**: 10 Zygarde Cells hidden around Hoenn (a Zygarde Cube from Professor Cozmo) |
| Diancie | *Diancie and the Cocoon of Destruction* | Granite Cave: a Carbink colony asks for help; Diancie joins |
| Hoopa | *Hoopa and the Clash of Ages* | Prison Bottle found in Mirage Tower; Hoopa unbound brings back any legendary you missed |
| Volcanion | *Volcanion and the Mechanical Marvel* | Mt Chimney's crater, after Groudon |
| Koraidon, Miraidon | Scarlet/Violet; Area Zero | **Proposal**: Professor Sada/Turo's time machine (a lab in Sootopolis' depths); ties to the time travel story |
| Paradox Pokémon (Great Tusk … Iron Crown) | Scarlet/Violet Area Zero | **Rumour**: after the time machine, one at a time on Hoenn's routes ("ancient" by day, "future" by night) |
| Wo-Chien, Chien-Pao, Ting-Lu, Chi-Yu | SV Treasures of Ruin | **Hunt**: 8 stakes per shrine around Hoenn; four sealed shrines |
| Okidogi, Munkidori, Fezandipiti, Ogerpon | Teal Mask (Kitakami) | Festival at Fortree; the Loyal Three as bosses, then Ogerpon with the masks |
| Terapagos | Indigo Disk | Last Hoenn event: Area Zero's crystal under the Cave of Origin |
| Pecharunt | Mochi Mayhem | A peach-shaped chest in Mt Pyre after the Loyal Three |

## Build order (suggested)

1. Rumour-style ones first (Ultra Beasts, Paradox, Marshadow, Zarude): the rumour system exists.
2. Ones that reuse existing places with a static encounter (Volcanion, Heatran, Kyurem, Swords).
3. Scenes needing new maps (Tree of Beginning, Newmoon islet, shrines) need Porymap work first.
4. Celebi's time travel and the Koraidon/Miraidon time machine with the story's time jump.
