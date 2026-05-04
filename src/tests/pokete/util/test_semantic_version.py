from pokete.util.semantic_version import SemanticVersion


def test_parses_correctly_and_strings():
    version_str = "4.1.3"
    version = SemanticVersion.parse(version_str)

    assert version.major == 4
    assert version.minor == 1
    assert version.patch == 3
    assert version.suffix is None
    assert str(version) == version_str


def test_parses_correctly_and_strings_with_suffix():
    version_str = "5.2.3-rc5"
    version = SemanticVersion.parse(version_str)

    assert version.major == 5
    assert version.minor == 2
    assert version.patch == 3
    assert version.suffix == "rc5"
    assert str(version) == version_str


def test_parses_correctly_and_strings_with_suffix_and_multi_minus():
    version_str = "5.2.3-rc5-5"
    version = SemanticVersion.parse(version_str)

    assert version.major == 5
    assert version.minor == 2
    assert version.patch == 3
    assert version.suffix == "rc5-5"
    assert str(version) == version_str


def test_equals_are_equal():
    version_str = "5.2.3-rc5"
    assert SemanticVersion.parse(version_str) == SemanticVersion.parse(version_str)


def test_inequals_are_not_equal():
    assert not (
        SemanticVersion.parse("5.2.3-rc5") == SemanticVersion.parse("1.3.3-beta")
    )


def test_major_greater():
    assert SemanticVersion.parse("1.2.3") > SemanticVersion.parse("0.3.2")


def test_minor_greater():
    assert SemanticVersion.parse("1.5.0") > SemanticVersion.parse("1.3.2")


def test_patch_greater():
    assert SemanticVersion.parse("1.5.3") > SemanticVersion.parse("1.5.2")


def test_equal_not_greater():
    assert not (SemanticVersion.parse("1.5.3") > SemanticVersion.parse("1.5.3"))


def test_equal_not_smaller():
    assert not (SemanticVersion.parse("1.5.3") < SemanticVersion.parse("1.5.3"))


def test_suffix_equal_not_greater():
    assert not (SemanticVersion.parse("1.5.3-rc") > SemanticVersion.parse("1.5.3-rc"))


def test_rc_greater():
    assert SemanticVersion.parse("1.5.3-rc2") > SemanticVersion.parse("1.5.3-rc1")


def test_beata_greater():
    assert SemanticVersion.parse("1.5.3-beta5") > SemanticVersion.parse("1.5.3-beta2")


def test_alpha_greater():
    assert SemanticVersion.parse("1.5.3-alpha3") > SemanticVersion.parse("1.5.3-alpha1")


def test_rc_greater_beta():
    assert SemanticVersion.parse("1.5.3-rc2") > SemanticVersion.parse("1.5.3-beta60")


def test_rc_greater_alpha():
    assert SemanticVersion.parse("1.5.3-rc2") > SemanticVersion.parse("1.5.3-alpha")


def test_beta_greater_alpha():
    assert SemanticVersion.parse("1.5.3-beta1") > SemanticVersion.parse("1.5.3-alpha60")


def test_alpha_greater_bs():
    assert SemanticVersion.parse("1.5.3-alpha1") > SemanticVersion.parse("1.5.3-60")
