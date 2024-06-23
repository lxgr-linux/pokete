import os
import sys


def show_help(ex: str, command: str):
    print(f"""{ex} {command} -- Install pokete to a given directory
Usage:
    {ex} {command} [dest] <flags>

Flags:
    --help\tShows help for a specific command

Copyright (c) lxgr-linux <lxgr-linux@protonmail.com> 2024""")


def install(ex: str, command: str, options: list[str],
            flags: dict[str, list[str]]):
    if "--help" in flags:
        show_help(ex, command)
    elif len(options) == 0:
        print(
            ":: Error: Not enough arguments, a destination has to be given, "
            f"try `{ex} {command} --help`"
        )
        sys.exit(2)
    else:
        dest = options[0]
        print(os.popen(f'sh -c "./util/install.sh {dest}"').read())
