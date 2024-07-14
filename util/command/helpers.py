import sys


def not_found(ex, option):
    print(
        f":: Error: Command '{option}' not found, "
        f"try `{ex} --help`"
    )
    sys.exit(2)


def not_enough_args(ex):
    print(
        ":: Error: Not enough arguments, "
        f"try `{ex} --help`"
    )
    sys.exit(2)
