from pathlib import Path
from dataclasses import dataclass
from ..constants import CWD


@dataclass(frozen=True)
class LanguageEntity:
    """
    Stores general information about a language. This is READ-ONLY so this
    data class is marked as frozen to prevent accidental writes.
    """
    name: str = "en_US"
    path: Path = (CWD / "assets" / "lang" / "en_US.json").resolve()
