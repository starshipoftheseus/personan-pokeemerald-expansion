@ Starter rumours (src/rumour.c). Call from an NPC after lock/faceplayer; VAR_RESULT is TRUE if a
@ rumour was told (the NPC's own line is then skipped).
Common_EventScript_TryStarterRumour::
	callnative TryStartStarterRumour
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_NoRumour
	msgbox Common_Text_StarterRumour, MSGBOX_DEFAULT
	closemessage
Common_EventScript_NoRumour:
	return

Common_Text_StarterRumour:
	.string "Have you heard the rumour?\p"
	.string "Someone spotted a wild {STR_VAR_1}\n"
	.string "around {STR_VAR_2}!\p"
	.string "If you go looking there, you might\n"
	.string "just run into it… but only once!$"

@ Travel between regions until routes link them (design/story.md): asks for each other region in
@ turn and warps to its hometown. Needs a Pokémon first.
Common_EventScript_RegionTravel::
	goto_if_unset FLAG_SYS_POKEMON_GET, Common_EventScript_TravelEnd
	msgbox Common_Text_TravelAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Common_EventScript_TravelEnd
	msgbox Common_Text_TravelKanto, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, Common_EventScript_TravelKanto
	msgbox Common_Text_TravelJohto, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, Common_EventScript_TravelJohto
	msgbox Common_Text_TravelHoenn, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, Common_EventScript_TravelHoenn
Common_EventScript_TravelEnd:
	return

Common_EventScript_TravelKanto:
	warp MAP_PALLET_TOWN, 0
	waitstate
	return

Common_EventScript_TravelJohto:
	warp MAP_NEW_BARK_TOWN_HNS, 0
	waitstate
	return

Common_EventScript_TravelHoenn:
	warp MAP_LITTLEROOT_TOWN, 0
	waitstate
	return

Common_Text_TravelAsk:
	.string "I run a ferry to the other regions.\n"
	.string "Would you like to go somewhere?$"

Common_Text_TravelKanto:
	.string "To PALLET TOWN in KANTO?$"

Common_Text_TravelJohto:
	.string "To NEW BARK TOWN in JOHTO?$"

Common_Text_TravelHoenn:
	.string "To LITTLEROOT TOWN in HOENN?$"
