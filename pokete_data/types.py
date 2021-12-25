types = {
    "normal": {
        "effective": [],
        "ineffective": [],
        "color": [],
    },
    "stone": {
        "effective": ["flying", "fire"],
        "ineffective": ["plant"],
        "color": ["grey"]
    },
    "plant": {
        "effective": ["stone", "ground", "water"],
        "ineffective": ["fire", "ice"],
        "color": ["green"]
    },
    "water": {
        "effective": ["stone", "flying", "fire"],
        "ineffective": ["plant", "ice"],
        "color": ["lightblue"]
    },
    "fire": {
        "effective": ["flying", "plant", "undead", "ice"],
        "ineffective": ["stone", "water"],
        "color": ["thicc", "red"]
    },
    "ground": {
        "effective": ["normal"],
        "ineffective": ["flying", "ice"],
        "color": ["grey"]
    },
    "electro": {
        "effective": ["stone", "flying"],
        "ineffective": ["ground"],
        "color": ["thicc", "yellow"]
    },
    "flying": {
        "effective": ["plant"],
        "ineffective": ["stone"],
        "color": ["thicc"]
    },
    "undead": {
        "effective": ["normal", "ground", "plant", "water", "poison"],
        "ineffective": ["fire"],
        "color": ["purple"]
    },
    "ice": {
        "effective": ["water", "plant", "ground"],
        "ineffective": ["fire"],
        "color": ["cyan"]
    },
    "poison": {
        "effective": ["normal"],
        "ineffective": ["undead"],
        "color": ["thicc", "green"]
    },
}


sub_types = ["bird", "snake"]


if __name__ == "__main__":
    print("\033[31;1mDo not execute this!\033[0m")
