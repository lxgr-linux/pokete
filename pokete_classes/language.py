from __future__ import annotations
from pathlib import Path
import json
import locale
from .color import Color
from .constants import CWD, FALLBACK_LANGUAGE
from .settings import Settings, settings

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

    def __init__(self, _settings: Settings, default_code=None):
        self.settings = _settings
        self._old_language_code = default_code or self.language_code
        self._language_file: dict = dict()
        self._fallback_file: dict | None = None
        self.language_path: Path = CWD / "assets" / "lang"
        self._load_language_file()

    @property
    def language_code(self):
        return self.settings.get("language").val

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
        else:
            if self._fallback_file is None:
                self._load_language_file_fallback()

            if key in self._fallback_file:
                return str(self._fallback_file.get(key))

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
        """
        self._language_file = self.__load_language_file_generic(self.language_code)

    def _load_language_file_fallback(self) -> None:
        """
        Loads the fallback language file into internal dictionary. It will be
        accessed if translation keys are missing from the currently used translation.
        """
        self._fallback_file = self.__load_language_file_generic(FALLBACK_LANGUAGE)

    def __load_language_file_generic(self, filename: str) -> dict:
        """
        Loads a language file and returns its content as dictionary.
        """
        language_path = self.language_path / f"{filename}.json"

        if language_path.exists() and language_path.is_file():
            with open(language_path, encoding="utf-8") as file:
                return json.load(file)

        raise RuntimeError("No language file with code "
                           f"'{filename}' found in path "
                           f"'{language_path}'.")


# For convenient use later in the program ~ origin
# Dependency injection for code testing
lang = Language(settings)

if __name__ == "__main__":
    print(f"\033[31;1mDo not execute this!{Color.reset}")
