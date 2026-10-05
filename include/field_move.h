#ifndef GUARD_FIELD_MOVE_H
#define GUARD_FIELD_MOVE_H

#include "global.h"
#include "constants/field_move.h"

struct FieldMoveInfo
{
    bool32 (*fieldMoveFunc)(void);
    bool32 (*isUnlockedFunc)(void);
    u16 moveID;
    u8 partyMsgID;
};

extern const struct FieldMoveInfo gFieldMoveInfo[];

static inline bool32 SetUpFieldMove(enum FieldMove fieldMove)
{
    return gFieldMoveInfo[fieldMove].fieldMoveFunc();
}

#if IS_HNS && defined(MAPS_EMERALD)
// Hoenn's rule for a field move (Hoenn badge, and optionally Hoenn's HM gift). See field_move.c.
bool32 IsHoennFieldMoveUnlocked(enum FieldMove fieldMove, bool32 needHm);
#endif

static inline bool32 IsFieldMoveUnlocked(enum FieldMove fieldMove)
{
#if IS_HNS && defined(MAPS_EMERALD)
    // A field move works if either region's rule allows it.
    if (IsHoennFieldMoveUnlocked(fieldMove, FALSE))
        return TRUE;
#endif
    return gFieldMoveInfo[fieldMove].isUnlockedFunc();
}

static inline u32 FieldMove_GetMoveId(enum FieldMove fieldMove)
{
    return gFieldMoveInfo[fieldMove].moveID;
}

static inline u32 FieldMove_GetPartyMsgID(enum FieldMove fieldMove)
{
    return gFieldMoveInfo[fieldMove].partyMsgID;
}

#endif //GUARD_FIELD_MOVE_H
