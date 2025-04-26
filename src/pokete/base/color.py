"""Contains the color class"""
from os import environ


class Color:
    """Color class that provides all needed escape codes"""
    reset = "\033[0m"
    thicc = "\033[1m"
    underlined = "\033[4m"
    grey = "\033[1;30m"
    red = "\033[38;5;196m"
    green = "\033[38;5;70m"
    yellow = "\033[38;5;226m"
    lightblue = "\033[1;34m"
    blue = "\033[34m"
    purple = "\033[1;35m"
    cyan = "\033[1;36m"
    lightgrey = "\033[37m"
    white = "\033[1;37m"

    # extended color palette
    brown = "\033[38;5;88m"
    lakeblue = "\033[38;5;33m"
    mediumgrey = "\033[38;5;238m"
    brightyellow = "\033[38;5;155m"
    deepgreen = "\033[38;5;35m"
    brightgreen = "\033[38;5;46m"
    darkgreen = "\033[38;5;29m"
    gold = "\033[38;5;94m"
    cavegrey = "\033[38;5;236m"
    peach = "\033[38;5;216m"

    if environ.get("TERM", "linux") == "linux":  # this fixes some colors on TTY
        gold = "\033[38;5;9m"
        cavegrey = "\033[38;5;7m"


if __name__ == "__main__":
    print("\033[31;1mDo not execute this!\033[0m")
