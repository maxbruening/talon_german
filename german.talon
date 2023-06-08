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

# Why copy and paste this to here? Ensuring these commands apply to the german
# mode as well should be all that is needed.
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

#######################################################################
## Misc Editing
#######################################################################
neue zeile | zeilenumbruch: key("enter")
(nächste Zeile | slap | slab | snap | SAP | schlapp):
    edit.line_end()
    key("enter")
neuer absatz:
  key("enter")
  key("enter")

leerzeichen: " "
schrägstrich oder: " / "

(Spiegelstrich | spiegel strich): " - "

(in | end | eins | fans | tanz | dein | ein) klammern:
    " ()"
    edit.left()
großgeschrieben | groß geschrieben | grossgeschrieben | mach groß | ausgeschrieben:
    edit.select_word()
    user.formatters_reformat_selection("title")

#######################################################################
## Editor Commands
#######################################################################
datei speichern: edit.save()
^speichern$: edit.save()
(kopier|kopiere) das: edit.copy()
(schneide|schneidet) das aus: edit.cut()
füge das ein: edit.paste()
((mach|mache) rückgängig | nop | nap): edit.undo()
((mach|mache) rückgängig | nop | nap) <user.number_small>:
    edit.undo()
    repeat(number_small - 1)
(nop | knopp | nap) das: user.clear_last_phrase()
^ob das$: user.clear_last_phrase()
stelle wieder her: edit.redo()

#######################################################################
## Navigation
#######################################################################
# small movements
(geh | gehe | g) (hoch | rauf): edit.up()
(geh | gehe | g) (hoch | rauf) <user.number_small>:
    edit.up()
    repeat(number_small - 1)
(geh | gehe | g) runter: edit.down()
(geh | gehe | g) runter <user.number_small>:
    edit.down()
    repeat(number_small - 1)
(geh | gehe | g) links: edit.left()
(geh | gehe | g) links <user.number_small>:
    edit.left()
    repeat(number_small - 1)
(geh | gehe | g) rechts: edit.right()
(geh | gehe | g) rechts <user.number_small>:
    edit.right()
    repeat(number_small - 1)

# large movements
(spring|spreng|sprang|springe|sprüche|spenge|spring die|springer|springt|springen) links:
    edit.word_left()
(spring|spreng|sprang|springe|sprüche|spenge|spring die|springer|springt|springen) links <user.number_small>:
    edit.word_left()
    repeat(number_small - 1)
(spring|spreng|sprang|springe|sprüche|spenge|spring die|springer|springt|springen) rechts:
    edit.word_right()
(spring|spreng|sprang|springe|sprüche|spenge|spring die|springer|springt|springen) rechts <user.number_small>:
    edit.word_right()
    repeat(number_small - 1)
(spring|spreng|sprang|springe|sprüche|spenge|spring die|sprenger|springer|springt|springen) zeilen anfang: edit.line_start()
(spring|spreng|sprang|springe|sprüche|spenge|spring die|sprenger|springer|springt|springen) ganz links: edit.line_start()
(spring|spreng|sprang|springe|sprüche|spenge|spring die|sprenger|springer|springt|springen) heimat: edit.line_start()
(spring|spreng|sprang|springe|sprüche|spenge|spring die|sprenger|springer|springt|springen) (band|Ben): edit.line_start()
(spring|spreng|sprang|springe|sprüche|spenge|spring die|sprenger|springer|springt|springen) zeilenende: edit.line_end()
(spring|spreng|sprang|springe|sprüche|spenge|spring die|sprenger|springer|springt|springen) push: edit.line_end()
(spring|spreng|sprang|springe|sprüche|spenge|spring die|sprenger|springer|springt|springen) ganz rechts: edit.line_end()
(spring|spreng|sprang|springe|sprüche|spenge|spring die|sprenger|springer|springt|springen|sprengel) (land|event|blend|rent|nennt|lent|lähmt|lernt|lend): edit.line_end()

#######################################################################
## Selecting Text
#######################################################################
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

#######################################################################
## Deleting Text
#######################################################################
# "weg" should only be recognized when it's not part of a sentence or
# using token for counting the number of "weg"s
^<user.weg> [{user.count}]$: user.smart_delete(weg, "{count or '1'}")
löschtaste: key("backspace")

(lösche|ohrlöcher|erlösche|bresche|lasche|wäsche|löschen|löcher) links:
    edit.extend_word_left()
    edit.delete()
(lösche|ohrlöcher|erlösche|bresche|lasche|wäsche|löschen|löcher) links <user.number_small>:
    edit.extend_word_left()
    repeat(number_small - 1)
    edit.delete()
(lösche|ohrlöcher|erlösche|bresche|lasche|wäsche|löschen|löcher) ganz links:
    edit.extend_line_start()
    edit.delete()
(entferne) links:
    edit.delete()
(lösche|ohrlöcher|erlösche|bresche|lasche|wäsche|löschen|löcher) rechts:
    edit.extend_word_right()
    edit.delete()
(lösche|ohrlöcher|erlösche|bresche|lasche|wäsche|löschen|löcher) rechts <user.number_small>:
    edit.extend_word_right()
    repeat(number_small - 1)
    edit.delete()
(lösche|ohrlöcher|erlösche|bresche|lasche|wäsche|löschen|löcher) ganz rechts:
    edit.extend_line_end()
    edit.delete()
(entferne) rechts:
    key("delete")
(lösche|ohrlöcher|erlösche|bresche|lasche|wäsche|löschen|löcher) zeile: edit.delete_line()

#######################################################################
## Talon
#######################################################################
# TODO: create talon setting for location of german settings directory
(bearbeite|wer arbeitet|bearbeitet|bearbeitete|gearbeitet|modifiziere|modifiziert) (deutsche|deutscher|solche) (wörter|wetter|blätter|better|pater):
    user.edit_text_file("/home/markus/.talon/user/knausj_talon/settings/additional_words_de.csv")
    sleep(500ms)
    edit.file_end()
(bearbeite|wer arbeitet|bearbeitet|bearbeitete|gearbeitet|modifiziere|modifiziert) (deutsche|deutscher|solche) befehle:
    user.edit_text_file("/home/markus/.talon/user/talon_german/german.talon")
    sleep(500ms)
    edit.file_end()

# Disable / enable pop noise. Relies on custom knausj action from me
# no pop
noob | no pop: user.disable_pop()
# yes pop
jazz pop | jessup | jetzt Pop | Jacob: user.enable_pop()
