"""General use functions for Pokete"""

import sys
import release


def liner(text, width, pre=""):
    """Wraps a string after a certain length and respects word endings
    ARGS:
        text: The text that should be lined
        width: The max width
        pre: Prefix that will be added in the next line
    RETURNS:
        The lined string"""
    lens = 0
    out = ""
    for name in text.split(" "):
        if "\n" in name:
            lens = len(pre)
            out += name + pre
        elif lens+len(name) + 1 <= width:
            out += name + " "
            lens += len(name) + 1
        else:
            lens = len(name) + 1 + len(pre)
            out += "\n" + pre + name + " "
    return out


def hard_liner(l_len, name):
    """Wraps a string after a certain length
    ARGS:
        name: The String
        l_len: The max length
    RETURNS:
        The lined string"""
    ret = ""
    for i in range(int(len(name) / l_len) + 1):
        ret += name[i * l_len:(i + 1) * l_len] + ("\n"
                                                  if i != int(len(name) / l_len)
                                                  else "")
    return ret


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
        Tuple of do_logging and load_mods"""
    do_logging = False
    load_mods = True
    for arg in args[1:]:
        if arg == "--log":
            do_logging = True
        elif arg == "--no_mods":
            load_mods = False
        elif arg == "--help":
            print_help(args[0])
            sys.exit(0)
        else:
            print(f":: Error: '{arg}' is not a valid option! See '--help' for \
options.")
            sys.exit(1)
    return do_logging, load_mods


if __name__ == "__main__":
    print("\033[31;1mDo not execute this!\033[0m")
