import scrap_engine as se
from ...language import _
from ...loops import std_loop, easy_exit_loop
from ...hotkeys import get_action, ACTION_DIRECTIONS, Action
from ...language import Language
from ...ui_elements import BetterChooseBox
from ...movemap import Movemap

HARDCODED_LANGUAGE_NAMES = {
    "en_US": "English",
    "de_DE": "German"
}


class LanguageOverlay(BetterChooseBox):

    def __init__(self):
        super(LanguageOverlay, self).__init__(
            4,
            [se.Text(" ")],
            name="Languages"
        )
        self.language = Language.instance()

    def __call__(self, _map: Movemap):
        available_languages = self.language.get_languages()
        languages = []

        for language in available_languages:
            key = f"ui.lang.{str(language).lower()}"
            languages.append(se.Text(f"({HARDCODED_LANGUAGE_NAMES[language]}) {_(key)}"))

        self.set_items(4, languages)

        self.map = _map
        with self:
            while True:
                action = get_action()

                if action.triggers(*ACTION_DIRECTIONS):
                    self.input(action)
                elif action.triggers(Action.CANCEL):
                    break
                elif action.triggers(Action.ACCEPT):
                    item = self.get_item(*self.index).ind
                    self.language.change_language(available_languages[item])

                std_loop()
                self.map.show()
