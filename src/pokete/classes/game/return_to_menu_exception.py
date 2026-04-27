"""Contains exception to exit a game loop and return to main menu"""


class ReturnToMenuException(Exception):
    """Exception to exit the game loop and return to the main menu"""
    pass


if __name__ == "__main__":
    print("\033[31;1mDo not execute this!\033[0m")
