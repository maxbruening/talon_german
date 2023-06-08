language: en_US
-
#^(german | deutsch | nemetz)$:
# keep 'nemetz' for quick german phrases only to avoid getting stuck in german
# mode when this was not intended
^(german | deutsch)$:
	mode.disable("command")
	mode.enable("user.german")

^(english | ego | pego)$: skip()

# doizy (jp doitsu = deutsch / german) conflicts with dot
# nemetz (ru = german) works great, no conflicts
# nemmy conflicts with mimi
^(doizy | nemetz | nemmy) <phrase>$:
    user.vosk_recognize_german(phrase)
