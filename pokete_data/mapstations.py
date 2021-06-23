stations = {
    "playmap_1": {
        "gen": {
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
            "width": 1,
            "height": 3,
            "s_next": "playmap_3",
        },
        "add": {
            "x": 10,
            "y": 2
        }
    },
    "playmap_6": {
        "gen": {
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
            "width": 2,
            "height": 1,
            "s_next": "playmap_13",
            "w_next": "playmap_16",
        },
        "add": {
            "x": 14,
            "y": 4
        }
    },
    "playmap_16": {
        "gen": {
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
            "width": 1,
            "height": 1,
            "s_next": "playmap_18",
        },
        "add": {
            "x": 18,
            "y": 3
        }
    },
}

if __name__ == "__main__":
    print("\033[31;1mDo not execute this!\033[0m")
