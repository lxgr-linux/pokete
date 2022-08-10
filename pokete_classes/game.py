"""Contains exception to exit a game loop and enter a new"""


class MapChangeExeption(Exception):
    """Exception to exit a game loop and enter a new
    ARGS:
        _map: The new map to enter"""

    def __init__(self, _map):
        self.map = _map
        super().__init__(f"Map change to {_map.name}")


if __name__ == "__main__":
    print("\033[31;1mDo not execute this!\033[0m")
