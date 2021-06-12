types = {
    "normal": {
        "effective": [],
        "ineffective": []
    },
    "stone": {
        "effective": ["flying", "fire"],
        "ineffective": ["plant"]
    },
    "plant": {
        "effective": ["stone", "ground", "water"],
        "ineffective": ["fire"]
    },
    "water": {
        "effective": ["stone", "flying", "fire"],
        "ineffective": ["plant"]
    },
    "fire": {
        "effective": ["flying", "plant", "undead"],
        "ineffective": ["stone", "water"]
    },
    "ground": {
        "effective": ["normal"],
        "ineffective": ["flying"]
    },
    "electro": {
        "effective": ["stone", "flying"],
        "ineffective": ["ground"]
    },
    "flying": {
        "effective": ["plant"],
        "ineffective": ["stone"]
    },
    "undead": {
        "effective": ["normal", "ground", "plant", "water"],
        "ineffective": ["fire"]
    },
}


if __name__ == "__main__":
    print("\033[31;1mDo not execute this!\033[0m")
