import unicodedata

from talon import Context, Module, actions, settings, speech_system
from talon.grammar import Phrase

from .clipscanner import ClipScanner

mod = Module()

mod.mode("german", desc="german language mode")

ctx = Context()
ctx.matches = """
mode: user.german
language: /.*/
"""
ctx.settings = {
    'speech.engine': 'vosk',
    'speech.language': 'de_DE',
    'speech.timeout': 0.3
}

ctx = Context()
ctx.matches = """
mode: user.german
language: de_DE
"""

setting_context_sensitive_dictation_german = mod.setting(
    "context_sensitive_dictation_german",
    type=bool,
    default=False,
    desc="Look at surrounding text to improve auto-capitalization/spacing in dictation mode. By default, this works by selecting that text & copying it to the clipboard, so it may be slow or fail in some applications.",
)

phrase_stack = []


def on_pre_phrase(d):  phrase_stack.append(d)


def on_post_phrase(d): phrase_stack.pop()


speech_system.register('pre:phrase', on_pre_phrase)
speech_system.register('post:phrase', on_post_phrase)

mod.setting("german_unicode",
            type=int,
            default=1,
            desc="Enable proper unicode punctuation")

letters = {
    "alt": "a",
    "bett": "b",
    "kap": "c",
    "kapp": "c",
    "cap": "c",
    "cup": "c",
    "drum": "d",
    "echt": "e",
    "fein": "f",
    "feind": "f",
    "gast": "g",
    "hab": "h",
    "hat": "h",
    "hart": "h",
    "ich": "i",
    "j": "j",
    "kennt": "k",
    "kent": "k",
    "kind": "k",
    "look": "l",
    "luck": "l",
    "met": "m",
    "mit": "m",
    "not": "n",
    "oft": "o",
    "pitt": "p",
    "kuh": "q",
    "rad": "r",
    "rat": "r",
    "rate": "r",
    "raten": "r",
    "sinn": "s",
    "tipp": "t",
    "ulf": "u",
    "von": "v",
    "wall": "w",
    "plex": "x",
    "chunky": "y",
    "junkie": "y",
    "tanki": "y",
    "z": "z",
    "ähnlich": "ä",
    "öl": "ö",
    "übel": "ü",
    "üben": "ü",
    "s z": "ß",
}
letters.update({v: v for v in letters.values()})

ctx.lists["user.letter"] = letters

ctx.lists["user.number_key"] = {
    "null": "0",
    "eins": "1",
    "zwei": "2",
    "drei": "3",
    "vier": "4",
    "fünf": "5",
    "sechs": "6",
    "sieben": "7",
    "acht": "8",
    "neun": "9",
    "komma": ",",
    "punkt": ".",
}

ctx.lists["user.punctuation"] = {
    "leerzeichen": "␣",  # will become spaces after all substitutions
    "blank": "␣",
    "blink": "␣",
    "plenk": "␣",
    "planck": "␣",
    "beistrich": ",",  # komma is often confused with komme
    "bei strich": ",",  # komma is often confused with komme
    "beiß dich": ",",  # komma is often confused with komme
    "beißt nicht": ",",  # komma is often confused with komme
    "beistriche": ",",  # komma is often confused with komme
    "punkt": ".",
    "ellipse": "...",
    "semikolon": ";",
    "doppelpunkt": ":",
    "schrägstrich": "/",
    "fragezeichen": "?",
    "ausrufezeichen": "!",
    "sternchen": "*",
    "bindestrich": "-",
    "gedankenstrich": "–",
    "unterstrich": "_",
    "raute": "#",
    "prozent": "%",
    "at zeichen": "@",
    "klammeraffe": "@",
    "und zeichen": "&",

    "dollar zeichen": "$",
    "dollarzeichen": "$",
    "pfund zeichen": "£",
    "pfundzeichen": "£",
    "euro zeichen": "€",
    "eurozeichen": "€",
}

ctx.lists["user.symbol_key"] = {
    "leerzeichen": "␣",  # will become spaces after all substitutions
    "blank": "␣",
    "blink": "␣",
    "plenk": "␣",
    "planck": "␣",
    "beistrich": ",",  # komma is often confused with komme
    "bei strich": ",",  # komma is often confused with komme
    "beistriche": ",",  # komma is often confused with komme
    "punkt": ".",
    "semikolon": ";",
    "doppelpunkt": ":",
    "schrägstrich": "/",
    "fragezeichen": "?",
    "ausrufezeichen": "!",
    "sternchen": "*",
    "bindestrich": "-",
    "gedankenstrich": "–",
    "unterstrich": "_",
    "raute": "#",
    "prozent": "%",
    "at zeichen": "@",
    "klammeraffe": "@",
    "und zeichen": "&",

    "dollar zeichen": "$",
    "pfund zeichen": "£",
    "euro zeichen": "€",

    "backslash": "\\",
    "senkrecht strich": "|",
    "zitat": '„',
    "zitat ende": '“',
    "halbes zitat": '‚',
    "halbes zitat ende": '‘',
    "apostroph": "’",
    "klammer auf": "(",
    "klammer zu": ")",
    "eckige klammer auf": "[",
    "eckige klammer zu": "]",
    "geschweifte klammer auf": "{",
    "geschweifte klammer zu": "}",
    "kleiner zeichen": "<",
    "größer zeichen": ">",
    "ist gleich zeichen": "=",
    "tilde": "~",
    "zirkumflex": "^",
}

mod.list("number", desc="Words for a positive nonzero number")
number_words = {
    "eins": "1",
    "zwei": "2",
    "drei": "3",
    "vier": "4",
    "fünf": "5",
    "sechs": "6",
    "sieben": "7",
    "acht": "8",
    "neun": "9",
    "zehn": "10",
}
number_words.update({str(i): str(i) for i in range(10)})
ctx.lists["self.number"] = number_words

@mod.capture
def number_small(m) -> int:
    """A small number"""

@ctx.capture(
    "user.number_small", rule=f"({'|'.join(number_words.keys())})"
)
def number_small(m) -> int:
    return int(number_words[str(m)])


mod.list("count", desc="Words for a positive nonzero count of actions")
count_words = {
    "einfach": "1",
    "zweifach": "2",
    "dreifach": "3",
    "vierfach": "4",
    "fünffach": "5",
    "sechsfach": "6",
    "siebenfach": "7",
    "achtfach": "8",
    "neunfach": "9",
    "zehnfach": "10",
}
ctx.lists["self.count"] = count_words

@mod.capture
def count_small(m) -> int:
    """A small count of instances of actions"""

@ctx.capture(
    "user.count_small", rule=f"({'|'.join(count_words.keys())})"
)
def count_small(m) -> int:
    return int(count_words[str(m)])

_space_after = ".,!?:;)]}–“‘$£€"
_no_space_before = ".,-!?:;)]}␣“‘’$£€"
_ascii_replace = {'–': '-', '„': '"', '“': '"', "‚": "'", "‘": "'", "’": "'"}
_capitalize_after = ".!?"

mod.list("modifier", desc="Modifiers for upper casement")
ctx.lists["self.modifier"] = {
    "schiff": "CAP",  # groß often becomes große/großer/großes
    "schiffs": "CAP",
    "schifft": "CAP",
    "holzschiff": "ALLCAPS",  # hold shift
    "zwerg": "LOWER",
}

@mod.capture
def vocabulary_german(m: str) -> str:
    """user vocabulary"""

@mod.capture
def wort(m: str) -> str:
    """word or spelled word or number, inserts space in the end"""


@mod.capture
def gk_wort(m: str) -> str:
    """potentially upper case word"""


@mod.capture
def satzglied(m: str) -> str:
    """word or symbol"""


@mod.capture
def satz(m: str) -> str:
    """sentence"""


@mod.capture
def weg(m: str, count: str) -> str:
    """capture multiple "weg"s"""

@mod.capture
def acronym(m: str) -> str:
    """an acronym composed of multiple letters"""


@mod.action_class
class Actions:
    def smart_insertion(txt: str) -> str:
        """handles context-aware insertion"""

        text = ""

        before, after = actions.user.dictation_peek(left=True, right=True)
        # the following checks only use the first char
        before = before[-1] if len(before) > 0 else before
        after = after[0] if len(after) > 0 else after

        squeeze_into_word = before != "" and unicodedata.category(before)[0] == 'L' \
                            and after != "" and unicodedata.category(after)[0] == 'L'

        if before != "" \
                and (unicodedata.category(before)[0] == 'L' or before in _space_after) \
                and txt[0] not in _no_space_before \
                and not squeeze_into_word:
            text += " "

        if before in _capitalize_after or before == "":
            txt = txt[0].upper() + txt[1:]

        if settings.get("user.german_unicode") == 0:
            ascii = txt
            for c in _ascii_replace:
                ascii = ascii.replace(c, _ascii_replace[c])
            text += ascii
        else:
            text += txt

        if (
                after != ""
                and (
                txt[-1] in _space_after
                or unicodedata.category(txt[-1])[0] == 'L'
        )
                and after not in ' \n\t'
                and after not in _no_space_before
                and not squeeze_into_word
        ):
            text += " "
        return text


    def insert(txt: str):
        """text insertion"""

        # delete whatever is currently selected
        # note: this behavior leads to missing spaces in vim as a delete in vim sometimes takes multiple
        # spaces at once (-> investigate!)
        #actions.key(" ")
        #actions.key("backspace")

        text = txt
        if setting_context_sensitive_dictation_german.get():
            text = actions.user.smart_insertion(text)
        actions.user.add_phrase_to_history(text)
        actions.insert(text)

    def smart_delete(txt: str, count: str):
        """delete word and optionally space"""

        with ClipScanner() as clip:
            for i in range(len(str(txt).split())):
                for j in range(int(count)):
                    # first just delete all spaces until next word
                    clip.clear()
                    actions.edit.extend_word_left()
                    before = clip.get_selection()
                    if before != '' and before[-1] in [" ", "\n"]:
                        actions.edit.extend_word_right()
                        actions.key("backspace")
                        continue

                    # if there were none, delete next word
                    actions.key("backspace")

                    # delete spaces before that as well
                    clip.clear()
                    actions.edit.extend_left()
                    before = clip.get_selection()
                    if before in [" ", "\n"]:
                        actions.key("backspace")
                    elif before != '':
                        actions.edit.extend_right()

    def vosk_recognize_german(phrase: Phrase):
        """Replay speech into vosk"""
        # NOTE: this is pretty much all considered an experimental API
        # and this script is just for demo purposes, for the beta only
        current_phrase = phrase_stack[-1]
        ts = current_phrase['_ts']
        start = phrase.words[0].start - ts
        # NOTE: might have to tweak this depending on engine / model if words
        # get lost or parts of "german" appear (as in "an")
        start = max(0, start - 0.2)
        end = phrase.words[-1].end - ts
        samples = current_phrase['samples']
        pstart = int(start * 16_000)
        pend = int(end * 16_000)
        samples = samples[pstart:pend]
        actions.mode.enable("user.german")
        try:
            # NOTE: the following API is completely private and subject to change with no notice
            speech_system._on_audio_frame(samples)
            # Change command history entry
            german_text = actions.user.history_get(0)
            phrase_text = actions.user.history_transform_phrase_text(phrase.words)
            command = actions.user.history_get(1).removesuffix(phrase_text)
            actions.user.history_set(1, command + german_text)
            actions.user.history_set(0, None)
        finally:
            actions.mode.disable("user.german")
