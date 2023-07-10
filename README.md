# Talon German
German Dictation Mode for the beta version of Talon Voice.

This is a fork of earlier setups, adding some improvements.

## Usage
Say `german` to switch from command mode to German dictation mode and `english` / `ego` to switch back.
Insert a quick german phrase with `(doitsu | nemetz) <german text>` (japanese / russian for "german").
Check out the _german.talon_ (and _german.py_) files for German commands.

## Improvements:
I added various improvements for myself. Check out _german.talon_ for more existing commands.

### Text editing and navigation
A handful of additional commands that make on-the-fly edits of text much more convenient.
especially:
* `springe links / rechts` will jump whole words in left / right direction
* `lösche links / rechts` will delete whole words in left / right direction
* `entferne links / rechts` will delete single chars in left / right direction
* `großgeschrieben` / `mach groß` helps fixing capitalization mistakes from vos
You can suffix most of these with a number to repeat them, for example `springe links 5`.

In addition to already existing `gehe rauf / runter / recht / links` for single char movements.

### Symbols
Some improvements regarding symbols - you can use more symbols and direct dictation now.
Also added more symbols I frequently used, for example `in Klammern` (` ()`), `Spiegelstrich` (` - `), `Ellipse` (`...`), `Schrägstrich oder` (` / `), `Zeilenumbruch`, `Leerzeichen` ...

### Improved robustness of commands with VOSK
Since registered commands have no influence on what VOSK detects (talon only gets the result after speech recognition), misdetections for commands can be a lot more common than with conformer.
I improved robustness of many of the commands by adding many of the common misrecognitions as possible alternatives.
Unfortunately, this makes my talon file a bit uglier to read, since something like "springe rechts" now turns into "(springe | sprenge | spring | sprang | ... ) rechts"

### German mode / quick german phrases
The previous setup allows you to dictate a quick german phrase from english mode without necessitating switching to german mode and back by appending your phrase to the `german` you produce to change modes (for example `german Hallo Welt`).
Note that the implementation for this is somewhat of hack and behavior might change with updates in talon or the english speech model.

Since I would sometimes switch into german mode when I did not want to all failed to remain in german mode (resulting in my german text getting interpreted as a bunch of english commands), I set up the quick german phrase and the german mode change to use different commands (there is also the fact that my german accent made the 'r' in 'german' a bit harder to recognize when quickly chaining):
* `german` switches to german mode and stays there.
* `doitsu` (japanese for german) or `nemetz` / `nemmy` (russian for german, I currently prefer this) will interpreted the following phrase as german and allow you to continue in english as before.

`english`, or short `ego` (japanese 'eigo' for english) switch back

### Quick access to configuration
Similar to knausj `customize ...`, following commands allow quick access to important configuration files:
* `[modifiziere | bearbeite] deutsche Wörter` opens a *additional_words_de.csv* file placed next to knausj *additional_words.csv*. Use this to add new words or fix misrecognitions as well as capitalisation mistakes coming from vosk. Note: actually, it works more like words_to_replace.csv, since it only replaces things that vosk recognized but cannot get it to recognize new stuff - I should rename that.
* `[modifiziere | bearbeite] deutsche Befehle` opens *german.talon*
The commands open a gvim instance.
Currently, the commands use a simple hard-coded path, so you will have to change that.


### Context sensitive dictation
Uses the knausj peek function, this keeps the behavior consistent and allows to make use of overloaded definitions for applications with special behavior.
Also introduced a setting `user.context_sensitive_dictation_german` that allows you to activate or deactivate this feature for german dictation (separately from english).

### Eye tracker control
You can control your eye tracker with the commands `Tracking (an | aus | Augen | Kopf | kalibrieren)`.

## Caveats:
* Only primitive capitalization
* Punctuation is less smart than knausj as well, especially if you do not use context sensitive dictation
* The usage of vosk limits you to what vosk recognizes - adding words or commands in your talon configuration will not influence vosk itself in any way, so you must match all phrases that vosk might hear (so while you might have to command "springe", Vosk might just as well recognize "spring" or "sprenge" instead).

## Todo:
* Currently uses absolute paths for csvs, use relative paths (perhaps switch to .talon-list)
* Remove custom *Clipscanner* clipboard implementation in favor of talon / knausj clipboard API
* better structure of commands, split into seperate files

## Dependencies
This is a plug-in for Talon Voice (https://talonvoice.com/).
Requires the [talon beta](https://www.patreon.com/lunixbochs) subscription for its support of additional speech engines.
Assumes [knausj](https://github.com/knausj85/knausj_talon) to be present in the talon user directory (for context sensitive dictation and as shared location for the *words_to_replace_de* csv).

## Setup
* download the newest German language model from [alphacephei][alphacephei] into `~/.talon/vosk/` or your preferred location:
  ```
  mkdir -p ~/.talon/vosk
  cd ~/.talon/vosk
  curl -LfSo vosk-model-de.zip https://alphacephei.com/vosk/models/vosk-model-de-0.21.zip
  unzip vosk-model-de.zip
  mv vosk-model-de-* vosk-model-de
  ```
  Note that there are models in different sizes, you can experiment with that.
* install vosk into the talon runtime by running `~/.talon/bin/pip install vosk` (on windows `scripts\pip install vosk`)
* clone this repository into your talon user folder (`~/.talon/user`)

It won't work on mac unless you sign the pip installed library file yourself, or unless aegis ships the vosk kaldi library with talon pre-signed.

## Related
Other related projects and repositories:
* [hanueles german port of knausj](https://github.com/hanuele/knausj_german) aims to offer a complete set of german commands mirroring knausj (not only limited to a dictation mode). Like this repo, requires knausj being present in the talon user directory. Seems to be less maintained though at the moment.

Also visit the [#language-deutsch](https://talonvoice.slack.com/archives/CURG8FXAQ) channel in the talon slack in case you have any questions or problems.


[alphacephei]: https://alphacephei.com/vosk/models
