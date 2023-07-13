language: en_US
-
^(german | deutsch)$:
	mode.disable("command")
	mode.enable("user.german")

^(english | ego | pego)$: skip()

^(nimitz) <phrase>$:
    user.vosk_recognize_german(phrase)
