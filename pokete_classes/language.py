from __future__ import annotations
from pathlib import Path
import json
import locale
from .color import Color
from .constants import CWD
from .settings import settings


HARDCODED_LANGUAGE_NAMES = {
    "en_US": "English",
    "de_DE": "German"
}


def get_system_locale() -> str:
    """
    Fetches the main language of the user's operating system.

    Returns: ISO language code
    """
    locale.setlocale(locale.LC_ALL, "")
    return locale.getlocale(locale.LC_CTYPE)[0]


class Language:
    """
    Class for loading and managing translation files.
    """

    def __init__(self, default_lang=None):
        self._old_language_code = self.language_code
        self._language_file: dict = dict()
        self.language_path: Path = CWD / "assets" / "lang"
        self._load_language_file()

    @property
    def language_code(self):
        return settings("language").val

    def str(self, key: str) -> str:
        """
        Fetch a localized string at from the currently used language.

        Args:
            key: Identifier of the string to fetch

        Returns: Localized string
        """
        if self._old_language_code != self.language_code:
            self._old_language_code = self.language_code
            self._load_language_file()

        if key in self._language_file:
            return str(self._language_file.get(key))

        # Temporarily - So previous code is not broken
        return key

        # raise RuntimeWarning(f"No entry with key '{key}' was found in the
        # translation file '{self.language.path}'")

    def get_languages(self) -> list:
        """
        Fetches and returns a list of all available language files.

        Returns: List of available language files in the assets directory
        """
        available_languages = []

        for item in self.language_path.glob("*.json"):
            if item.is_file():
                language_name = item.name.replace(".json", "")

                if language_name != "schema":
                    available_languages.append(language_name)

        return available_languages

    def _load_language_file(self) -> None:
        """
        Loads the language file into the internal dictionary.

        Args:
            language_path: Path to the language file
        """

        language_path = self.language_path / f"{self.language_code}.json"

        # if not (language_path.exists() and language_path.is_file()):


        with open(language_path, encoding="utf-8") as language_file:
            self._language_file = json.load(language_file)


# For convenient use later in the program ~ origin
# _ = Language.instance().str
lang = Language()

if __name__ == "__main__":
    print(f"\033[31;1mDo not execute this!{Color.reset}")
