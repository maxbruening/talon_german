mode: user.german
language: de_DE
-
settings():
    speech.timeout = 0.400

# idea: allow to directly chain commands
# how about using 'ego' (as in jp 'eigo')?
^(englisch | english | ego | aygo | pego | hey ingo)$:
	mode.disable("user.german")
	mode.enable("command")

^sleep all [<phrase>]$:
    user.switcher_hide_running()
    user.history_disable()
    user.homophones_hide()
    user.help_hide()
    user.mouse_sleep()
    speech.disable()
    user.engine_sleep()
    skip()
^talon sleep [<phrase>]$:
    speech.disable()
    skip()
^talon wake$:
    speech.enable()
    skip()

^german$: skip()

<user.satz>: user.insert(satz)

^(abkürzung|abkürzungen) <user.acronym>: "{acronym}"

neue zeile: key("enter")
neuer absatz:
  key("enter")
  key("enter")

leerzeichen: " "

# "weg" should only be recognized when it's not part of a sentence or
# using token for counting the number of "weg"s
^<user.weg> [{user.count}]$: user.smart_delete(weg, "{count or '1'}")

^speichern$: edit.save()

(kopier|kopiere) das: edit.copy()
(schneide|schneidet) das aus: edit.cut()
füge das ein: edit.paste()
(mach|mache) rückgängig: edit.undo()
stelle wieder her: edit.redo()

# Navigation
geh hoch: edit.up()
geh hoch <user.number_small>:
    edit.up()
    repeat(number_small - 1)
geh runter: edit.down()
geh runter <user.number_small>:
    edit.down()
    repeat(number_small - 1) 
    
(spring|springe|springt|springen) links:
    edit.word_left()
(spring|springe|springt|springen) links <user.number_small>:
    edit.word_left()
    repeat(number_small - 1)
(spring|springe|springt|springen) rechts:
    edit.word_right()
(spring|springe|springt|springen) rechts <user.number_small>:
    edit.word_right()
    repeat(number_small - 1)
(spring|springe|springt|springen) zeilen anfang: edit.line_start()
(spring|springe|springt|springen) heimat: edit.line_start()
(spring|springe|springt|springen) zeilenende: edit.line_end()
(spring|springe|springt|springen) push: edit.line_end()

## Selection
(auswähle|auswählen) links:
    edit.extend_word_left()
(auswähle|auswählen) links <user.number_small>:
    edit.extend_word_left()
    repeat(number_small - 1)
(auswähle|auswählen) rechts:
    edit.extend_word_right()
(auswähle|auswählen) rechts <user.number_small>:
    edit.extend_word_right()
    repeat(number_small - 1)
    
(lösche|löschen) links:
    edit.extend_word_left()
    edit.delete()
(lösche|löschen) links <user.number_small>:
    edit.extend_word_left()
    repeat(number_small - 1)
    edit.delete()
(lösche|löschen) rechts:
    edit.extend_word_left()
    edit.delete()
(lösche|löschen) rechts <user.number_small>:
    edit.extend_word_right()
    repeat(number_small - 1)
    edit.delete()

löschtaste: key("backspace")