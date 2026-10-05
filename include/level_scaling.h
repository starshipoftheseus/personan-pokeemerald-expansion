#ifndef GUARD_LEVEL_SCALING_H
#define GUARD_LEVEL_SCALING_H

struct Trainer;

u32 GetTotalBadgeCount(void);
u32 GetScaledLevelCap(bool32 hardMode);
u32 GetTrainerPartyLevelBoost(const struct Trainer *trainer, const u32 *monIndices, u32 monsCount);
u32 GetScaledWildMonLevel(u32 level);
u16 GetScaledSpecies(u16 species, u32 level);

#endif // GUARD_LEVEL_SCALING_H
