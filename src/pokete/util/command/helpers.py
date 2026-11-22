import sys


def not_found(ex: str, option: str) -> None:
    print(f":: Error: Command '{option}' not found, try `{ex} --help`")
    sys.exit(2)


def not_enough_args(ex: str) -> None:
    print(f":: Error: Not enough arguments, try `{ex} --help`")
    sys.exit(2)
