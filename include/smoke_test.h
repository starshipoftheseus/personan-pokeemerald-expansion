#ifndef GUARD_SMOKE_TEST_H
#define GUARD_SMOKE_TEST_H

// Headless smoke test, see src/smoke_test.c and hack_scripts/smoke_test.py.
#define SMOKE_TEST_OFF 0xFFFF

extern const volatile u16 gSmokeTestMap;

void SmokeTest_Start(void);

#endif // GUARD_SMOKE_TEST_H
