"""General use functions for Pokete"""

import sys
import release


def sort_vers(vers):
    """Sorts versions
    ARGS:
        vers: List of versions
    RETURNS:
        Sorted list"""
    return [k[-1] for k in
            sorted([([int(j) for j in i.split(".")], i) for i in vers])]


def print_help(path):
    """Shows help message
    ARGS:
        path: The game's path"""
    print(f"""Pokete {release.CODENAME} v{release.VERSION}
Usage: {path} (<options>)
Options:
    --log          : Enables logging
    --help         : Shows this help
    --no_mods      : Disables mods
    --no_audio     : Disables

Homepage: https://github.com/lxgr-linux/pokete

All save and logfiles are located in ~{release.SAVEPATH}/
Feel free to contribute.
See README.md for more information.
This software is licensed under the GPLv3, you should have gotten a
copy of it alongside this software.
Copyright (c) lxgr-linux <lxgr-linux@protonmail.com> 2022""")


def parse_args(args):
    """Parses command line args
    ARGS:
        args: Arguments given to the game
    RETURNS:
        Tuple of do_logging, load_mods and use_audio"""
    do_logging = False
    load_mods = True
    use_audio = True
    for arg in args[1:]:
        if arg == "--log":
            do_logging = True
        elif arg == "--no_mods":
            load_mods = False
        elif arg == "--no_audio":
            use_audio = False
        elif arg == "--help":
            print_help(args[0])
            sys.exit(0)
        else:
            print(f":: Error: '{arg}' is not a valid option! See '--help' for \
options.")
            sys.exit(1)
    return do_logging, load_mods, use_audio


if __name__ == "__main__":
    print("\033[31;1mDo not execute this!\033[0m")
