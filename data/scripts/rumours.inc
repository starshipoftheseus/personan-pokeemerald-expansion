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
