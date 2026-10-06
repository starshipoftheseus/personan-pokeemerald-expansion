# Playtest checklist (test ROM 8)

Start a **new save**. Note anything wrong with: ROM number, map, what you did, what happened.
Priority: **P1** = blocks play, **P2** = wrong but playable, **P3** = polish.

## P1: core loop
1. New game starts (title, intro, New Bark Town); you can move, talk, open the menu.
2. Get a starter in Elm's lab; first wild battle on Route 29 works (start, attack, catch, run).
3. A trainer battle works and ends normally (win and lose/white out).
4. Save, reset, Continue: you're where you saved with your party and items.
5. Pokémon Center healing works (Johto, Kanto, Hoenn), and the PC (box) works.
6. **Ferry**: Cherrygrove Pokémon Center gentleman (after you have a Pokémon) -> say yes, pick
   Kanto -> arrive in Pallet Town. Repeat from Viridian's center to Hoenn (Littleroot) and from
   Oldale's center back to Johto (New Bark). No freeze, black screen or stuck player.
7. Walking around each hometown and its first route doesn't freeze or soft-lock (can always leave).

## P1: Hoenn start
8. Littleroot: no moving vans, no frozen people; you can walk north to Route 101.
9. Route 101: no Birch-and-Zigzagoon scene; grass battles work.
10. Birch's lab: no voice/scene when you enter; Birch is there and talks.
11. Oldale and Route 103: no stuck rival scene.

## P1: Kanto (FireRed) start
12. Pallet Town: NPCs visible with normal colours; Oak's lab door animates.
13. Walking north to Route 1: Oak's "wait!" scene and getting a FireRed starter (if it triggers)
    completes without freezing. Note whether it triggers.
14. Viridian City and Route 1 battles work.

## P2: region features
15. **Wild Pokémon**: Route 29 by day vs night shows different Pokémon (change the clock / play
    at night). Hoenn Route 101 and Kanto Route 1 show region-appropriate Pokémon (Kanto: Gen 1/4/7,
    Johto: 2/5/8, Hoenn: 3/6/9). Surfing, fishing and Rock Smash give Pokémon.
16. **Trainers**: Route 102 (Hoenn) and Route 30 (Johto) trainers use their region's generations;
    Roxanne / Falkner / Brock have their regional teams (design/balance.md, boss_teams.py).
17. **Starter rumours**: the same gentleman tells a rumour (e.g. Bulbasaur in Viridian Forest);
    the next grass encounter there is that starter, once.
18. **Level caps** (only if you chose a cap in the new-game challenge menu): EXP stops at the cap;
    Hoenn/Kanto use their own badges.
19. **Town Map / Fly**: the map shows the region you are in (Johto, Hoenn, Kanto); flying to a
    visited town works.
20. **Doors** animate in all three regions; **healing balls** appear in Hoenn centers.
21. **Summary screen**: Rename and Relearn options work.
22. **Berry trees** in Hoenn (Route 102, 104): visible, can pick berries. If missing, note the route.

## P2: progression
23. Beat a gym in each region: badge given, field move unlocked (Cut/Flash...), badge counted on
    the save screen.
24. HM field moves work in Hoenn and Kanto with that region's badge.
25. Day Care in each region accepts Pokémon.

## P3: polish
26. Sprite colours, missing sprites, odd music, text errors, tile seams anywhere.
27. Map name popups show the right names in all regions.
28. Following Pokémon, running shoes, bike in all regions.

## Known gaps (not bugs)
- No walking routes between regions yet (ferry only; plan in region_links.md).
- New game starts in New Bark, not Pallet (planned).
- Legendary events, Ruby/Sapphire in Littleroot, Dewford Gym redesign: not built yet.
- Union Rooms and Battle Pike rooms need a link cable / Frontier challenge.
- The Pokémon-only-from-their-region rule is on the honour system.
