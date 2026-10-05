// Starter rumours (design/events.md). A Pokémon Center NPC in each region shares a rumour: a
// starter Pokémon of that region's generations has been seen on a route. The next wild encounter
// on that route is that starter, once. Built on Emerald's mass outbreak (as Pokémon R.O.W.E.'s
// spotted-Pokémon outbreaks are); outbreakUnused3 marks an outbreak as a rumour.
#include "global.h"
#include "event_data.h"
#include "level_scaling.h"
#include "overworld.h"
#include "pokedex.h"
#include "pokemon.h"
#include "region_map.h"
#include "rumour.h"
#include "script.h"
#include "string_util.h"
#include "constants/map_groups.h"

#if IS_HNS && defined(MAPS_EMERALD) && defined(MAPS_FIRERED)

struct Rumour
{
    u16 species;
    u16 map;    // MAP_ constant: (group << 8) | num
};

#define RUMOUR(sp, m) { SPECIES_##sp, MAP_##m }

// Kanto: Gen 1, 4, 7. Johto: Gen 2, 5, 8. Hoenn: Gen 3, 6, 9. Routes are early-game grass.
static const struct Rumour sKantoRumours[] =
{
    RUMOUR(BULBASAUR, VIRIDIAN_FOREST), RUMOUR(CHARMANDER, ROUTE3), RUMOUR(SQUIRTLE, ROUTE24),
    RUMOUR(TURTWIG, ROUTE2), RUMOUR(CHIMCHAR, ROUTE4), RUMOUR(PIPLUP, ROUTE25),
    RUMOUR(ROWLET, ROUTE1), RUMOUR(LITTEN, ROUTE22), RUMOUR(POPPLIO, ROUTE6),
};
static const struct Rumour sJohtoRumours[] =
{
    RUMOUR(CHIKORITA, ROUTE29_HNS), RUMOUR(CYNDAQUIL, ROUTE30_HNS), RUMOUR(TOTODILE, ROUTE32_HNS),
    RUMOUR(SNIVY, ROUTE36_HNS), RUMOUR(TEPIG, ROUTE37_HNS), RUMOUR(OSHAWOTT, ROUTE42_HNS),
    RUMOUR(GROOKEY, ILEX_FOREST_HNS), RUMOUR(SCORBUNNY, ROUTE38_HNS), RUMOUR(SOBBLE, ROUTE43_HNS),
};
static const struct Rumour sHoennRumours[] =
{
    RUMOUR(TREECKO, ROUTE101), RUMOUR(TORCHIC, ROUTE103), RUMOUR(MUDKIP, ROUTE102),
    RUMOUR(CHESPIN, PETALBURG_WOODS), RUMOUR(FENNEKIN, ROUTE112), RUMOUR(FROAKIE, ROUTE104),
    RUMOUR(SPRIGATITO, ROUTE116), RUMOUR(FUECOCO, ROUTE117), RUMOUR(QUAXLY, ROUTE110),
};

#define RUMOUR_MARK 0xA5
#define RUMOUR_DEFAULT_LEVEL 30 // once the region's league is beaten (no cap to go by)

static void ShowRumour(void)
{
    const struct MapHeader *header = Overworld_GetMapHeaderByGroupAndId(gSaveBlock1Ptr->outbreakLocationMapGroup,
                                                                        gSaveBlock1Ptr->outbreakLocationMapNum);
    StringCopy(gStringVar1, GetSpeciesName(gSaveBlock1Ptr->outbreakPokemonSpecies));
    GetMapName(gStringVar2, header->regionMapSectionId, 0);
}

// Sets VAR_RESULT to TRUE and STR_VAR_1/2 to the starter and route when there is a rumour to tell:
// the one already going, or else the next starter of this region not yet caught.
void TryStartStarterRumour(struct ScriptContext *ctx)
{
    const struct Rumour *rumours;
    u32 i, j, count, level;

    (void)ctx;
    gSpecialVar_Result = FALSE;
    if (gSaveBlock1Ptr->outbreakUnused3 == RUMOUR_MARK && gSaveBlock1Ptr->outbreakPokemonSpecies != SPECIES_NONE)
    {
        ShowRumour();
        gSpecialVar_Result = TRUE;
        return;
    }

    switch (gMapHeader.mapLayout->layoutVersion)
    {
    case LAYOUT_VERSION_FRLG:
        rumours = sKantoRumours;
        count = ARRAY_COUNT(sKantoRumours);
        break;
    case LAYOUT_VERSION_EMERALD:
        rumours = sHoennRumours;
        count = ARRAY_COUNT(sHoennRumours);
        break;
    default:
        rumours = sJohtoRumours;
        count = ARRAY_COUNT(sJohtoRumours);
        break;
    }

    for (i = 0; i < count; i++)
    {
        if (!GetSetPokedexFlag(SpeciesToNationalPokedexNum(rumours[i].species), FLAG_GET_CAUGHT))
            break;
    }
    if (i == count)
        return;

    if (gMapHeader.mapLayout->layoutVersion == LAYOUT_VERSION_HNS)
    {
        // Johto: Heart & Soul's own caps, so go by its Johto badges.
        for (level = 8, j = 0; j < 8; j++)
            level += FlagGet(FLAG_BADGE01_GET + j) ? 4 : 0;
        if (FlagGet(FLAG_IS_CHAMPION))
            level = RUMOUR_DEFAULT_LEVEL;
    }
    else
    {
        level = GetScaledLevelCap(FALSE);
        level = level > 10 ? level - 5 : (level == 0 ? RUMOUR_DEFAULT_LEVEL : 5);
    }

    gSaveBlock1Ptr->outbreakPokemonSpecies = rumours[i].species;
    gSaveBlock1Ptr->outbreakLocationMapGroup = rumours[i].map >> 8;
    gSaveBlock1Ptr->outbreakLocationMapNum = rumours[i].map & 0xFF;
    gSaveBlock1Ptr->outbreakPokemonLevel = level;
    gSaveBlock1Ptr->outbreakPokemonProbability = 100;
    gSaveBlock1Ptr->outbreakDaysLeft = 0xFFFF;
    gSaveBlock1Ptr->outbreakUnused3 = RUMOUR_MARK;
    for (i = 0; i < MAX_MON_MOVES; i++)
        gSaveBlock1Ptr->outbreakPokemonMoves[i] = MOVE_NONE;
    ShowRumour();
    gSpecialVar_Result = TRUE;
}

bool32 IsRumourEncounter(void)
{
    return gSaveBlock1Ptr->outbreakUnused3 == RUMOUR_MARK;
}

// A rumour Pokémon appears once: called after it has been created for battle.
void EndRumour(void)
{
    gSaveBlock1Ptr->outbreakPokemonSpecies = SPECIES_NONE;
    gSaveBlock1Ptr->outbreakUnused3 = 0;
    gSaveBlock1Ptr->outbreakDaysLeft = 0;
}

#else

void TryStartStarterRumour(struct ScriptContext *ctx)
{
    (void)ctx;
    gSpecialVar_Result = FALSE;
}

bool32 IsRumourEncounter(void)
{
    return FALSE;
}

void EndRumour(void)
{
}

#endif
