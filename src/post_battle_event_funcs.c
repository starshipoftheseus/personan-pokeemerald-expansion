#include "global.h"
#include "main.h"
#include "credits.h"
#include "event_data.h"
#include "hall_of_fame.h"
#include "hall_of_fame_frlg.h"
#include "load_save.h"
#include "overworld.h"
#include "script_pokemon_util.h"
#include "tv.h"
#include "constants/heal_locations.h"
#include "regions.h"

#if IS_HNS && defined(MAPS_EMERALD) && defined(MAPS_FIRERED)
#define ALL_REGIONS_BUILT TRUE
enum { HOF_REGION_JOHTO, HOF_REGION_HOENN, HOF_REGION_FRLG };

// Which region's league this Hall of Fame belongs to. FireRed Kanto shares Kanto's map sections
// with Heart & Soul's Kanto, so its maps are told apart by their FireRed layouts.
static u32 GetHallOfFameRegion(void)
{
    if (gMapHeader.mapLayout->layoutVersion == LAYOUT_VERSION_FRLG)
        return HOF_REGION_FRLG;
    if (GetCurrentRegion() == REGION_HOENN)
        return HOF_REGION_HOENN;
    return HOF_REGION_JOHTO;
}

// Each region's league script sets its own champion flag before this runs. The game counts as
// cleared (FLAG_SYS_GAME_CLEAR) only once all three champions are beaten (design/overview.md).
static void SetRegionGameClearFlags(void)
{
    switch (GetHallOfFameRegion())
    {
    case HOF_REGION_HOENN:
        FlagSet(FLAG_HOENN_SYS_GAME_CLEAR);
        break;
    case HOF_REGION_FRLG:
        FlagSet(FLAG_FRLG_SYS_GAME_CLEAR);
        break;
    }
    if (FlagGet(FLAG_IS_CHAMPION) && FlagGet(FLAG_HOENN_IS_CHAMPION) && FlagGet(FLAG_FRLG_IS_CHAMPION))
        FlagSet(FLAG_SYS_GAME_CLEAR);
}

// Continue the game from the hometown of the region whose league was just beaten.
static void SetRegionContinueGameWarp(void)
{
    switch (GetHallOfFameRegion())
    {
    case HOF_REGION_HOENN:
        SetContinueGameWarpToHealLocation(gSaveBlock2Ptr->playerGender == MALE
            ? HEAL_LOCATION_LITTLEROOT_TOWN_BRENDANS_HOUSE_2F : HEAL_LOCATION_LITTLEROOT_TOWN_MAYS_HOUSE_2F);
        break;
    case HOF_REGION_FRLG:
        SetContinueGameWarpToHealLocation(HEAL_LOCATION_PALLET_TOWN);
        break;
    default:
        SetContinueGameWarpToHealLocation(HEAL_LOCATION_NEW_BARK_TOWN_HNS);
        break;
    }
}
#else
#define ALL_REGIONS_BUILT FALSE
#endif

int GameClear(void)
{
    int i;
    bool32 ribbonGet;
    struct RibbonCounter {
        u8 partyIndex;
        u8 count;
    } ribbonCounts[6];

    HealPlayerParty();

#if ALL_REGIONS_BUILT
    // Hall of Fame records exist once any region's league has been beaten.
    gHasHallOfFameRecords = (GetGameStat(GAME_STAT_FIRST_HOF_PLAY_TIME) != 0);
    SetRegionGameClearFlags();
#else
    if (FlagGet(FLAG_SYS_GAME_CLEAR) == TRUE)
    {
        gHasHallOfFameRecords = TRUE;
    }
    else
    {
        gHasHallOfFameRecords = FALSE;
        FlagSet(FLAG_SYS_GAME_CLEAR);
    }
#endif

    if (GetGameStat(GAME_STAT_FIRST_HOF_PLAY_TIME) == 0)
        SetGameStat(GAME_STAT_FIRST_HOF_PLAY_TIME, (gSaveBlock2Ptr->playTimeHours << 16) | (gSaveBlock2Ptr->playTimeMinutes << 8) | gSaveBlock2Ptr->playTimeSeconds);

    SetContinueGameWarpStatus();

#if ALL_REGIONS_BUILT
    SetRegionContinueGameWarp();
#else
    if (IS_HNS)
        SetContinueGameWarpToHealLocation(HEAL_LOCATION_NEW_BARK_TOWN_HNS);
    else if (gSaveBlock2Ptr->playerGender == MALE)
        SetContinueGameWarpToHealLocation(HEAL_LOCATION_LITTLEROOT_TOWN_BRENDANS_HOUSE_2F);
    else
        SetContinueGameWarpToHealLocation(HEAL_LOCATION_LITTLEROOT_TOWN_MAYS_HOUSE_2F);
#endif

    ribbonGet = FALSE;

    for (i = 0; i < PARTY_SIZE; i++)
    {
        struct Pokemon *mon = &gPlayerParty[i];

        ribbonCounts[i].partyIndex = i;
        ribbonCounts[i].count = 0;

        if (GetMonData(mon, MON_DATA_SANITY_HAS_SPECIES)
         && !GetMonData(mon, MON_DATA_SANITY_IS_EGG)
         && !GetMonData(mon, MON_DATA_CHAMPION_RIBBON))
        {
            u8 val[1] = {TRUE};
            SetMonData(mon, MON_DATA_CHAMPION_RIBBON, val);
            ribbonCounts[i].count = GetRibbonCount(mon);
            ribbonGet = TRUE;
        }
    }

    if (ribbonGet == TRUE)
    {
        IncrementGameStat(GAME_STAT_RECEIVED_RIBBONS);
        FlagSet(FLAG_SYS_RIBBON_GET);

        for (i = 1; i < 6; i++)
        {
            if (ribbonCounts[i].count > ribbonCounts[0].count)
            {
                struct RibbonCounter prevBest = ribbonCounts[0];
                ribbonCounts[0] = ribbonCounts[i];
                ribbonCounts[i] = prevBest;
            }
        }

        if (ribbonCounts[0].count > NUM_CUTIES_RIBBONS)
        {
            TryPutSpotTheCutiesOnAir(&gPlayerParty[ribbonCounts[0].partyIndex], MON_DATA_CHAMPION_RIBBON);
        }
    }

    SetMainCallback2(CB2_DoHallOfFameScreen);
    return 0;
}

bool8 SetCB2WhiteOut(void)
{
    SetMainCallback2(CB2_WhiteOut);
    return FALSE;
}

bool8 EnterHallOfFame(void)
{
    bool8 ribbonState;
    bool8 *r7;
    int i;
    bool8 gaveAtLeastOneRibbon;
    HealPlayerParty();
#if ALL_REGIONS_BUILT
    // Hall of Fame records exist once any region's league has been beaten.
    gHasHallOfFameRecords = (GetGameStat(GAME_STAT_FIRST_HOF_PLAY_TIME) != 0);
    SetRegionGameClearFlags();
#else
    if (FlagGet(FLAG_SYS_GAME_CLEAR) == TRUE)
    {
        gHasHallOfFameRecords = TRUE;
    }
    else
    {
        gHasHallOfFameRecords = FALSE;
        FlagSet(FLAG_SYS_GAME_CLEAR);
    }
#endif
    if (GetGameStat(GAME_STAT_FIRST_HOF_PLAY_TIME) == 0)
    {
        SetGameStat(GAME_STAT_FIRST_HOF_PLAY_TIME, (gSaveBlock2Ptr->playTimeHours << 16) | (gSaveBlock2Ptr->playTimeMinutes << 8) | gSaveBlock2Ptr->playTimeSeconds);
    }
    SetContinueGameWarpStatus();
#if ALL_REGIONS_BUILT
    SetRegionContinueGameWarp();
#else
    if (IS_HNS)
        SetContinueGameWarpToHealLocation(HEAL_LOCATION_NEW_BARK_TOWN_HNS);
    else
        SetContinueGameWarpToHealLocation(HEAL_LOCATION_PALLET_TOWN);
#endif
    gaveAtLeastOneRibbon = FALSE;
    for (i = 0, r7 = &ribbonState; i < PARTY_SIZE; i++)
    {
        if (GetMonData(&gPlayerParty[i], MON_DATA_SANITY_HAS_SPECIES) && !GetMonData(&gPlayerParty[i], MON_DATA_SANITY_IS_EGG))
        {
            if (!GetMonData(&gPlayerParty[i], MON_DATA_CHAMPION_RIBBON))
            {
                *r7 = TRUE;
                SetMonData(&gPlayerParty[i], MON_DATA_CHAMPION_RIBBON, &ribbonState);
                gaveAtLeastOneRibbon = TRUE;
            }
        }
    }
    if (gaveAtLeastOneRibbon == TRUE)
    {
        IncrementGameStat(GAME_STAT_RECEIVED_RIBBONS);
        FlagSet(FLAG_SYS_RIBBON_GET);
    }
    SetMainCallback2(CB2_DoHallOfFameScreenFrlg);
    return FALSE;
}
