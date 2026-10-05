// Level scaling and level caps across regions.
// Approach adapted from Pokémon R.O.W.E. by BelialClover (design/credits/README.md).
//
// Each region is played at its own levels with its own badge level cap until its Elite Four is
// beaten. Revisiting a beaten region, trainers' and wild Pokémon's levels are raised (never
// lowered) to match the player's total badges, and raised Pokémon evolve to suit their level.
#include "global.h"
#include "data.h"
#include "event_data.h"
#include "level_scaling.h"
#include "pokemon.h"
#include "random.h"
#include "constants/trainers.h"

#if IS_HNS && defined(MAPS_EMERALD) && defined(MAPS_FIRERED)
#define LEVEL_SCALING_ACTIVE B_LEVEL_SCALING
#else
#define LEVEL_SCALING_ACTIVE FALSE
#endif

// Region rules (design/balance.md): while a region's Elite Four is unbeaten you play it at its own
// levels, with a level cap from that region's own badges. Once its league is beaten its cap lifts,
// and coming back later its trainers and wild Pokémon scale with your total badges.
enum { SCALING_REGION_HNS, SCALING_REGION_HOENN, SCALING_REGION_FRLG };

// Caps from each game's gym leaders' aces (badges 0-8; the 9th entry is its league).
static const u8 sFrlgLevelCaps[]  = { 14, 21, 24, 29, 43, 43, 47, 50, 63 };
static const u8 sHoennLevelCaps[] = { 15, 19, 24, 29, 31, 33, 42, 46, 58 };

// Scaling floor when revisiting a beaten region, by total badge count (all regions).
static const u8 sRevisitLevelByBadges[] =
{
    14, 21, 24, 29, 43, 43, 47, 50, 63,
    65, 67, 69, 71, 73, 75, 77, 80,
    82, 84, 86, 88, 90, 92, 94, 97,
    98, 98, 99, 99, 99, 99, 100, 100, 100,
};

#define HARD_MODE_CAP_DROP      2   // Hard caps sit this many levels lower
#define TRAINER_FLOOR_BELOW_CAP 10  // ordinary trainers' strongest Pokémon reaches floor level - this
#define BOSS_FLOOR_BELOW_CAP    3   // gym leaders, Elite Four, champions and rivals
#define WILD_FLOOR_BELOW_CAP    14  // wild Pokémon (+ a little random spread)
#define NON_LEVEL_EVO_LEVEL     36  // trade, stone, friendship etc. evolutions happen at this level

static u32 GetScalingRegion(void)
{
#ifdef MAPS_FIRERED
    if (gMapHeader.mapLayout->layoutVersion == LAYOUT_VERSION_FRLG)
        return SCALING_REGION_FRLG;
#endif
#ifdef MAPS_EMERALD
    if (gMapHeader.mapLayout->layoutVersion == LAYOUT_VERSION_EMERALD)
        return SCALING_REGION_HOENN;
#endif
    return SCALING_REGION_HNS;
}

static bool32 IsRegionLeagueBeaten(u32 region)
{
    switch (region)
    {
#ifdef MAPS_FIRERED
    case SCALING_REGION_FRLG:
        return FlagGet(FLAG_FRLG_IS_CHAMPION);
#endif
#ifdef MAPS_EMERALD
    case SCALING_REGION_HOENN:
        return FlagGet(FLAG_HOENN_IS_CHAMPION);
#endif
    default:
        return FlagGet(FLAG_IS_CHAMPION);
    }
}

static u32 CountBadges(u32 firstFlag, u32 count)
{
    u32 i, badges = 0;
    for (i = 0; i < count; i++)
        badges += FlagGet(firstFlag + i);
    return badges;
}

u32 GetTotalBadgeCount(void)
{
    u32 i, count = 0;

    for (i = 0; i < NUM_BADGES; i++)   // Heart & Soul: Johto and its own Kanto
        count += FlagGet(FLAG_BADGE01_GET + i);
#ifdef MAPS_EMERALD
    for (i = 0; i < 8; i++)
        count += FlagGet(FLAG_HOENN_BADGE01_GET + i);
#endif
#ifdef MAPS_FIRERED
    for (i = 0; i < 8; i++)
        count += FlagGet(FLAG_FRLG_BADGE01_GET + i);
#endif
    return count;
}

// The level cap in the current region, or 0 when Heart & Soul's own caps apply (Johto and its
// Kanto) or the region's league is beaten.
u32 GetScaledLevelCap(bool32 hardMode)
{
    u32 region = GetScalingRegion();
    const u8 *caps;
    u32 badges;

    if (region == SCALING_REGION_HNS || IsRegionLeagueBeaten(region))
        return 0;
#ifdef MAPS_FIRERED
    if (region == SCALING_REGION_FRLG)
    {
        caps = sFrlgLevelCaps;
        badges = CountBadges(FLAG_FRLG_BADGE01_GET, 8);
    }
    else
#endif
    {
#ifdef MAPS_EMERALD
        caps = sHoennLevelCaps;
        badges = CountBadges(FLAG_HOENN_BADGE01_GET, 8);
#else
        return 0;
#endif
    }
    return caps[badges] - (hardMode ? HARD_MODE_CAP_DROP : 0);
}

static u32 GetRevisitLevel(void)
{
    u32 badges = GetTotalBadgeCount();
    if (badges >= ARRAY_COUNT(sRevisitLevelByBadges))
        badges = ARRAY_COUNT(sRevisitLevelByBadges) - 1;
    return sRevisitLevelByBadges[badges];
}

static bool32 IsScalingActiveHere(void)
{
    return LEVEL_SCALING_ACTIVE && IsRegionLeagueBeaten(GetScalingRegion());
}

static bool32 IsBossClass(u32 trainerClass)
{
    switch (trainerClass)
    {
    case TRAINER_CLASS_LEADER:
    case TRAINER_CLASS_ELITE_FOUR:
    case TRAINER_CLASS_CHAMPION:
    case TRAINER_CLASS_RIVAL:
        return TRUE;
    default:
        return FALSE;
    }
}

// Levels to add to every Pokémon in a trainer's party, so its strongest one reaches the floor.
// The whole party moves together, keeping the gaps the trainer was designed with.
u32 GetTrainerPartyLevelBoost(const struct Trainer *trainer, const u32 *monIndices, u32 monsCount)
{
    u32 i, highest = 0, floor;
    u32 cap = GetRevisitLevel();

    if (!IsScalingActiveHere())
        return 0;

    for (i = 0; i < monsCount; i++)
    {
        if (trainer->party[monIndices[i]].lvl > highest)
            highest = trainer->party[monIndices[i]].lvl;
    }
    floor = cap - (IsBossClass(trainer->trainerClass) ? BOSS_FLOOR_BELOW_CAP : TRAINER_FLOOR_BELOW_CAP);
    return highest < floor ? floor - highest : 0;
}

u32 GetScaledWildMonLevel(u32 level)
{
    u32 floor;

    if (!IsScalingActiveHere())
        return level;
    floor = GetRevisitLevel() - WILD_FLOOR_BELOW_CAP;
    if (level >= floor)
        return level;
    return floor + Random() % 4;
}

// The species a Pokémon would be by this level: level evolutions at their level, others at
// NON_LEVEL_EVO_LEVEL. With several options (e.g. Eevee) the first one listed is used.
u16 GetScaledSpecies(u16 species, u32 level)
{
    u32 stage, i;

    if (!LEVEL_SCALING_ACTIVE)
        return species;

    for (stage = 0; stage < 3; stage++)
    {
        const struct Evolution *evos = GetSpeciesEvolutions(species);
        u16 next = SPECIES_NONE;

        if (evos == NULL)
            break;
        for (i = 0; evos[i].method != EVOLUTIONS_END; i++)
        {
            u32 needed;

            switch (evos[i].method)
            {
            case EVO_LEVEL:
                needed = evos[i].param != 0 ? evos[i].param : NON_LEVEL_EVO_LEVEL;
                break;
            case EVO_TRADE:
            case EVO_ITEM:
            case EVO_LEVEL_BATTLE_ONLY:
                needed = NON_LEVEL_EVO_LEVEL;
                break;
            default:
                continue;
            }
            if (level >= needed && IsSpeciesEnabled(evos[i].targetSpecies))
            {
                next = evos[i].targetSpecies;
                break;
            }
        }
        if (next == SPECIES_NONE)
            break;
        species = next;
    }
    return species;
}
