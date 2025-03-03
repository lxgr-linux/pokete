from abc import ABC, abstractmethod

from pokete.classes.interactions.interactor_interface import InteractorInterface


class UIInterface(ABC):
    @abstractmethod
    def ask_bool(self, text: str) -> bool:
        pass

    @abstractmethod
    def ask_ok(self, text: str) -> None:
        pass

    @abstractmethod
    def choose_poke(self) -> str | None:
        pass


class NPCInterface(InteractorInterface, ABC):
    """Describes what NPCs are allowed to do, and what not"""

    @property
    @abstractmethod
    def used(self) -> bool:
        pass

    @abstractmethod
    def chat(self) -> None:
        pass

    @abstractmethod
    def give(self, name: str, item: str):
        pass

    @abstractmethod
    def set_used(self):
        pass

    @abstractmethod
    def unset_used(self):
        pass

    @abstractmethod
    def get(self, name: str) -> "NPCInterface":
        pass


class NPCAction(ABC):
    @abstractmethod
    def act(self, npc: NPCInterface, ui: UIInterface):
        pass
