npcs = {
    "test_npc": {
        "texts": [" < Hey", " < I'm Josi"],
        "fn": None,
        "args": (),
        "map": "playmap_3",
        "x": 49,
        "y": 14
    },
    "old_man": {
        "texts": [" < Hello young trainer", " < When I've been at your age, I also was a trainer", " < And I found this very special Poketeball", " < A Hyperball", " < It's one of the oldest and rarerest of them all", " < You can keep it!"],
        "fn": "playmap_10_old_man",
        "args": (),
        "map": "playmap_10",
        "x": 4,
        "y": 3
    },
    "healer": {
        "texts": [" < Hello fellow trainer", " < You and your Poketes look exhausted", " < I will heal them!"],
        "fn": "heal",
        "args": (),
        "map": "playmap_8",
        "x": 52,
        "y": 1
    },
}


if __name__ == "__main__":
    print("\033[31;1mDo not execute this!\033[0m")
