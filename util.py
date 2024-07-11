#!/usr/bin/env python3

import sys
from util import gen_wiki, prepare_after, prepare_before, make_release, \
    install
from util.arguments import RootCommand, Command, not_found, not_enough_args


def fallback(ex: str, options: list[str],
             flags: dict[str, list[str]]):
    if not options:
        not_enough_args(ex)
    not_found(ex, options[0])


def main():
    c = RootCommand(
        "util",
        "Pokete utility",
        fallback,
        commands=[
            Command("install", "Install pokete to a given directory", install),
            Command(
                "prepare-pages", "Prepares github pages", fallback,
                commands=[
                    Command("before", "Actions run pre branch switch",
                            prepare_before),
                    Command("after", "Actions run post branch switch",
                            prepare_after)
                ]
            ),
            Command("release", "Creates a release", make_release),
            Command("wiki", "Generate a markdown wiki", gen_wiki)
        ]
    )

    c.exec()


if __name__ == "__main__":
    main()
