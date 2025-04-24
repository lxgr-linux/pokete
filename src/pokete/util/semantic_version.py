from typing import Optional


class SemanticVersion:
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
