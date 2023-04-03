import csv
import os
from pathlib import Path
from talon import Context, Module, resource

ctx = Context()
ctx.matches = """
mode: user.german
language: de_DE
"""

mod = Module()

# NOTE: This method requires this module to be one folder below the top-level
#   knausj folder.
SETTINGS_DIR: Path = Path(__file__).parents[1] / "knausj_talon" / "settings"

if not SETTINGS_DIR.is_dir():
    os.mkdir(SETTINGS_DIR)


def get_list_from_csv(
        filename: str, headers: tuple[str, str], default: dict[str, str] = {}
):
    """Retrieves list from CSV"""
    path = SETTINGS_DIR / filename
    assert filename.endswith(".csv")

    if not path.is_file():
        with open(path, "w", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            for key, value in default.items():
                writer.writerow([key] if key == value else [value, key])

    # Now read via resource to take advantage of talon's
    # ability to reload this script for us when the resource changes
    with resource.open(str(path), "r") as f:
        rows = list(csv.reader(f))

    # print(str(rows))
    mapping = {}
    if len(rows) >= 2:
        actual_headers = rows[0]
        if not actual_headers == list(headers):
            print(
                f'"{filename}": Malformed headers - {actual_headers}.'
                + f" Should be {list(headers)}. Ignoring row."
            )
        for row in rows[1:]:
            if len(row) == 0:
                # Windows newlines are sometimes read as empty rows. :champagne:
                continue
            if len(row) == 1:
                output = spoken_form = row[0]
            else:
                output, spoken_form = row[:2]
                if len(row) > 2:
                    print(
                        f'"{filename}": More than two values in row: {row}.'
                        + " Ignoring the extras."
                    )
            # Leading/trailing whitespace in spoken form can prevent recognition.
            spoken_form = spoken_form.strip()
            mapping[spoken_form] = output

    return mapping


_default_vocabulary = {
    "N map": "nmap",
    "under documented": "under-documented",
}

# "user.vocabulary" is used to explicitly add words/phrases that Talon doesn't
# recognize. Words in user.vocabulary (or other lists and captures) are
# "command-like" and their recognition is prioritized over ordinary words.
mod.list("vocabulary_german", desc="additional german vocabulary words")

additional_words = get_list_from_csv(
    "additional_words_de.csv",
    headers=("Word(s)", "Spoken Form (If Different)"),
    default=_default_vocabulary,
)
ctx.lists["user.vocabulary_german"] = additional_words

@ctx.capture("user.vocabulary_german", rule='({user.vocabulary_german})')
def vocabulary_german(m) -> str:
    """user vocabulary"""
    return str(m)

# Always capitalize words that are defined in this file
always_capitalized_words = get_list_from_csv(
    "capitalized_words_de_custom.csv",
    headers=("Word(s)"),
    default={},
)
ctx.lists["user.always_capitalized_words_german"] = always_capitalized_words

