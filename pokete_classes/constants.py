from pathlib import Path

# Holds the path to the main pokete folder. Every path related task should be
# referring to this constant to get access to all the internal files. READ-ONLY
CWD: Path = Path(__file__).parents[1]

# Standard fallback language code
FALLBACK_LANGUAGE = "en_US"
