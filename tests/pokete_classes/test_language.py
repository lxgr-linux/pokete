from unittest import TestCase
from unittest.mock import patch
from pokete_classes.language import Language
from pokete_classes.settings import Settings, Setting


class TestLanguage(TestCase):
    @patch("pokete_classes.settings.Settings")
    def setUp(self, mock_settings: Settings) -> None:
        # Only directly instanced for this particular unit test
        self.mock = mock_settings
        self.mock.get.return_value = Setting("language", "schema")
        self.language = Language(self.mock, "schema")

    def test_language_code(self):
        code = self.language.language_code
        self.assertEqual(2, self.mock.get.call_count)
        self.assertEqual(self.mock.get("language").val, code)

    def test_change_language(self):
        self.assertEqual("Pokete Translation File Schema", self.language.str("title"))

        # with self.assertRaises(RuntimeWarning):
        #    self.language.str("invalid_key")

    def test_get_languages(self):
        langs = self.language.get_languages()
        self.assertCountEqual(["en_US", "de_DE"], langs)
