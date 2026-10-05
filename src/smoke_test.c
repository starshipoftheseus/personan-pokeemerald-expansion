#include "global.h"
#include "main.h"
#include "battle_main.h"
#include "data.h"
#include "event_data.h"
#include "rumour.h"
#include "pokemon.h"
#include "overworld.h"
#include "script.h"
#include "sprite.h"
#include "task.h"
#include "smoke_test.h"

// Headless smoke test. hack_scripts/smoke_test.py patches gSmokeTestMap in a copy of the ROM
// and runs it in tools/mgba/mgba-rom-test. The game skips the intro, starts a new game on that
// map, runs the overworld for gSmokeTestFrames frames, prints what it sees through mGBA's debug
// log, and stops with SWI 3 (exit code in r0). A crash shows up as a timeout instead.
// In the normal ROM gSmokeTestMap is SMOKE_TEST_OFF and none of this runs.

const volatile u16 gSmokeTestMap = SMOKE_TEST_OFF; // (map group << 8) | map number
const volatile u16 gSmokeTestFrames = 300;
const volatile u16 gSmokeTestTrainers = FALSE; // 1: build every trainer's party and check it;
                                               // 2: the same with every badge and league won (level scaling on)
                                               // 3: start a starter rumour on this map and log it

enum
{
    SMOKE_TEST_ON_MAP,      // still on the map it started on
    SMOKE_TEST_MOVED_MAP,   // a script warped the player somewhere else
};

#define REG_DEBUG_ENABLE (*(vu16 *)0x4FFF780)
#define REG_DEBUG_FLAGS  (*(vu16 *)0x4FFF700)
#define REG_DEBUG_STRING ((char *)0x4FFF600)
#define DEBUG_LOG_INFO   (3 | 0x100)

static u32 sFramesRun;

static char *AppendString(char *dst, const char *src)
{
    while (*src)
        *dst++ = *src++;
    return dst;
}

static char *AppendNumber(char *dst, u32 value)
{
    char digits[10];
    u32 count = 0;

    do
    {
        digits[count++] = '0' + value % 10;
        value /= 10;
    } while (value != 0);
    while (count != 0)
        *dst++ = digits[--count];
    return dst;
}

static void LogValue(const char *name, u32 value)
{
    char *end = AppendNumber(AppendString(AppendString(REG_DEBUG_STRING, "SMOKE "), name), value);
    *end = '\0';
    REG_DEBUG_FLAGS = DEBUG_LOG_INFO;
}

static void Exit(u32 exitCode)
{
    register u32 r0 asm("r0") = exitCode;
    asm volatile("swi 0x3" :: "r" (r0));
}

// Builds every trainer's party as a battle would and checks each Pokémon is a real species at a
// sane level. Logs the bad trainers and exits with the count of them.
static void CheckTrainerParties(void)
{
    u32 id, i, bad = 0, checked = 0, lowest = MAX_LEVEL;

    if (gSmokeTestTrainers == 2)
    {
        for (i = 0; i < NUM_BADGES; i++)
            FlagSet(FLAG_BADGE01_GET + i);
        FlagSet(FLAG_IS_CHAMPION);
#if defined(MAPS_EMERALD) && defined(MAPS_FIRERED)
        for (i = 0; i < 8; i++)
        {
            FlagSet(FLAG_HOENN_BADGE01_GET + i);
            FlagSet(FLAG_FRLG_BADGE01_GET + i);
        }
        FlagSet(FLAG_HOENN_IS_CHAMPION);
        FlagSet(FLAG_FRLG_IS_CHAMPION);
#endif
    }

    for (id = 1; id < TRAINERS_COUNT; id++)
    {
        const struct Trainer *trainer = GetTrainerStructFromId(id);
        u32 count;

        if (trainer == NULL || trainer->partySize == 0 || trainer->party == NULL)
            continue;
        ZeroEnemyPartyMons();
        count = CreateNPCTrainerPartyFromTrainer(gEnemyParty, trainer, TRUE, BATTLE_TYPE_TRAINER);
        checked++;
        for (i = 0; i < count && i < PARTY_SIZE; i++)
        {
            u32 species = GetMonData(&gEnemyParty[i], MON_DATA_SPECIES);
            u32 level = GetMonData(&gEnemyParty[i], MON_DATA_LEVEL);
            if (level < lowest)
                lowest = level;
            if (species == SPECIES_NONE || !IsSpeciesEnabled(species) || level == 0 || level > MAX_LEVEL)
            {
                LogValue("bad_trainer=", id);
                bad++;
                break;
            }
        }
    }
    LogValue("trainers_checked=", checked);
    LogValue("trainers_bad=", bad);
    LogValue("lowest_level=", lowest);
    Exit(bad != 0 ? 2 : SMOKE_TEST_ON_MAP);
}

static void CB2_SmokeTest(void)
{
    u32 group, num;

    if (gSmokeTestTrainers == 3)
    {
        TryStartStarterRumour(NULL);
        LogValue("rumour=", gSpecialVar_Result);
        LogValue("rumour_species=", gSaveBlock1Ptr->outbreakPokemonSpecies);
        LogValue("rumour_group=", gSaveBlock1Ptr->outbreakLocationMapGroup);
        LogValue("rumour_num=", gSaveBlock1Ptr->outbreakLocationMapNum);
        LogValue("rumour_level=", gSaveBlock1Ptr->outbreakPokemonLevel);
        Exit(SMOKE_TEST_ON_MAP);
    }
    if (gSmokeTestTrainers)
        CheckTrainerParties();

    CB2_Overworld();
    if ((sFramesRun % 100) == 0)
        LogValue("frame=", sFramesRun); // shows how far a run got before a timeout
    if (++sFramesRun < gSmokeTestFrames)
        return;

    group = gSaveBlock1Ptr->location.mapGroup;
    num = gSaveBlock1Ptr->location.mapNum;
    LogValue("target_group=", gSmokeTestMap >> 8);
    LogValue("target_num=", gSmokeTestMap & 0xFF);
    LogValue("map_group=", group);
    LogValue("map_num=", num);
    LogValue("mapsec=", gMapHeader.regionMapSectionId);
    LogValue("layout_version=", gMapHeader.mapLayout->layoutVersion);
    LogValue("x=", gSaveBlock1Ptr->pos.x);
    LogValue("y=", gSaveBlock1Ptr->pos.y);
    LogValue("controls_locked=", ArePlayerFieldControlsLocked());
    LogValue("script_running=", ScriptContext_IsEnabled());
    LogValue("frames=", sFramesRun);
    if (group == (gSmokeTestMap >> 8) && num == (gSmokeTestMap & 0xFF))
        Exit(SMOKE_TEST_ON_MAP);
    else
        Exit(SMOKE_TEST_MOVED_MAP);
}

void SmokeTest_Start(void)
{
    REG_DEBUG_ENABLE = 0xC0DE;
    ResetTasks();
    ResetSpriteData();
    FreeAllSpritePalettes();
    sFramesRun = 0;
    gMain.state = 0; // the map loader runs from state 0; the copyright screen left its own state here
    NewGameOnMap(gSmokeTestMap >> 8, gSmokeTestMap & 0xFF, CB2_SmokeTest);
    LogValue("loaded=", 1); // a timeout without this line hung while loading the map
}
