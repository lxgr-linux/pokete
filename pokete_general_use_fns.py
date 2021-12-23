"""General use functions for Pokete"""
import sys
import release


def liner(text, width, pre=""):
    """Wraps a string after a certain length and respects word endings"""
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
    """Wraps a string after a certain length"""
    ret = ""
    for i in range(int(len(name) / l_len) + 1):
        ret += name[i * l_len:(i + 1) * l_len] + ("\n"
                                                  if i != int(len(name) / l_len)
                                                  else "")
    return ret


def sort_vers(vers):
    """Sorts versions"""
    return [k[-1] for k in
            sorted([([int(j) for j in i.split(".")], i) for i in vers])]


def std_loop(ev):
    """Standart action executed in most loops"""
    if ev.get() == "exit":
        raise KeyboardInterrupt


def print_help(path):
    """Shows help message"""
    print(f"""Pokete {release.CODENAME} v{release.VERSION}
Usage: {path} (<options>)
Options:
    --log     : Enables logging
    --help    : Shows this help
    --no_mods : Disables mods

Homepage: https://github.com/lxgr-linux/pokete

All save and logfiles are located in ~{release.SAVEPATH}/
Feel free to contribute.
See README.md for more information.
Copyright (c) lxgr-linux <lxgr-linux@protonmail.com> 2021""")


def parse_args(args):
    """Parses command line args"""
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
