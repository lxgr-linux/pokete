#!/usr/bin/env python3

from pokete.util.command import Command, RootCommand, not_enough_args, not_found
from pokete.util.utility import (
    export,
    gen_wiki,
    install,
    make_release,
    prepare_after,
    prepare_before,
    validate,
    wiki,
)


def fallback(ex: str, options: list[str], flags: dict[str, list[str]]):
    if not options:
        not_enough_args(ex)
    not_found(ex, options[0])


def main():
    c = RootCommand(
        "util",
        "Pokete utility",
        fallback,
        commands=[
            Command(
                "install",
                "Install pokete to a given directory",
                install,
                usage="[dest]",
            ),
            Command(
                "prepare-pages",
                "Prepares github pages",
                fallback,
                commands=[
                    Command(
                        "before",
                        "Actions run pre branch switch",
                        prepare_before,
                    ),
                    Command(
                        "after", "Actions run post branch switch", prepare_after
                    ),
                ],
            ),
            Command(
                "export",
                "Exports data from the game files",
                fallback,
                commands=[
                    Command(
                        "base-assets",
                        "Exports base assets",
                        export.export_base_data,
                        flags=[export.out_flag],
                    ),
                ],
            ),
            Command(
                "release",
                "Prepare all relevant files for release",
                make_release,
                additional_info="Tags have to follow the `vMAJOR.MINOR.PATCH-RELEASE` semantic.",
                usage="[tag]",
            ),
            Command(
                "wiki",
                "Generate a markdown wiki",
                gen_wiki,
                flags=[
                    wiki.silent_flag,
                    wiki.quiet_flag,
                    wiki.verbose_flag,
                    wiki.single_flag,
                    wiki.multi_flag,
                    wiki.pics_flag,
                ],
            ),
            Command("validate-data", "Validates pokete_data", validate),
        ],
    )

    c.exec()


if __name__ == "__main__":
    main()
