import re
import sys

from .changelog import write_changelog
from .appimage import write_appimage
from .release_py import write_release_py
from pokete.util.command import not_enough_args

TAG_REGEX = r"^v([0-9]+)\.([0-9]+)\.([0-9]+)(-[0-9A-Za-z-]+)?$"


def __release(tag: str):
    print(":: Writing appstream data...")
    write_changelog(tag)
    print(":: Writing appimage builder file...")
    write_appimage(tag)
    print(":: Writing release.py...")
    write_release_py(tag)


def __is_tag_valid(tag: str) -> bool:
    return re.fullmatch(TAG_REGEX, tag) is not None


def main(
    ex: str, options: list[str],
    flags: dict[str, list[str]]
):
    if len(options) == 0:
        not_enough_args(ex)
    else:
        tag = options[0]
        if not __is_tag_valid(tag):
            print(
                ":: Error: Invalid tag, "
                f"try `{ex} --help`"
            )
            sys.exit(2)
        __release(tag)
