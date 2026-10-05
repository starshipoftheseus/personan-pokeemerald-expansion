#ifndef GUARD_RUMOUR_H
#define GUARD_RUMOUR_H

struct ScriptContext;

void TryStartStarterRumour(struct ScriptContext *ctx);
bool32 IsRumourEncounter(void);
void EndRumour(void);

#endif // GUARD_RUMOUR_H
