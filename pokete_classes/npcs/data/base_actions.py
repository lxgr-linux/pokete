from pokete_classes.npcs import NPCAction
from pokete_classes.npcs.npc_action import NPCInterface, UIInterface


class Chat(NPCAction):
    def act(self, npc: NPCInterface, ui: UIInterface):
        npc.chat()


base_actions: dict[str, NPCAction] = {"chat": Chat()}
