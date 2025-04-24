import unittest

from pokete.util.semantic_version import SemanticVersion


class SemanticVersionTest(unittest.TestCase):
    def test_parses_correctly_and_strings(self):
        version_str = "4.1.3"
        version = SemanticVersion.parse(version_str)

        self.assertEqual(version.major, 4)
        self.assertEqual(version.minor, 1)
        self.assertEqual(version.patch, 3)
        self.assertIsNone(version.suffix)
        self.assertEqual(str(version), version_str)

    def test_parses_correctly_and_strings_with_suffix(self):
        version_str = "5.2.3-rc5"
        version = SemanticVersion.parse(version_str)

        self.assertEqual(version.major, 5)
        self.assertEqual(version.minor, 2)
        self.assertEqual(version.patch, 3)
        self.assertEqual(version.suffix, "rc5")
        self.assertEqual(str(version), version_str)
