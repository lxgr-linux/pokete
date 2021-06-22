stations = {
    "playmap_1": {
        "gen": {
            "width": 2,
            "height": 1,
            "w_next": "cave_1"
        },
        "add": {
            "rx": 5,
            "ry": 7
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
            "rx": 6,
            "ry": 5
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
            "rx": 7,
            "ry": 5
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
            "rx": 9,
            "ry": 5
        }
    },
    "playmap_4": {
        "gen": {
            "width": 1,
            "height": 3,
            "s_next": "playmap_3",
        },
        "add": {
            "rx": 10,
            "ry": 2
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
            "rx": 10,
            "ry": 6
        }
    },
    "playmap_7": {
        "gen": {
            "width": 1,
            "height": 1,
            "d_next": "playmap_6",
        },
        "add": {
            "rx": 9,
            "ry": 7
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
            "rx": 11,
            "ry": 7
        }
    },
    "playmap_11": {
        "gen": {
            "width": 1,
            "height": 1,
            "w_next": "playmap_8",
        },
        "add": {
            "rx": 11,
            "ry": 8
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
            "rx": 13,
            "ry": 7
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
            "rx": 14,
            "ry": 5
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
            "rx": 14,
            "ry": 4
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
            "rx": 16,
            "ry": 4
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
            "rx": 17,
            "ry": 4
        }
    },
    "playmap_19": {
        "gen": {
            "width": 1,
            "height": 1,
            "s_next": "playmap_18",
        },
        "add": {
            "rx": 18,
            "ry": 3
        }
    },
}

if __name__ == "__main__":
    print("\033[31;1mDo not execute this!\033[0m")
