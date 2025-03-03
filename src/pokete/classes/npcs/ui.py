from pokete.base.input_loops import ask_bool, ask_ok
from pokete.classes import deck
from pokete.classes.landscape import MapInteract
from pokete.classes.npcs.npc_action import UIInterface


class UI(UIInterface):
    def __init__(self, npc: MapInteract):
        self.__npc: MapInteract = npc

    def ask_bool(self, text: str) -> bool:
        return ask_bool(self.__npc.ctx, text)

    def ask_ok(self, text: str) -> None:
        ask_ok(self.__npc.ctx, text)

    def choose_poke(self) -> str | None:
        return deck.deck(self.__npc.ctx, 6, "Your deck", True)
