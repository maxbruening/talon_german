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

phrase_stack = []


def on_pre_phrase(d):  phrase_stack.append(d)


def on_post_phrase(d): phrase_stack.pop()


speech_system.register('pre:phrase', on_pre_phrase)
speech_system.register('post:phrase', on_post_phrase)

mod.setting("german_unicode",
            type=int,
            default=1,
            desc="Enable proper unicode punctuation")

ctx.lists["user.letter"] = {
    "alpha": "a",
    "bravo": "b",
    "charlie": "c",
    "delta": "d",
    "echo": "e",
    "foxtrott": "f",
    "golf": "g",
    "hotel": "h",
    "india": "i",
    "julia": "j",
    "kilo": "k",
    "lima": "l",
    "mike": "m",
    "november": "n",
    "oskar": "o",
    "papa": "p",
    "québec": "q",
    "romeo": "r",
    "sierra": "s",
    "tango": "t",
    "uniform | uniformen": "u",
    "viktor": "v",
    "whisky": "w",
    "x ray": "x",
    "junkie": "y",
    "zulu": "z",
    "ära": "ä",
    "ökonom | ökonomen": "ö",
    "übermut": "ü",
    "s z": "ß",
}

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


@mod.action_class
class Actions:
    def enable_german_unicode():
        """enable proper unicode punctuation"""
        ctx.settings["user.german_unicode"] = 1

    def disable_german_unicode():
        """disable proper unicode punctuation"""
        ctx.settings["user.german_unicode"] = 0

    def smart_insert(txt: str):
        """context-aware insertion"""

        text = ""

        # delete whatever is currently selected
        actions.key(" ")
        actions.key("backspace")

        with ClipScanner() as clip:

            # scan left side of the cursor
            clip.clear()
            actions.edit.extend_left()
            before = clip.get_selection().strip()
            if before != "":
                actions.edit.extend_right()

            # scan right side of the cursor
            clip.clear()
            actions.edit.extend_right()
            after = clip.get_selection().strip()
            if after != "":
                actions.edit.extend_left()

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
