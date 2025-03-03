import os
import sys


def install(ex: str, options: list[str],
            flags: dict[str, list[str]]):
    if len(options) == 0:
        print(
            ":: Error: Not enough arguments, a destination has to be given, "
            f"try `{ex} {options} --help`"
        )
        sys.exit(2)
    else:
        dest = options[0]
        print(os.popen(f'sh -c "./pokete.util/pokete.utility/install.sh {dest}"').read())
