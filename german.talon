mode: user.german
language: de_DE
-

^(englisch | english)$:
	mode.disable("user.german")
	mode.enable("command")

^german$: skip()

^unicode$:
	user.enable_german_unicode()

^kein unicode$:
	user.disable_german_unicode()

enter: key("enter")

# "weg" should only be recognized when it's not part of a sentence or
# using token for counting the number of "weg"s
^<user.weg>$: user.smart_delete(weg)

^speichern$: edit.save()

<user.satz>: user.smart_insert(satz)
