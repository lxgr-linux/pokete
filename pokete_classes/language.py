from __future__ import annotations
from pathlib import Path
import json
import locale
from .entities.language_entity import LanguageEntity
from .color import Color


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

    __instance = None

    @classmethod
    def instance(cls) -> Language:
        """
        Returns: Singleton instance of language class
        """
        if Language.__instance is None:
            Language.__instance = Language()
        return Language.__instance

    def __init__(self, default_lang=None):
        self._language_file: dict = dict()
        self.language: LanguageEntity = LanguageEntity()
        self.language_path: Path = self.language.path.parent
        self.change_language(default_lang or get_system_locale())

    def str(self, key: str) -> str:
        """
        Fetch a localized string at from the currently used language.

        Args:
            key: Identifier of the string to fetch

        Returns: Localized string
        """
        if key in self._language_file:
            return str(self._language_file.get(key))

        # Temporarily - So previous code is not broken
        return key

        # raise RuntimeWarning(f"No entry with key '{key}' was found in the
        # translation file '{self.language.path}'")

    def change_language(self, language: str) -> LanguageEntity:
        """
        Changes the current language. If parsed language identifier is invalid
        then the fallback language 'en_US' will be used.

        Args:
            language: Language file to look for

        Returns: Language entity. Will fall back to 'en_US' if no translation
        file has been found.
        """
        self.language = self._get_language_entity(language)
        self._load_language_file(self.language.path)
        return self.language

    def get_selected_language(self) -> LanguageEntity:
        """
        Returns

        Returns: Selected language
        """
        return self.language

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

    def _get_language_entity(self, language: str) -> LanguageEntity:
        """
        This method will return a language entity, which contains its name
        and its absolute path.

        Args:
            language: Language file to look for

        Returns: Language entity. Will fall back to 'en_US' if no translation
        file has been found.
        """
        entity = LanguageEntity()

        language_file = self.language_path / f"{language}.json"

        if language_file.exists() and language_file.is_file():
            entity = LanguageEntity(language, language_file.resolve())

        return entity

    def _load_language_file(self, language_path: Path) -> None:
        """
        Loads the language file into the internal dictionary.

        Args:
            language_path: Path to the language file
        """
        with open(language_path, encoding="utf-8") as language_file:
            self._language_file = json.load(language_file)


# For convenient use later in the program ~ origin
_ = Language.instance().str

if __name__ == "__main__":
    print(f"\033[31;1mDo not execute this!{Color.reset}")
