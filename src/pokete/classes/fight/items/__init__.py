from .ap_potion import ApPotion
from .balls import HyperBall, PoketeBall, SuperBall
from .healing_potions import HealingPotion, SuperPotion
from .item import FightItem

fight_items: dict[str | None, FightItem] = {
    "heal_potion": HealingPotion(),
    "super_potion": SuperPotion(),
    "poketeball": PoketeBall(),
    "superball": SuperBall(),
    "hyperball": HyperBall(),
    "ap_potion": ApPotion(),
}
