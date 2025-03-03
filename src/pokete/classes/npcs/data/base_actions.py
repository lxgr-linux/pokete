from pokete.classes.npcs import NPCAction
from pokete.classes.npcs.npc_action import NPCInterface, UIInterface


class Heal(NPCAction):
    def act(self, npc: NPCInterface, ui: UIInterface):
        npc.ctx.figure.heal()


class Chat(NPCAction):
    def act(self, npc: NPCInterface, ui: UIInterface):
        npc.chat()


base_actions: dict[str, NPCAction] = {"chat": Chat(), "heal": Heal()}
