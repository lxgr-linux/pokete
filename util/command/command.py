import sys

from .parse import parse


class Flag:
    def __init__(self, aliases: list[str], desc: str):
        self.aliases = aliases
        self.desc = desc

    def is_flag(self, flag: str):
        return flag in self.aliases


class Command:
    def __init__(
        self,
        name: str, desc: str,
        fn,
        flags: list[Flag] | None = None,
        commands: list["Command"] | None = None,
        additional_info: str = ""
    ):
        self.name = name
        self.desc = desc
        self.fn = fn
        self.flags = (flags if flags is not None else []) + [
            Flag(["-h", "--help"], "Shows help for a specific command")]
        self.additional_info = additional_info
        self.commands = commands if commands is not None else []

    def __print_help(self, ex: str):
        print(f"""{self.name} -- {self.desc}

Usage:
    {ex} [command] [options]... <flags>
{f"""
Options:
{"\n".join(f"\t{command.name}\t\t{command.desc}" for command in self.commands)}
""" if self.commands else ""}
{f"""
Flags:
{"\n".join(f"\t{"|".join(flag.aliases)}\t\t{flag.desc}" for flag in self.flags)}
""" if self.flags else ""}
{f"\n{self.additional_info}\n" if self.additional_info else ""}
Copyright (c) lxgr-linux <lxgr-linux@protonmail.com> 2024""")

    def run(self, ex: str, options: list[str],
            flags: dict[str, list[str]]):
        if options:
            for c in self.commands:
                if c.name == options[0]:
                    c.run(f"{ex} {options[0]}",
                          options[1:],
                          flags)
                    return
        all_flags = [i for f in self.flags for i in f.aliases]
        for flag in flags:
            if flag not in all_flags:
                print(
                    f":: Error: Unknown flag `{flag}`, "
                    f"try `{ex} --help`"
                )
                sys.exit(2)
        if "--help" in flags or "-h" in flags:
            self.__print_help(ex)
            sys.exit(0)
        else:
            self.fn(ex, options, flags)


class RootCommand(Command):
    def exec(self):
        args = sys.argv
        options, flags = parse(args)
        self.run(args[0], options, flags)
