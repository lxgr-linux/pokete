import re
import sys

from util.changelog import write_changelog

TAG_REGEX = r"^v([0-9]+)\.([0-9]+)\.([0-9]+)(-[0-9A-Za-z-]+)?$"


def __release(tag: str):
    write_changelog()
    pass


def __is_tag_valid(tag: str) -> bool:
    return re.fullmatch(TAG_REGEX, tag) is not None


def show_help(ex: str, command: str):
    print(f"""{ex} {command} -- Prepare all relevant files for release
Usage:
    {ex} {command} [tag] <flags>
    
Tags have to follow the `vMAJOR.MINOR.PATCH-RELEASE` semantic.

Flags:
    --help\t\tShows help for a specific command

Copyright (c) lxgr-linux <lxgr-linux@protonmail.com> 2024""")


def main(
    ex: str, command: str, options: list[str],
    flags: dict[str, list[str]]
):
    if "--help" in flags:
        show_help(ex, command)
    elif len(options) == 0:
        print(
            ":: Error: Not enough arguments, a tag has to be given, "
            f"try `{ex} {command} help`"
        )
        sys.exit(2)
    else:
        tag = options[0]
        if not __is_tag_valid(tag):
            print(
                ":: Error: Invalid tag, "
                f"try `{ex} {command} help`"
            )
            sys.exit(2)
        __release(tag)
