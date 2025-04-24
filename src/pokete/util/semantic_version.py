from functools import total_ordering
from typing import Optional


@total_ordering
class SemanticVersion:
    __suffix_order = ("rc", "beta", "alpha")

    def __init__(
        self, major: int, minor: int, patch: int,
        suffix: Optional[str] = None
    ):
        self.major = major
        self.minor = minor
        self.patch = patch
        self.suffix = suffix

    @classmethod
    def parse(cls, version_str: str) -> "SemanticVersion":
        splid = version_str.split("-")
        prefix = splid[0]
        suffix: Optional[str] = (a if (a := "-".join(splid[1:])) != "" else None)

        (major, minor, patch) = (int(i) for i in prefix.split("."))

        return cls(major, minor, patch, suffix)

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}{
            ("-"+self.suffix) if self.suffix is not None else ""
        }"

    def __eq__(self, value) -> bool:
        other: "SemanticVersion" = value
        return other.major == self.major and \
            other.minor == self.minor and \
            other.patch == self.patch and \
            other.suffix == self.suffix

    def __gt__(self, other: "SemanticVersion") -> bool:
        for s, o in zip((self.major, self.minor, self.patch), (other.major, other.minor, other.patch)):
            if s > o:
                return True
            elif s < o:
                return False
        if self.suffix == other.suffix:
            return False
        elif self.suffix is None:
            return True
        elif other.suffix is None:
            return False
        for suffix in self.__suffix_order:
            if self.suffix.startswith(suffix):
                if other.suffix.startswith(suffix):
                    return int(self.suffix.strip(suffix)) > int(other.suffix.strip(suffix))
                return True
        return self.suffix > other.suffix
