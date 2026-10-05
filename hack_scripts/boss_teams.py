"""Hand-picked regional replacements for bosses' off-region Pokémon (design/balance.md).

Keyed by (trainer Name, region): {old species: new species}, applied to every battle with that boss
in that region (rematches included). Each boss keeps their type theme and team shape; replacements
are of similar strength. Kanto = Gen 1/4/7, Johto = Gen 2/5/8, Hoenn = Gen 3/6/9.
Red, Leaf and Blue's Johto team keep their own Pokémon: they are Kanto's heroes, visiting.
"""

KEEP = {("RED", "Hoenn"), ("LEAF", "Hoenn"), ("BLUE", "Johto")}

S = lambda text: dict(pair.split(">") for pair in text.split())

BOSS_SWAPS = {
    # --- Hoenn (Gen 3, 6, 9)
    ("ROXANNE", "Hoenn"): S("Geodude>Nacli Golem>Garganacl Kabuto>Anorith Kabutops>Armaldo Omanyte>Lileep "
                            "Omastar>Cradily Onix>Carbink Steelix>Tyrantrum Aerodactyl>Glimmora"),
    ("BRAWLY", "Hoenn"): S("Machop>Pancham Machamp>Pangoro Hitmontop>Hawlucha Hitmonchan>Flamigo Hitmonlee>Annihilape"),
    ("WATTSON", "Hoenn"): S("Voltorb>Dedenne Magneton>Klefki Mareep>Pawmi Flaaffy>Pawmo Ampharos>Pawmot Pikachu>Plusle "
                            "Raichu>Heliolisk Electrode>Bellibolt Electabuzz>Kilowattrel"),
    ("FLANNERY", "Hoenn"): S("Slugma>Litleo Magcargo>Pyroar Ponyta>Charcadet Rapidash>Ceruledge Growlithe>Fletchinder "
                             "Arcanine>Talonflame Houndour>Capsakid Houndoom>Scovillain"),
    ("NORMAN", "Hoenn"): S("Chansey>Maushold_Three Blissey>Farigiraf Kangaskhan>Oinkologne_M Tauros>Tauros_Paldea_Combat"),
    ("WINONA", "Hoenn"): S("Skarmory>Bombirdier Dratini>Noibat Dragonair>Noibat Dragonite>Noivern Hoothoot>Fletchling "
                           "Noctowl>Squawkabilly_Green"),
    ("TATE&LIZA", "Hoenn"): S("Xatu>Espathra Slowpoke>Inkay Slowking>Malamar Drowzee>Espurr Hypno>Meowstic_M"),
    ("JUAN", "Hoenn"): S("Kingdra>Tatsugiri_Curly Poliwag>Clauncher Poliwhirl>Finizen Politoed>Clawitzer Lapras>Dondozo"),
    ("WALLACE", "Hoenn"): S("Tentacruel>Dragalge Gyarados>Palafin_Zero"),
    ("DRAKE", "Hoenn"): S("Kingdra>Goodra"),
    ("MATT", "Hoenn"): S("Golbat>Skrelp"),
    ("ARCHIE", "Hoenn"): S("Crobat>Dragalge"),
    ("TABITHA", "Hoenn"): S("Zubat>Shroodle Golbat>Grafaiai"),
    ("MAXIE", "Hoenn"): S("Zubat>Shroodle Crobat>Glimmora"),
    ("WALLY", "Hoenn"): S("Magneton>Klefki"),
    ("BRENDAN", "Hoenn"): S("Slugma>Litleo"),
    ("MAY", "Hoenn"): S("Slugma>Litleo"),
    ("STEVEN", "Hoenn"): S("Skarmory>Tinkaton"),
    # --- FireRed Kanto (Gen 1, 4, 7)
    ("LORELEI", "Kanto"): S("Piloswine>Glaceon"),
    ("BRUNO", "Kanto"): S("Steelix>Lucario Heracross>Pinsir Hariyama>Bewear Hitmontop>Passimian "
                          "Tauros_Paldea_Blaze>Crabominable"),
    ("AGATHA", "Kanto"): S("Crobat>Drifblim Misdreavus>Mismagius"),
    ("LANCE", "Kanto"): S("Kingdra>Garchomp Salamence>Garchomp Altaria>Drampa Noivern>Kommo_O"),
    ("TERRY", "Kanto"): S("Heracross>Pinsir Tyranitar>Rhyperior"),
    # --- Johto (Gen 2, 5, 8)
    ("FALKNER", "Johto"): S("Pidgey>Pidove"),
    ("BUGSY", "Johto"): S("Scyther>Swadloon"),
    ("WHITNEY", "Johto"): S("Clefairy>Snubbull"),
    ("MORTY", "Johto"): S("Haunter>Lampent Gengar>Chandelure"),
    ("PRYCE", "Johto"): S("Dewgong>Beartic Jynx>Mr_Rime Cloyster>Cryogonal Mamoswine>Darmanitan_Galar_Standard"),
    ("JASMINE", "Johto"): S("Magneton>Klinklang Magnezone>Klinklang"),
    ("CHUCK", "Johto"): S("Primeape>Mienshao Poliwrath>Conkeldurr Pinsir>Heracross Annihilape>Grapploct"),
    ("CLAIR", "Johto"): S("Dragonair>Fraxure Gyarados>Druddigon Lapras>Dracovish Dragonite>Hydreigon"),
    ("LANCE", "Johto"): S("Gyarados>Dracovish Charizard>Hydreigon Dragonite>Dragapult"),
    ("{B_RIVAL_NAME}", "Johto"): S("Zubat>Woobat Golbat>Swoobat Weepinbell>Foongus Victreebel>Amoonguss"),
    ("GIOVANNI", "Johto"): S("Kangaskhan>Ursaring Honchkrow>Mandibuzz Nidoqueen>Excadrill Persian>Liepard Nidoking>Krookodile"),
    ("PROTON", "Johto"): S("Koffing>Trubbish Slowpoke>Slowpoke_Galar Muk>Garbodor Nidoqueen>Excadrill "
                           "Weezing>Weezing_Galar Nidoking>Krookodile Rhydon>Golurk"),
    ("ARCHER", "Johto"): S("Porygon_Z>Porygon2 Tauros>Bouffalant Gyarados>Barraskewda Slowbro>Slowbro_Galar Weezing>Weezing_Galar"),
    ("PETREL", "Johto"): S("Cloyster>Arctovish"),
    ("ARIANA", "Johto"): S("Arbok>Scolipede Persian>Liepard Vileplume>Amoonguss Gyarados>Barraskewda"),
    # --- Heart & Soul's Kanto, later era (Gen 1, 4, 7): Johto's leaders visiting, Kanto's leaders, E4
    ("FALKNER", "Kanto"): S("Noctowl>Staraptor Skarmory>Aerodactyl Swellow>Dodrio Pelipper>Gyarados"),
    ("BUGSY", "Kanto"): S("Ledian>Vespiquen Forretress>Vikavolt Scizor>Wormadam_Trash Shedinja>Yanmega Masquerain>Ribombee"),
    ("WHITNEY", "Kanto"): S("Delcatty>Lopunny Blissey>Chansey Miltank>Tauros Ursaluna_Bloodmoon>Snorlax Obstagoon>Bewear"),
    ("MORTY", "Kanto"): S("Sableye>Spiritomb Wyrdeer>Mimikyu_Disguised Typhlosion_Hisui>Marowak_Alola"),
    ("PRYCE", "Kanto"): S("Glalie>Froslass Mr_Rime>Jynx Slowking>Slowbro"),
    ("JASMINE", "Kanto"): S("Skarmory>Bronzong Mawile>Togedemaru Corsola>Omastar Aggron>Bastiodon Steelix>Lucario "
                            "Perrserker>Dugtrio_Alola"),
    ("CHUCK", "Kanto"): S("Medicham>Gallade Annihilape>Machamp Breloom>Passimian Sneasler>Crabominable"),
    ("CLAIR", "Kanto"): S("Shelgon>Gabite Kingdra>Drampa Salamence>Garchomp"),
    ("BROCK", "Kanto"): S("Relicanth>Kabutops Kleavor>Rampardos"),
    ("MISTY", "Kanto"): S("Quagsire>Gastrodon_West Milotic>Lapras Politoed>Poliwrath Swampert>Mudsdale"),
    ("LTSURGE", "Kanto"): S("Lanturn>Luxray Manectric>Electivire"),
    ("ERIKA", "Kanto"): S("Jumpluff>Roserade Bellossom>Vileplume Ludicolo>Lurantis Electrode_Hisui>Tsareena"),
    ("SABRINA", "Kanto"): S("Wobbuffet>Mr_Mime Espeon>Oranguru Mr_Mime_Galar>Hypno Slowbro_Galar>Slowbro "
                            "Rapidash_Galar>Bruxish"),
    ("JANINE", "Kanto"): S("Swalot>Skuntank Crobat>Drapion Weezing_Galar>Weezing Sneasler>Toxicroak"),
    ("BLAINE", "Kanto"): S("Houndoom>Flareon Magcargo>Magmortar Torkoal>Turtonator Camerupt>Ninetales "
                           "Blaziken>Infernape Arcanine_Hisui>Arcanine"),
    ("BLUE", "Kanto"): S("Tyranitar>Rhyperior"),
    ("WILL", "Kanto"): S("Girafarig>Oranguru Slowking>Slowbro Espeon>Gallade Xatu>Oricorio_Pau Gardevoir>Alakazam "
                         "Grumpig>Bronzong Slowking_Galar>Slowbro"),
    ("KOGA", "Kanto"): S("Ariados>Venomoth Qwilfish>Toxapex Crobat>Toxicroak Swalot>Skuntank Clodsire>Nidoking "
                         "Overqwil>Drapion"),
    ("KAREN", "Kanto"): S("Umbreon>Weavile Houndoom>Persian_Alola Absol>Honchkrow Obstagoon>Drapion"),
    ("{B_RIVAL_NAME}", "Kanto"): S("Ursaluna_Bloodmoon>Snorlax Crobat>Honchkrow Octillery>Gyarados Houndoom>Weavile "
                                   "Tyranitar>Garchomp"),
}
