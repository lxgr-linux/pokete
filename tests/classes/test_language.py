from unittest import TestCase
from pathlib import Path
from pokete_classes.language import Language
from pokete_classes.constants import CWD


class TestLanguage(TestCase):
    def setUp(self) -> None:
        # Only directly instanced for this particular unit test
        self.language = Language("dummy")

    def test_get_language_entity(self):
        dummy_file_path: Path = (CWD / "assets" / "lang" / "schema.json").resolve()
        entity = self.language._get_language_entity("schema")
        self.assertEqual(entity.name, "schema")
        self.assertEqual(entity.path, dummy_file_path)

    def test_change_language(self):
        self.language.change_language("schema")
        self.assertEqual(self.language.str("title"), "Pokete Translation File Schema")

        with self.assertRaises(RuntimeWarning):
            self.language.str("invalid_key")

    def test_get_languages(self):
        langs = self.language.get_languages()
        self.assertEqual(langs, ["en_US"])
