from pokete.classes.asset_service.resources.base import ItemDict

items: dict[str, ItemDict] = {
    "poketeball": {
        "pretty_name": "Poketeball",
        "desc": "A ball you can use to catch Poketes",
        "price": 2,
        "fn": "poketeball",
        "usable_in_duel": False,
    },
    "superball": {
        "pretty_name": "Superball",
        "desc": "A ball you can use to catch Poketes with an increased chance",
        "price": 10,
        "fn": "superball",
        "usable_in_duel": False,
    },
    "hyperball": {
        "pretty_name": "Hyperball",
        "desc": "For catching Poketes with a waaay higher chance",
        "price": None,
        "fn": "hyperball",
        "usable_in_duel": False,
    },
    "healing_potion": {
        "pretty_name": "Healing potion",
        "desc": "Heals a Pokete with 5 HP",
        "price": 15,
        "fn": "heal_potion",
        "usable_in_duel": True,
    },
    "super_potion": {
        "pretty_name": "Super potion",
        "desc": "Heals a Pokete with 15 HP",
        "price": 25,
        "fn": "super_potion",
        "usable_in_duel": True,
    },
    "ap_potion": {
        "pretty_name": "AP potion",
        "desc": "Refills the Poketes attack APs.",
        "price": 100,
        "fn": "ap_potion",
        "usable_in_duel": True,
    },
    "treat": {
        "pretty_name": "Treat",
        "desc": "Upgrades a Pokete by a whole level.",
        "price": None,
        "fn": None,
        "usable_in_duel": False,
    },
    "shut_the_fuck_up_stone": {
        "pretty_name": "'Shut the fuck up' stone",
        "desc": "Makes trainer leaving you alone",
        "price": None,
        "fn": None,
        "usable_in_duel": True,
    },
}

if __name__ == "__main__":
    print("\033[31;1mDo not execute this!\033[0m")
