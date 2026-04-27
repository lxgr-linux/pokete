import sys


def not_found(ex, option):
    print(f":: Error: Command '{option}' not found, try `{ex} --help`")
    sys.exit(2)


def not_enough_args(ex):
    print(f":: Error: Not enough arguments, try `{ex} --help`")
    sys.exit(2)
