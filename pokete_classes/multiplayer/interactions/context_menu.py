from ..remote_fight import remote_fight
from ..communication import com_service
from ...context import Context
from ...input_loops import ask_ok
from ...interactions import MultiTextChooseBox
from ...multiplayer.pc_manager import pc_manager

OPTION_FIGHT = "Fight"
OPTION_TRADE = "Trade"
OPTION_QUIT = "Quit..."


class ContextMenu:
    def __init__(self):
        self.menu = MultiTextChooseBox(
            [OPTION_FIGHT, OPTION_TRADE, OPTION_QUIT],
            "Interact"
        )

    def __call__(self, ctx: Context):
        rmtpl = pc_manager.get_interactable(ctx.figure)
        if rmtpl is None:
            return
        match self.menu(ctx):
            case "Fight":
                resp = com_service.request_fight(rmtpl.name)
                #ask_ok(ctx, f"{resp}")
                if resp:
                    remote_fight.start(rmtpl.ctx)
            case "Trade":
                pass
            case "Quit...":
                pass
