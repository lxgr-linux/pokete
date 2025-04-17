from pokete.base.context import Context
from pokete.base.exception_propagation import exception_propagating_periodic_event
from pokete.base.periodic_event_manager import PeriodicEventManager
from .pokete_care import PoketeCare
from .. import timer
from ..npcs import NPCAction
from ..npcs.npc_action import NPCInterface, UIInterface
from .dummy import DummyFigure
from ..poke import EvoMap, Poke


class PoketeCareNPCAction(NPCAction):
    def __init__(self, care: PoketeCare):
        self.care: PoketeCare = care

    def act(self, npc: NPCInterface, ui: UIInterface):
        if self.care.poke is None:
            npc.text(["Here you can leave one of your Poketes for some time \
and we will train it."])
            if ui.ask_bool(
                "Do you want to put a Pokete into the Pokete-Care?"
            ):
                if (index := ui.choose_poke()) is not None:
                    self.care.poke = npc.ctx.figure.pokes[index]
                    self.care.entry = timer.time.time
                    npc.ctx.figure.add_poke(Poke("__fallback__", 0), index)
                    npc.text(["We will take care of it."])
        else:
            add_xp = int((timer.time.time - self.care.entry) / 30)
            self.care.entry = timer.time.time
            self.care.poke.add_xp(add_xp)
            npc.text(["Oh, you're back.", f"Your {self.care.poke.name} \
gained {add_xp}xp and reached level {self.care.poke.lvl()}!"])
            if ui.ask_bool("Do you want it back?"):
                dummy = DummyFigure(self.care.poke)
                evomap = EvoMap(npc.ctx.map.height, npc.ctx.map.width)
                while evomap(
                    Context(PeriodicEventManager([exception_propagating_periodic_event]), npc.ctx.map,
                            npc.ctx.overview, dummy),
                    dummy.pokes[0]
                ):
                    continue
                npc.ctx.figure.add_poke(dummy.pokes[0])
                npc.ctx.figure.caught_pokes += dummy.caught_pokes
                npc.text(["Here you go!", "Until next time!"])
                self.care.poke = None
        npc.text(["See you!"])
