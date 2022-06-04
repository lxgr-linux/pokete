stations = {
    "playmap_1": {
        "gen": {
            "additionals": ["intromap"],
            "width": 2,
            "height": 1,
            "desc": "A small town.",
            "w_next": "cave_1"
        },
        "add": {
            "x": 5,
            "y": 7
        }
    },
    "cave_1": {
        "gen": {
            "additionals": [],
            "width": 1,
            "height": 2,
            "desc": "A dark cave full of batos.",
            "s_next": "playmap_1",
            "d_next": "playmap_2",
        },
        "add": {
            "x": 6,
            "y": 5
        }
    },
    "playmap_2": {
        "gen": {
            "additionals": [],
            "width": 2,
            "height": 1,
            "desc": "Part of light areas near Josi Town.",
            "a_next": "cave_1",
            "d_next": "playmap_3",
        },
        "add": {
            "x": 7,
            "y": 5
        }
    },
    "playmap_3": {
        "gen": {
            "additionals": ["playmap_49"],
            "width": 2,
            "height": 1,
            "desc": "A small sunny village.",
            "a_next": "playmap_2",
            "w_next": "playmap_4",
            "s_next": "playmap_6",
        },
        "add": {
            "x": 9,
            "y": 5
        }
    },
    "playmap_4": {
        "gen": {
            "additionals": ["playmap_5"],
            "width": 1,
            "height": 3,
            "desc": "The shores of the great Sunnydale lake.",
            "s_next": "playmap_3",
            "d_next": "playmap_28"
        },
        "add": {
            "x": 10,
            "y": 2
        }
    },
    "playmap_6": {
        "gen": {
            "additionals": [],
            "width": 1,
            "height": 2,
            "desc": "The woodland edge at the foot of a great mountain full of \
caves.",
            "w_next": "playmap_3",
            "a_next": "playmap_7",
            "d_next": "playmap_8",
        },
        "add": {
            "x": 10,
            "y": 6
        }
    },
    "playmap_7": {
        "gen": {
            "additionals": [],
            "width": 1,
            "height": 1,
            "desc": "A dark and mysterious cave.",
            "d_next": "playmap_6",
        },
        "add": {
            "x": 9,
            "y": 7
        }
    },
    "playmap_8": {
        "gen": {
            "additionals": ["playmap_10", "playmap_9"],
            "width": 2,
            "height": 1,
            "desc": "An abandoned fisher village.",
            "a_next": "playmap_6",
            "s_next": "playmap_11",
            "d_next": "playmap_12",
        },
        "add": {
            "x": 11,
            "y": 7
        }
    },
    "playmap_11": {
        "gen": {
            "additionals": [],
            "width": 1,
            "height": 1,
            "desc": "The shore of a lake near an olf fisher village.",
            "w_next": "playmap_8",
        },
        "add": {
            "x": 11,
            "y": 8
        }
    },
    "playmap_12": {
        "gen": {
            "width": 2,
            "additionals": [],
            "height": 1,
            "desc": "A dense forest near Deepens forest.",
            "a_next": "playmap_8",
            "w_next": "playmap_13",
        },
        "add": {
            "x": 13,
            "y": 7
        }
    },
    "playmap_13": {
        "gen": {
            "additionals": ["playmap_14", "playmap_20"],
            "width": 1,
            "height": 2,
            "desc": "Deepens forest, a big town in the middle of the deepest \
forest, populated by thousands of people and cultural center of the region.",
            "s_next": "playmap_12",
            "w_next": "playmap_15",
        },
        "add": {
            "x": 14,
            "y": 5
        }
    },
    "playmap_15": {
        "gen": {
            "additionals": [],
            "width": 2,
            "height": 1,
            "desc": "A small clearing near Deepens forest.",
            "s_next": "playmap_13",
            "d_next": "playmap_16",
        },
        "add": {
            "x": 14,
            "y": 4
        }
    },
    "playmap_16": {
        "gen": {
            "additionals": ["playmap_17"],
            "width": 1,
            "height": 1,
            "desc": "A small 'village', that's not even worth talking about.",
            "a_next": "playmap_15",
            "d_next": "playmap_18",
        },
        "add": {
            "x": 16,
            "y": 4
        }
    },
    "playmap_18": {
        "gen": {
            "additionals": [],
            "width": 2,
            "height": 1,
            "desc": "A small see at the foot of the Big mountain.",
            "a_next": "playmap_16",
            "w_next": "playmap_19",
        },
        "add": {
            "x": 17,
            "y": 4
        }
    },
    "playmap_19": {
        "gen": {
            "additionals": [],
            "width": 1,
            "height": 1,
            "desc": "A dark and big cave in the Big mountain.",
            "s_next": "playmap_18",
            "w_next": "playmap_21",
        },
        "add": {
            "x": 18,
            "y": 3
        }
    },
    "playmap_21": {
        "gen": {
            "additionals": ["playmap_22", "playmap_23", "playmap_24",
                            "playmap_25", "playmap_26", "playmap_27",
                            "playmap_29", "playmap_50"],
            "width": 3,
            "height": 1,
            "desc": "The great Rock-ville is the biggest city in the region \
around the Big mountain. With the Rocky hotel it's also a tourist \
hotspot.",
            "s_next": "playmap_19",
            "d_next": "playmap_33",
            "w_next": "playmap_40"
        },
        "add": {
            "x": 18,
            "y": 2
        }
    },
    "playmap_28": {
        "gen": {
            "additionals": [],
            "width": 2,
            "height": 1,
            "desc": "A foggy place full of ghosts and plants.",
            "a_next": "playmap_4",
            "d_next": "playmap_30",
        },
        "add": {
            "x": 11,
            "y": 3
        }
    },
    "playmap_30": {
        "gen": {
            "additionals": ["playmap_31", "playmap_32"],
            "width": 1,
            "height": 1,
            "desc": "With its plant Poketes, Flowy Town may be the greenest \
spot in the Pokete world and with the great git-tree it may also be one \
of the most spectacular.",
            "a_next": "playmap_28",
        },
        "add": {
            "x": 13,
            "y": 3
        }
    },
    "playmap_33": {
        "gen": {
            "additionals": ["playmap_34"],
            "width": 1,
            "height": 1,
            "desc": "Part of the great agracultural landscape near Agrawos.",
            "a_next": "playmap_21",
            "d_next": "playmap_35",
        },
        "add": {
            "x": 21,
            "y": 2
        }
    },
    "playmap_35": {
        "gen": {
            "additionals": ["playmap_36", "playmap_37", "playmap_38"],
            "width": 1,
            "height": 2,
            "desc": "Part of the great agracultural landscape near Agrawos.",
            "a_next": "playmap_33",
            "s_next": "playmap_39",
        },
        "add": {
            "x": 22,
            "y": 2
        }
    },
    "playmap_40": {
        "gen": {
            "additionals": [],
            "width": 2,
            "height": 1,
            "desc": "A Great beach, with great weather, always.",
            "s_next": "playmap_21",
        },
        "add": {
            "x": 18,
            "y": 1
        }
    },
    "playmap_39": {
        "gen": {
            "additionals": ["playmap_41", "playmap_42", "playmap_43",
                            "playmap_44", "playmap_45", "playmap_46",
                            "playmap_47", "playmap_48"],
            "width": 2,
            "height": 2,
            "desc": "The great city of Agrawos, agricultural and cultural "
                    "center of the whole region. It's famous for its great "
                    "Pokete-Arena and its master trainer. Check out the "
                    "MowCow-Burger restaurant, which offers the best, "
                    "juiciest and most delicious Mowcow-burgers, cut from the "
                    "happiest and most delicious Mowcows anywhere to find!", 
            "w_next": "playmap_35",
        },
        "add": {
            "x": 21,
            "y": 4
        }
    },
}

if __name__ == "__main__":
    print("\033[31;1mDo not execute this!\033[0m")
