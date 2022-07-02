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

neue zeile: key("enter")
neuer absatz:
  key("enter")
  key("enter")

# "weg" should only be recognized when it's not part of a sentence or
# using token for counting the number of "weg"s
^<user.weg> [{user.count}]$: user.smart_delete(weg, "{count or '1'}")

<user.satz>: user.smart_insert(satz)

^speichern$: edit.save()

(kopier|kopiere) das: edit.copy()
(schneide|schneidet) das aus: edit.cut()
füge das ein: edit.paste()
mache rückgängig: edit.undo()
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