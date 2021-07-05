types = {
    "normal": {
        "effective": [],
        "ineffective": [],
        "color": None,
    },
    "stone": {
        "effective": ["flying", "fire"],
        "ineffective": ["plant"],
        "color": "Color.grey"
    },
    "plant": {
        "effective": ["stone", "ground", "water"],
        "ineffective": ["fire", "ice"],
        "color": "Color.green"
    },
    "water": {
        "effective": ["stone", "flying", "fire"],
        "ineffective": ["plant", "ice"],
        "color": "Color.lightblue"
    },
    "fire": {
        "effective": ["flying", "plant", "undead", "ice"],
        "ineffective": ["stone", "water"],
        "color": "Color.thicc+Color.red"
    },
    "ground": {
        "effective": ["normal"],
        "ineffective": ["flying"],
        "color": "Color.grey"
    },
    "electro": {
        "effective": ["stone", "flying"],
        "ineffective": ["ground"],
        "color": "Color.thicc+Color.yellow"
    },
    "flying": {
        "effective": ["plant"],
        "ineffective": ["stone"],
        "color": "Color.thicc"
    },
    "undead": {
        "effective": ["normal", "ground", "plant", "water"],
        "ineffective": ["fire"],
        "color": "Color.purple"
    },
    "ice": {
        "effective": ["water", "plant"],
        "ineffective": ["fire"],
        "color": "Color.white"
    },
}


if __name__ == "__main__":
    print("\033[31;1mDo not execute this!\033[0m")
