stations = {
    "playmap_1": {
        "gen": {
            "additionals": ["intromap"],
            "width": 2,
            "height": 1,
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
            "additionals": [],
            "width": 2,
            "height": 1,
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
            "additionals": ["playmap_22", "playmap_23", "playmap_24", "playmap_25", "playmap_26", "playmap_27"],
            "width": 3,
            "height": 1,
            "s_next": "playmap_19",
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
            "additionals": ["playmap_31"],
            "width": 1,
            "height": 1,
            "a_next": "playmap_28",
        },
        "add": {
            "x": 13,
            "y": 3
        }
    },
}

if __name__ == "__main__":
    print("\033[31;1mDo not execute this!\033[0m")
