from pokete.classes.asset_service.service import asset_service
from pokete.classes.npcs import NPCAction
from pokete.classes.npcs.npc_action import NPCInterface, UIInterface
from pokete.classes.poke import Poke


class GiveBasic(NPCAction):
    def __init__(self, name: str, item: str):
        self.name = name
        self.item = item

    def act(self, npc: NPCInterface, ui: UIInterface):
        npc.give(self.name, self.item)


class Playmap17Boy(NPCAction):
    def act(self, npc: NPCInterface, ui: UIInterface):
        if "choka" in [i.identifier for i in npc.ctx.figure.pokes[:6]]:
            npc.text(["Oh, cool!", "You have a Choka!",
                      "I've never seen one before!",
                      "Here you go, have $200!"])
            if ui.ask_bool(
                "The young boy gifted you $200. Do you want to accept it?"
            ):
                npc.ctx.figure.add_money(200)
            npc.set_used()
        else:
            npc.text(["In this region lives the Würgos Pokete.",
                      f"At level {asset_service.get_base_assets().pokes['würgos'].evolve_lvl} \
It evolves into Choka.",
                      "I have never seen one before!"])


class Playmap13introductor(NPCAction):
    def act(self, npc: NPCInterface, ui: UIInterface):
        if not npc.get("Last Trainer").used:
            npc.text(
                [
                    "To get to the other side of this building, "
                    "you have to win some epic fights against Deepest "
                    "Forests' best trainers!", "This won't be easy!"
                ]
            )
        else:
            npc.text(
                [
                    "It looks like you've been succesfull!",
                    "Congrats!"
                ]
            )
            npc.set_used()


class Playmap20Trader(NPCAction):
    def act(self, npc: NPCInterface, ui: UIInterface):
        if (index := ui.choose_poke()) is None:
            return
        poke = Poke("ostri", 500)
        npc.ctx.figure.add_poke(poke, index)
        npc.set_used()
        ui.ask_ok(
            f"You received: {poke.name.capitalize()}"
            f" at level {poke.lvl()}.",
        )
        npc.text(["Cool, huh?"])


class Playmap23Npc8(NPCAction):
    def act(self, npc: NPCInterface, ui: UIInterface):
        if ui.ask_bool(
            "The man gifted you $100. Do you want to accept it?",
        ):
            npc.set_used()
            npc.ctx.figure.add_money(100)


class Playmap39Npc25(NPCAction):
    def act(self, npc: NPCInterface, ui: UIInterface):
        if not npc.get("Leader Sebastian").used:
            npc.text(["I can't let you go!",
                      "You first have to defeat our arena leader!"])
            npc.ctx.figure.set(npc.ctx.figure.x + 1, npc.ctx.figure.y)
        else:
            npc.text(["Have a pleasant day."])


class Playmap43Npc23(NPCAction):
    def act(self, npc: NPCInterface, ui: UIInterface):
        if ui.ask_bool("Do you also want to have one?"):
            npc.ctx.figure.pokes.append(Poke("mowcow", 2000))
            npc.set_used()


class Playmap42Npc21(NPCAction):
    def act(self, npc: NPCInterface, ui: UIInterface):
        poke_list = [i for i in npc.ctx.figure.pokes[:6]
                     if i.lvl() >= 50 and i.identifier == "mowcow"]
        if len(poke_list) > 0:
            poke = poke_list[0]
            npc.text(["Oh great!", "You're my hero!",
                      f"You brought me a level {poke.lvl()} Mowcow!",
                      "I'm thanking you!",
                      "Now I can still serve the best MowCow-Burgers!",
                      "Can I have it?"])
            if ui.ask_bool(
                "Do you want to give your Mowcow to the cook?"
            ):
                npc.ctx.figure.pokes[npc.ctx.figure.pokes.index(poke)] = Poke(
                    "__fallback__", 0)
                npc.text(["Here you go, have $1000!"])
                if ui.ask_bool(
                    "The cook gifted you $1000. "
                    "Do you want to accept it?",
                ):
                    npc.ctx.figure.add_money(1000)
                npc.set_used()
        else:
            npc.text(["Ohhh man...", "All of our beef is empty...",
                      "How are we going to serve the best MowCow-Burgers "
                      "without beef?",
                      "If only someone here could bring me a fitting "
                      "Mowcow!?",
                      "But it has to be at least on level 50 to meet our "
                      "high quality standards.",
                      "I will pay a good price!"])


actions: dict[str, NPCAction] = {
    "playmap_10_old_man": GiveBasic("Old man", "hyperball"),
    "playmap_29_ld_man": GiveBasic("The man", "ld_flying"),
    "playmap_32_npc_12": GiveBasic("Old man", "hyperball"),
    "playmap_36_npc_14": GiveBasic("Old woman", "ap_potion"),
    "playmap_37_npc_15": GiveBasic("Bert the bird", "super_potion"),
    "playmap_39_npc_20": GiveBasic("Gerald the farmer", "super_potion"),
    "playmap_47_npc_26": GiveBasic("Poor man", "healing_potion"),
    "playmap_48_npc_27": GiveBasic("Old geezer", "ld_the_old_roots_hit"),
    "playmap_49_npc_28": GiveBasic("Candy man", "treat"),
    "playmap_17_boy": Playmap17Boy(),
    "playmap_20_trader": Playmap20Trader(),
    "playmap_23_npc_8": Playmap23Npc8(),
    "playmap_39_npc_25": Playmap39Npc25(),
    "playmap_43_npc_23": Playmap43Npc23(),
    "playmap_42_npc_21": Playmap42Npc21(),
}
