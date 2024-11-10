from .item import FightItem
from .balls import PoketeBall, SuperBall, HyperBall
from .healing_potions import HealingPotion, SuperPotion
from .ap_potion import ApPotion

fight_items: dict[str|None, FightItem] = {
    "heal_potion": HealingPotion(),
    "super_potion": SuperPotion(),
    "poketeball": PoketeBall(),
    "superball": SuperBall(),
    "hyperball": HyperBall(),
    "ap_potion": ApPotion()
}
