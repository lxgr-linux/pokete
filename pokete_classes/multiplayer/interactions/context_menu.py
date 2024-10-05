from ...context import Context
from ...interactions import MultiTextChooseBox
from ...multiplayer.pc_manager import pc_manager


class ContextMenu:
    def __init__(self):
        self.menu = MultiTextChooseBox(
            ["Fight", "Trade", "Quit..."],
            "Interact"
        )

    def __call__(self, ctx: Context):
        rmtpl = pc_manager.get_interactable(ctx.figure)
        if rmtpl is None:
            return
        self.menu(ctx)
