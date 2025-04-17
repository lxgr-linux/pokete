from pokete.classes.asset_service.resources import StationDict, DecorationDict

stations: dict[str, StationDict] = {
    "playmap_1": {
        "gen": {
            "additionals": ["intromap"],
            "desc": "A small town.",
            "d_next": "playmap_51",
            "text": """ *P#
├───
 # #""",
            "color": "brightgreen"
        },
        "add": {
            "x": 3,
            "y": 12
        }
    },
    "playmap_51": {
        "gen": {
            "additionals": [],
            "desc":
                "Some small patches of grass surrounded by forrest, near "
                "Nice Town.",
            "a_next": "playmap_1",
            "w_next": "cave_1",
            "text": r"""└─┐
──┘""",
            "color": "darkgreen"
        },
        "add": {
            "x": 7,
            "y": 12
        }
    },
    "cave_1": {
        "gen": {
            "additionals": [],
            "desc": "A dark cave full of batos.",
            "s_next": "playmap_51",
            "d_next": "playmap_2",
            "text": """█
█
█""",
            "color": "cavegrey"
        },
        "add": {
            "x": 7,
            "y": 9
        }
    },
    "playmap_2": {
        "gen": {
            "additionals": [],
            "desc": "Part of light areas near Sunny Dale.",
            "a_next": "cave_1",
            "d_next": "playmap_3",
            "text": """────""",
            "color": "darkgreen"
        },
        "add": {
            "x": 8,
            "y": 9
        }
    },
    "playmap_3": {
        "gen": {
            "additionals": ["playmap_49"],
            "desc": "A small sunny village.",
            "a_next": "playmap_2",
            "w_next": "playmap_4",
            "s_next": "playmap_6",
            "text": """P│$
─┤
#│#""",
            "color": "brightgreen"
        },
        "add": {
            "x": 12,
            "y": 8
        }
    },
    "playmap_4": {
        "gen": {
            "additionals": ["playmap_5"],
            "desc": "The shores of the great Sunnydale lake.",
            "s_next": "playmap_3",
            "d_next": "playmap_28",
            "text": """├
│
│""",
            "color": "darkgreen"
        },
        "add": {
            "x": 13,
            "y": 5
        }
    },
    "playmap_6": {
        "gen": {
            "additionals": [],
            "desc": "The woodland edge at the foot of a great mountain full of \
caves.",
            "w_next": "playmap_3",
            "a_next": "playmap_7",
            "d_next": "playmap_8",
            "text": """│
│
┴──""",
            "color": "deepgreen"
        },
        "add": {
            "x": 13,
            "y": 11
        }
    },
    "playmap_7": {
        "gen": {
            "additionals": [],
            "desc": "A dark and mysterious cave.",
            "d_next": "playmap_6",
            "text": """██""",
            "color": "cavegrey"
        },
        "add": {
            "x": 11,
            "y": 13
        }
    },
    "playmap_8": {
        "gen": {
            "additionals": ["playmap_10", "playmap_9"],
            "desc": "An abandoned fisher village.",
            "a_next": "playmap_6",
            "s_next": "playmap_11",
            "d_next": "playmap_12",
            "text": """#
─┬─""",
            "color": "brightyellow"
        },
        "add": {
            "x": 16,
            "y": 12
        }
    },
    "playmap_11": {
        "gen": {
            "additionals": [],
            "desc": "The shore of a lake near an olf fisher village.",
            "w_next": "playmap_8",
            "text": """│""",
            "color": "yellow"
        },
        "add": {
            "x": 17,
            "y": 14
        }
    },
    "playmap_12": {
        "gen": {
            "additionals": [],
            "desc": "A dense forest near Deepens forest.",
            "a_next": "playmap_8",
            "w_next": "playmap_13",
            "text": """ │
─┘""",
            "color": "brown"
        },
        "add": {
            "x": 19,
            "y": 12
        }
    },
    "playmap_13": {
        "gen": {
            "additionals": ["playmap_14", "playmap_20"],
            "desc": "Deepens forest, a big town in the middle of the deepest "
                    "forest, populated by thousands of people and cultural "
                    "center of the region.",
            "s_next": "playmap_12",
            "w_next": "playmap_15",
            "text": """#│A
 │
P│$""",
            "color": "gold"
        },
        "add": {
            "x": 19,
            "y": 9
        }
    },
    "playmap_15": {
        "gen": {
            "additionals": [],
            "desc": "A small clearing near Deepens forest.",
            "s_next": "playmap_13",
            "d_next": "playmap_16",
            "text": """┌──""",
            "color": "brown"
        },
        "add": {
            "x": 20,
            "y": 8
        }
    },
    "playmap_16": {
        "gen": {
            "additionals": ["playmap_17"],
            "desc": "A small 'village', that's not even worth talking about.",
            "a_next": "playmap_15",
            "d_next": "playmap_18",
            "text": """───""",
            "color": "brightyellow"
        },
        "add": {
            "x": 23,
            "y": 8
        }
    },
    "playmap_18": {
        "gen": {
            "additionals": [],
            "desc": "A small see at the foot of the Big mountain.",
            "a_next": "playmap_16",
            "w_next": "playmap_19",
            "text": """──┘""",
            "color": "darkgreen"
        },
        "add": {
            "x": 26,
            "y": 8
        }
    },
    "playmap_19": {
        "gen": {
            "additionals": [],
            "desc": "A dark and big cave in the Big mountain.",
            "s_next": "playmap_18",
            "w_next": "playmap_21",
            "text": """█
█""",
            "color": "cavegrey"
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
            "desc": "The great Rock-ville is the biggest city in the region "
                    "around the Big mountain. With the Rocky hotel it's "
                    "also a tourist hotspot.",
            "s_next": "playmap_19",
            "d_next": "playmap_33",
            "w_next": "playmap_40",
            "text": """P│ #
┌┴──
│#C """,
            "color": "lightgrey"
        },
        "add": {
            "x": 28,
            "y": 3
        }
    },
    "playmap_40": {
        "gen": {
            "additionals": [],
            "desc": "A Great beach, with great weather, always.",
            "s_next": "playmap_21",
            "text": """│""",
            "color": "yellow"
        },
        "add": {
            "x": 29,
            "y": 2
        }
    },
    "playmap_28": {
        "gen": {
            "additionals": [],
            "desc": "A foggy place full of ghosts and plants.",
            "a_next": "playmap_4",
            "d_next": "playmap_30",
            "text": """  ┌──
──┘""",
            "color": "brightgreen"
        },
        "add": {
            "x": 14,
            "y": 4
        }
    },
    "playmap_30": {
        "gen": {
            "additionals": ["playmap_31", "playmap_32"],
            "desc": "With its plant Poketes, Flowy Town may be the greenest "
                    "spot in the Pokete world and with the great git-tree it "
                    "may also be one of the most spectacular.",
            "a_next": "playmap_28",
            "text": """A$P
───┤
# # """,
            "color": "deepgreen"
        },
        "add": {
            "x": 19,
            "y": 3
        }
    },
    "playmap_33": {
        "gen": {
            "additionals": ["playmap_34"],
            "desc": "Part of the great agracultural landscape near Agrawos.",
            "a_next": "playmap_21",
            "d_next": "playmap_35",
            "text": """──""",
            "color": "yellow"
        },
        "add": {
            "x": 34,
            "y": 4
        }
    },
    "playmap_35": {
        "gen": {
            "additionals": ["playmap_36", "playmap_37", "playmap_38"],
            "desc": "Part of the great agracultural landscape near Agrawos.",
            "a_next": "playmap_33",
            "s_next": "playmap_39",
            "text": """──┐
┌─┘
└─┐""",
            "color": "brightyellow"
        },
        "add": {
            "x": 36,
            "y": 4
        }
    },
    "playmap_39": {
        "gen": {
            "additionals": ["playmap_41", "playmap_42", "playmap_43",
                            "playmap_44", "playmap_45", "playmap_46",
                            "playmap_47", "playmap_48"],
            "desc": "The great city of Agrawos, agricultural and cultural "
                    "center of the whole region. It's famous for its great "
                    "Pokete-Arena and its master trainer. Check out the "
                    "MowCow-Burger restaurant, which offers the best, "
                    "juiciest and most delicious Mowcow-burgers, cut from the "
                    "happiest and most delicious Mowcows anywhere to find!",
            "w_next": "playmap_35",
            "text": """ #│#
 P│A
├─┘#
 $ #""",
            "color": "yellow"
        },
        "add": {
            "x": 36,
            "y": 7
        }
    },

}

decorations: dict[str, DecorationDict] = {
    "cave3": {
        "gen": {
            "text": """██
████
  ███""",
            "color": "mediumgrey"
        },
        "add": {
            "x": 8,
            "y": 10
        }
    },

    "cave2": {
        "gen": {
            "text": """█
███
 ███""",
            "color": "mediumgrey"
        },
        "add": {
            "x": 10,
            "y": 13
        }
    },

    "cave1": {
        "gen": {
            "text": """
██████
██████
     █""",
            "color": "mediumgrey"
        },
        "add": {
            "x": 1,
            "y": 8
        }
    },

    "cave4-1": {
        "gen": {
            "text": """████
████""",
            "color": "mediumgrey"
        },
        "add": {
            "x": 23,
            "y": 1
        }
    },

    "cave4": {
        "gen": {
            "text": """ ███
 ███
  ███
  ███
   ██""",
            "color": "mediumgrey"
        },
        "add": {
            "x": 23,
            "y": 3
        }
    },

    "cave5": {
        "gen": {
            "text": """   ██
█████
████
 ██  """,
            "color": "mediumgrey"
        },
        "add": {
            "x": 29,
            "y": 5
        }
    },
    "mountainsee": {
        "gen": {
            "text": """█""",
            "color": "lakeblue"
        },
        "add": {
            "x": 29,
            "y": 8
        }
    },

    "cave7": {
        "gen": {
            "text": """  ████
  ████
 ███  """,
            "color": "mediumgrey"
        },
        "add": {
            "x": 31,
            "y": 1
        }
    },

    "rockybeach": {
        "gen": {
            "text": """█████""",
            "color": "lakeblue"
        },
        "add": {
            "x": 27,
            "y": 1
        }
    },

    "cave6": {
        "gen": {
            "text": """██""",
            "color": "cavegrey"
        },
        "add": {
            "x": 32,
            "y": 4
        }
    },
    "sunnylake": {
        "gen": {
            "text": """███""",
            "color": "lakeblue"
        },
        "add": {
            "x": 12,
            "y": 4
        }
    },
    "fisherlake": {
        "gen": {
            "text": """ ████ """,
            "color": "lakeblue"
        },
        "add": {
            "x": 14,
            "y": 15
        }
    },
}

if __name__ == "__main__":
    print("\033[31;1mDo not execute this!\033[0;1m")
