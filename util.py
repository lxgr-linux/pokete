import sys
from util import parse, gen_wiki, prepare_pages


def show_help(name: str):
    print(f"""{name} -- Pokete utility
Usage:
    {name} [command] [options]... <flags>
    
Commands:
    wiki\t\tGenerates wiki.md
    prpare-pages\tPrepares github pages
    release\t\tCreates a release commit
    help\t\tShows this help
    
Flags:
    --help\t\tShows help for a specific command

Copyright (c) lxgr-linux <lxgr-linux@protonmail.com> 2024""")


def main():
    args = sys.argv
    command, options, flags = parse(args)

    arg_tup = (args[0], command, options, flags)

    match command:
        case "help":
            show_help(args[0])
        case "wiki":
            gen_wiki(*arg_tup)
        case "prepare-pages":
            prepare_pages(*arg_tup)
        case _:
            if "--help" in flags:
                show_help(args[0])
            else:
                print(
                    f":: Error: Command '{command}' not found, "
                    f"try `{args[0]} help`"
                )
                sys.exit(2)


if __name__ == "__main__":
    main()
