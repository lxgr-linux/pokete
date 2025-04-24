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

    def test_parses_correctly_and_strings_with_suffix_and_multi_minus(self):
        version_str = "5.2.3-rc5-5"
        version = SemanticVersion.parse(version_str)

        self.assertEqual(version.major, 5)
        self.assertEqual(version.minor, 2)
        self.assertEqual(version.patch, 3)
        self.assertEqual(version.suffix, "rc5-5")
        self.assertEqual(str(version), version_str)

    def test_equals_are_equal(self):
        version_str = "5.2.3-rc5"
        self.assertTrue(
            SemanticVersion.parse(version_str) == SemanticVersion.parse(version_str)
        )

    def test_inequals_are_not_equal(self):
        self.assertFalse(
            SemanticVersion.parse("5.2.3-rc5") == SemanticVersion.parse("1.3.3-beta")
        )

    def test_major_greater(self):
        self.assertTrue(
            SemanticVersion.parse("1.2.3") > SemanticVersion.parse("0.3.2")
        )

    def test_minor_greater(self):
        self.assertTrue(
            SemanticVersion.parse("1.5.0") > SemanticVersion.parse("1.3.2")
        )

    def test_patch_greater(self):
        self.assertTrue(
            SemanticVersion.parse("1.5.3") > SemanticVersion.parse("1.5.2")
        )

    def test_equal_not_greater(self):
        self.assertFalse(
            SemanticVersion.parse("1.5.3") > SemanticVersion.parse("1.5.3")
        )

    def test_equal_not_smaller(self):
        self.assertFalse(
            SemanticVersion.parse("1.5.3") < SemanticVersion.parse("1.5.3")
        )

    def test_suffix_equal_not_greater(self):
        self.assertFalse(
            SemanticVersion.parse("1.5.3-rc") > SemanticVersion.parse("1.5.3-rc")
        )

    def test_rc_greater(self):
        self.assertTrue(
            SemanticVersion.parse("1.5.3-rc2") > SemanticVersion.parse("1.5.3-rc1")
        )

    def test_beata_greater(self):
        self.assertTrue(
            SemanticVersion.parse("1.5.3-beta5") > SemanticVersion.parse("1.5.3-beta2")
        )

    def test_alpha_greater(self):
        self.assertTrue(
            SemanticVersion.parse("1.5.3-alpha3") > SemanticVersion.parse("1.5.3-alpha1")
        )

    def test_rc_greater_beta(self):
        self.assertTrue(
            SemanticVersion.parse("1.5.3-rc2") > SemanticVersion.parse("1.5.3-beta60")
        )

    def test_rc_greater_alpha(self):
        self.assertTrue(
            SemanticVersion.parse("1.5.3-rc2") > SemanticVersion.parse("1.5.3-alpha")
        )

    def test_beta_greater_alpha(self):
        self.assertTrue(
            SemanticVersion.parse("1.5.3-beta1") > SemanticVersion.parse("1.5.3-alpha60")
        )

    def test_alpha_greater_bs(self):
        self.assertTrue(
            SemanticVersion.parse("1.5.3-alpha1") > SemanticVersion.parse("1.5.3-60")
        )
