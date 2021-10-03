"""Contains the color class"""


class Color:
    """Color class that provides all needed escape codes"""
    reset = "\033[0m"
    thicc = "\033[1m"
    underlined = "\033[4m"
    grey = "\033[1;30m"
    red = "\033[31m"
    green = "\033[32m"
    yellow = "\033[33m"
    lightblue = "\033[1;34m"
    blue = "\033[34m"
    purple = "\033[1;35m"
    cyan = "\033[1;36m"
    lightgrey = "\033[37m"
    white = "\033[1;37m"


if __name__ == "__main__":
    print("\033[31;1mDo not execute this!\033[0m")
