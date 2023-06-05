import os

from talon import Context, actions

ctx = Context()
ctx.matches = """
mode: user.german
language: de_DE
"""

# dictionary for capitalization
path = os.path.dirname(os.path.abspath(__file__))
with open(path + "/dictionary/german.dic") as f:
    list_of_words = f.read().split("\n")

dict_of_words = {}
for word in list_of_words:
    if word.lower() in dict_of_words:
        # multiple entries, use lower:
        dict_of_words[word.lower()] = word.lower()
    else:
        dict_of_words[word.lower()] = word

_space_after = ".,!?:;)]}–“‘$£€"
_no_space_before = ".,-!?:;)]}␣“‘’$£€"
_ascii_replace = {'–': '-', '„': '"', '“': '"', "‚": "'", "‘": "'", "’": "'"}
_capitalize_after = ".!?"




@ctx.capture("user.wort", rule='({user.number_key}+ | <user.vocabulary_german> | <word>)')
def wort(m) -> str:
    """word or spelled word or number, inserts space in the end"""
    return ''.join(str(m).split()) + ' '


@ctx.capture("user.gk_wort", rule='[{user.modifier}] <user.wort>')
def gk_wort(m) -> str:
    """potentially upper case word"""
    word = " ".join(m[1:])
    if m[0] == "CAP":
        return actions.user.formatted_text(word, "CAPITALIZE_ALL_WORDS")
    elif m[0] == "ALLCAPS":
        return actions.user.formatted_text(word, "ALL_CAPS")
    elif m[0] == "LOWER":
        return actions.user.formatted_text(word, "ALL_LOWERCASE")
    else:
        word = str(m)
        key = word.replace(" ", "")
        if key in dict_of_words:
            return dict_of_words[key] + " "
        else:
            return word


@ctx.capture("user.satzglied", rule='(<user.gk_wort> | {user.punctuation} | {user.symbol_key})')
def satzglied(m) -> str:
    """word or symbol"""
    if str(m)[0] in _space_after:
        return str(m) + ' '
    else:
        return str(m)


@ctx.capture("user.satz", rule='<user.satzglied>+')
def satz(m) -> str:
    """sentence"""
    result = [str(m[0])]
    for i in range(1, len(m)):
        if str(m[i])[0] in _no_space_before and result[i - 1][-1] == ' ':
            result[i - 1] = result[i - 1][:-1]
        result.append(str(m[i]))
    result = ''.join(result)

    if result[-1] == ' ':
        result = result[:-1]

    result = result.replace('␣', ' ')
    return result


@ctx.capture("user.weg", rule='weg+')
def weg(m) -> str:
    """capture multiple "weg"s"""
    return str(m)


@ctx.capture("user.acronym", rule="{user.letter}+")
def acronym(m: str) -> str:
    return "".join(m.letter_list).upper()
