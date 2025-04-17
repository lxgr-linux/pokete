import scrap_engine as se


class StdFrame(se.Frame):
    """Standardized frame
    ARGS:
        height: The frames height
        width: The frames width"""

    def __init__(self, height, width):
        super().__init__(width=width, height=height,
                         corner_chars=["┌", "┐", "└", "┘"],
                         horizontal_chars=["─", "─"],
                         vertical_chars=["│", "│"], state="float")


class StdFrame2(se.Frame):
    """Standardized frame
    ARGS:
        height: The frames height
        width: The frames width"""

    def __init__(self, height, width, state="solid"):
        super().__init__(width=width, height=height,
                         corner_chars=["_", "_", "|", "|"],
                         horizontal_chars=["_", "_"], state=state)
