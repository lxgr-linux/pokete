stations = {
    "playmap_1": {
        "gen": {
            "additionals": ["intromap"],
            "width": 4,
            "height": 3,
            "desc": "A small town.",
            "d_next": "playmap_51",
            "text": """*P⌂ ┣━━━ ⌂⌂ """,
            "color": "\033[38;5;28m"
        },
        "add": {
            "x": 3,
            "y": 12
        }
    },
    "playmap_51": {
        "gen": {
            "additionals": [],
            "width": 3,
            "height": 2,
            "desc":
                "Some small patches of grass surrounded by forrest, near "
                "Nice Town.",
            "a_next": "playmap_1",
            "w_next": "cave_1",
            "text": r"""┗━┓━━┛""",
            "color": "\033[38;5;22m"
        },
        "add": {
            "x": 7,
            "y": 12
        }
    },
    "cave_1": {
        "gen": {
            "additionals": [],
            "width": 1,
            "height": 3,
            "desc": "A dark cave full of batos.",
            "s_next": "playmap_51",
            "d_next": "playmap_2",
            "text": """▅██""",
            "color": "\033[38;5;236m"
        },
        "add": {
            "x": 7,
            "y": 9
        }
    },
    "playmap_2": {
        "gen": {
            "additionals": [],
            "width": 4,
            "height": 1,
            "desc": "Part of light areas near Sunny Dale.",
            "a_next": "cave_1",
            "d_next": "playmap_3",
            "text": """━━━━""",
            "color": "\033[38;5;28m"
        },
        "add": {
            "x": 8,
            "y": 9
        }
    },
    "playmap_3": {
        "gen": {
            "additionals": ["playmap_49"],
            "width": 3,
            "height": 3,
            "desc": "A small sunny village.",
            "a_next": "playmap_2",
            "w_next": "playmap_4",
            "s_next": "playmap_6",
            "text": """P┃$━┫⌂⌂┃⌂""",
            "color": "\033[38;5;76m"
        },
        "add": {
            "x": 12,
            "y": 8
        }
    },
    "playmap_4": {
        "gen": {
            "additionals": ["playmap_5"],
            "width": 1,
            "height": 3,
            "desc": "The shores of the great Sunnydale lake.",
            "s_next": "playmap_3",
            "d_next": "playmap_28",
            "text": """┣┃┃""",
            "color": "\033[38;5;29m"
        },
        "add": {
            "x": 13,
            "y": 5
        }
    },
    "playmap_6": {
        "gen": {
            "additionals": [],
            "width": 3,
            "height": 3,
            "desc": "The woodland edge at the foot of a great mountain full of \
caves.",
            "w_next": "playmap_3",
            "a_next": "playmap_7",
            "d_next": "playmap_8",
            "text": """┃  ┃  ┻━━""",
            "color": "\033[38;5;28m"
        },
        "add": {
            "x": 13,
            "y": 11
        }
    },
    "playmap_7": {
        "gen": {
            "additionals": [],
            "width": 2,
            "height": 1,
            "desc": "A dark and mysterious cave.",
            "d_next": "playmap_6",
            "text": """██""",
            "color": "\033[38;5;236m"
        },
        "add": {
            "x": 11,
            "y": 13
        }
    },
    "playmap_8": {
        "gen": {
            "additionals": ["playmap_10", "playmap_9"],
            "width": 3,
            "height": 2,
            "desc": "An abandoned fisher village.",
            "a_next": "playmap_6",
            "s_next": "playmap_11",
            "d_next": "playmap_12",
            "text": """ ⌂ ━┳━""",
            "color": "\033[38;5;136m"
        },
        "add": {
            "x": 16,
            "y": 12
        }
    },
    "playmap_11": {
        "gen": {
            "additionals": [],
            "width": 1,
            "height": 1,
            "desc": "The shore of a lake near an olf fisher village.",
            "w_next": "playmap_8",
            "text": """┃""",
            "color": "\033[38;5;178m"
        },
        "add": {
            "x": 17,
            "y": 14
        }
    },
    "playmap_12": {
        "gen": {
            "width": 3,
            "additionals": [],
            "height": 2,
            "desc": "A dense forest near Deepens forest.",
            "a_next": "playmap_8",
            "w_next": "playmap_13",
            "text": """  ┃━━┛""",
            "color": "\033[38;5;88m\033[1m"
        },
        "add": {
            "x": 19,
            "y": 12
        }
    },
    "playmap_13": {
        "gen": {
            "additionals": ["playmap_14", "playmap_20"],
            "width": 3,
            "height": 3,
            "desc": "Deepens forest, a big town in the middle of the deepest \
forest, populated by thousands of people and cultural center of the region.",
            "s_next": "playmap_12",
            "w_next": "playmap_15",
            "text": """⌂┃A⌂┃⌂P┃$""",
            "color": "\033[38;5;94m\033[1m"
        },
        "add": {
            "x": 20,
            "y": 9
        }
    },
    "playmap_15": {
        "gen": {
            "additionals": [],
            "width": 3,
            "height": 1,
            "desc": "A small clearing near Deepens forest.",
            "s_next": "playmap_13",
            "d_next": "playmap_16",
            "text": """┏━━""",
            "color": "\033[38;5;88m\033[1m"
        },
        "add": {
            "x": 21,
            "y": 8
        }
    },
    "playmap_16": {
        "gen": {
            "additionals": ["playmap_17"],
            "width": 2,
            "height": 1,
            "desc": "A small 'village', that's not even worth talking about.",
            "a_next": "playmap_15",
            "d_next": "playmap_18",
            "text": """━━""",
            "color": "\033[38;5;154m\033[1m"
        },
        "add": {
            "x": 24,
            "y": 8
        }
    },
    "playmap_18": {
        "gen": {
            "additionals": [],
            "width": 3,
            "height": 1,
            "desc": "A small see at the foot of the Big mountain.",
            "a_next": "playmap_16",
            "w_next": "playmap_19",
            "text": """━━┛""",
            "color": "\033[38;5;28m\033[1m"
        },
        "add": {
            "x": 26,
            "y": 8
        }
    },
    "playmap_19": {
        "gen": {
            "additionals": [],
            "width": 1,
            "height": 2,
            "desc": "A dark and big cave in the Big mountain.",
            "s_next": "playmap_18",
            "w_next": "playmap_21",
            "text": """██""",
            "color": "\033[38;5;236m"
        },
        "add": {
            "x": 28,
            "y": 6
        }
    },
    "playmap_21": {
        "gen": {
            "additionals": ["playmap_22", "playmap_23", "playmap_24",
                            "playmap_25", "playmap_26", "playmap_27",
                            "playmap_29", "playmap_50"],
            "width": 4,
            "height": 3,
            "desc": "The great Rock-ville is the biggest city in the region \
around the Big mountain. With the Rocky hotel it's also a tourist \
hotspot.",
            "s_next": "playmap_19",
            "d_next": "playmap_33",
            "w_next": "playmap_40",
            "text": """P┃⌂⌂┏┻━━┃⌂C """,
            "color": "\033[38;5;246m"
        },
        "add": {
            "x": 28,
            "y": 3
        }
    },
    "playmap_28": {
        "gen": {
            "additionals": [],
            "width": 5,
            "height": 2,
            "desc": "A foggy place full of ghosts and plants.",
            "a_next": "playmap_4",
            "d_next": "playmap_30",
            "text": """  ┏━━━━┛  """,
            "color": "\033[38;5;22m"
        },
        "add": {
            "x": 14,
            "y": 4
        }
    },
    "playmap_30": {
        "gen": {
            "additionals": ["playmap_31", "playmap_32"],
            "width": 4,
            "height": 3,
            "desc": "With its plant Poketes, Flowy Town may be the greenest \
spot in the Pokete world and with the great git-tree it may also be one \
of the most spectacular.",
            "a_next": "playmap_28",
            "text": """ $P ━━━┫⌂A⌂⌂""",
            "color": "\033[38;5;34m"
        },
        "add": {
            "x": 19,
            "y": 3
        }
    },
    "playmap_33": {
        "gen": {
            "additionals": ["playmap_34"],
            "width": 2,
            "height": 1,
            "desc": "Part of the great agracultural landscape near Agrawos.",
            "a_next": "playmap_21",
            "d_next": "playmap_35",
            "text": """━━""",
            "color": "\033[38;5;178m"
        },
        "add": {
            "x": 34,
            "y": 4
        }
    },
    "playmap_35": {
        "gen": {
            "additionals": ["playmap_36", "playmap_37", "playmap_38"],
            "width": 3,
            "height": 3,
            "desc": "Part of the great agracultural landscape near Agrawos.",
            "a_next": "playmap_33",
            "s_next": "playmap_39",
            "text": """━━┓┏━┛┗━┓""",
            "color": "\033[38;5;154m"
        },
        "add": {
            "x": 36,
            "y": 4
        }
    },
    "playmap_40": {
        "gen": {
            "additionals": [],
            "width": 1,
            "height": 1,
            "desc": "A Great beach, with great weather, always.",
            "s_next": "playmap_21",
            "text": """┃""",
            "color": "\033[38;5;178m"
        },
        "add": {
            "x": 29,
            "y": 2
        }
    },
    "playmap_39": {
        "gen": {
            "additionals": ["playmap_41", "playmap_42", "playmap_43",
                            "playmap_44", "playmap_45", "playmap_46",
                            "playmap_47", "playmap_48"],
            "width": 4,
            "height": 4,
            "desc": "The great city of Agrawos, agricultural and cultural "
                    "center of the whole region. It's famous for its great "
                    "Pokete-Arena and its master trainer. Check out the "
                    "MowCow-Burger restaurant, which offers the best, "
                    "juiciest and most delicious Mowcow-burgers, cut from the "
                    "happiest and most delicious Mowcows anywhere to find!",
            "w_next": "playmap_35",
            "text": """  ┃⌂ P┃A┣━┛⌂⌂$⌂⌂""",
            "color": "\033[38;5;227m\033[1m"
        },
        "add": {
            "x": 36,
            "y": 7
        }
    },
    
    
    
}

decorations={
    "wheeto": {
        "gen": {
            "additionals": [],
            "width": 3,
            "height": 4,
            "desc": "",
            "text": """\ /\|/\|/ | """,
            "color": "\033[38;5;64m\033[1m"
        },
        "add": {
            "x": 41,
            "y": 6
        }
    },
    
    "cave3": {
        "gen": {
            "additionals": [],
            "width": 5,
            "height": 3,
            "desc": "",
            "text": """█▄   ███▄   ▜█▙""",
            "color": "\033[38;5;238m"
        },
        "add": {
            "x": 8,
            "y": 10
        }
    },
    
    "cave2": {
        "gen": {
            "additionals": [],
            "width": 4,
            "height": 3,
            "desc": "",
            "text": """▐   ▐██  ▜█▆""",
            "color": "\033[38;5;238m"
        },
        "add": {
            "x": 10,
            "y": 13
        }
    },
    
    "cave1": {
        "gen": {
            "additionals": [],
            "width": 6,
            "height": 4,
            "desc": "",
            "text": """▄▄▂   ████▇▅██████    ▀▜""",
            "color": "\033[38;5;238m"
        },
        "add": {
            "x": 1,
            "y": 8
        }
    },
    
    "cave4-1": {
        "gen": {
            "additionals": [],
            "width": 4,
            "height": 2,
            "desc": "",
            "text": """████████""",
            "color": "\033[38;5;238m"
        },
        "add": {
            "x": 23,
            "y": 1
        }
    },
    
    "cave4": {
        "gen": {
            "additionals": [],
            "width": 5,
            "height": 5,
            "desc": "",
            "text": """▐███ ▕███▎ ▜██▊  ▜██  ▝██""",
            "color": "\033[38;5;238m"
        },
        "add": {
            "x": 23,
            "y": 3
        }
    },
    
    
    "water_mountainsee": {
        "gen": {
            "additionals": [],
            "width": 1,
            "height": 1,
            "desc": "",
            "text": """█""",
            "color": "\033[38;5;27m\033[1m"
        },
        "add": {
            "x": 29,
            "y": 8
        }
    },
    "cave5": {
        "gen": {
            "additionals": [],
            "width": 5,
            "height": 4,
            "desc": "",
            "text": """   ██▙▄▟█▛███▌  █▀  """,
            "color": "\033[38;5;238m"
        },
        "add": {
            "x": 29,
            "y": 5
        }
    },
    
    "water_rockybeach": {
        "gen": {
            "additionals": [],
            "width": 6,
            "height": 2,
            "desc": "",
            "text": """████▀▀▀▀ ▔  """,
            "color": "\033[38;5;27m\033[1m"
        },
        "add": {
            "x": 27,
            "y": 1
        }
    },
    
    "cave7": {
        "gen": {
            "additionals": [],
            "width": 6,
            "height": 3,
            "desc": "",
            "text": """   ██▀  ▗█▛  ▐█▀  """,
            "color": "\033[38;5;238m"
        },
        "add": {
            "x": 31,
            "y": 1
        }
    },
    
    "cave6": {
        "gen": {
            "additionals": [],
            "width": 2,
            "height": 1,
            "desc": "",
            "text": """██""",
            "color": "\033[38;5;236m"
        },
        "add": {
            "x": 32,
            "y": 4
        }
    },
     
    "rose": {
        "gen": {
            "additionals": [],
            "width": 7,
            "height": 5,
            "desc": "",
            "text": """   N      ▲   W ◀ ▶ E   ▼      S   """
        },
        "add": {
            "x": 53,
            "y": 11
        }
    },
    "water_sunnylake": {
        "gen": {
            "additionals": [],
            "width": 2,
            "height": 2,
            "desc": "",
            "text": """▄▄██""",
            "color": "\033[38;5;27m\033[1m"
        },
        "add": {
            "x": 12,
            "y": 3
        }
    },
    
    "water_fisherlake": {
        "gen": {
            "additionals": [],
            "width": 6,
            "height": 1,
            "desc": "",
            "text": """▆▆██▆▃""",
            "color": "\033[38;5;27m\033[1m"
        },
        "add": {
            "x": 14,
            "y": 15
        }
    },
    
    "Legend": {
        "gen": {
            "additionals": [],
            "width": 15,
            "height": 6,
            "desc": "",
            "text": """│ Legend:      │ P-Pokecenter │ $-Shop       │ C-PoketeCare │ A-Arena      └──────────────"""
            #! - avaiable quests
        },
        "add": {
            "x": 45,
            "y": 1
        }
    },
    
    "karpi": {
        "gen": {
            "additionals": [],
            "width": 8,
            "height": 1,
            "desc": "",
            "text": """<°))))><""",
            "color": "\033[1m\033[34m"
        },
        "add": {
            "x": 21,
            "y": 15
        }
    },
       
    "owl": {
        "gen": {
            "additionals": [],
            "width": 5,
            "height": 4,
            "desc": "",
            "text": """,___,{o,o}/)_)  ""  """,
            "color": "\033[1m\033[38;5;22m"
        },
        "add": {
            "x": 24,
            "y": 9
        }
    },
    
    "rosi_flower": {
        "gen": {
            "additionals": [],
            "width": 3,
            "height": 1,
            "desc": "",
            "text": """(@)""",
            "color": "\033[1m\033[38;5;196m"
        },
        "add": {
            "x": 16,
            "y": 1
        }
    },
    
    "rosi_trunk": {
        "gen": {
            "additionals": [],
            "width": 3,
            "height": 2,
            "desc": "",
            "text": """ | \|/""",
            "color": "\033[1m\033[38;5;29m"
        },
        "add": {
            "x": 16,
            "y": 2
        }
    },
}

if __name__ == "__main__":
    print("\033[31;1mDo not execute this!\033[0m")
