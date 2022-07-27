npcs = {
    "test_npc": {
        "texts": ["npc.test_npc.hey"],
        "fn": None,
        "map": "playmap_3",
        "x": 49,
        "y": 14
    },
    "old_man": {
        "texts": ["npc.old_man.greet",
                  "npc.old_man.talk",
                  "npc.old_man.found_hyperball",
                  "npc.old_man.hyperball",
                  "npc.old_man.rarest",
                  "npc.old_man.keep"],
        "fn": "playmap_10_old_man",
        "map": "playmap_10",
        "x": 4,
        "y": 3
    },
    "healer": {
        "texts": ["Hello, fellow trainer.", "You and your Poketes look exhausted.", "I can heal them!"],
        "fn": "heal",
        "map": "playmap_8",
        "x": 52,
        "y": 1
    },
    "npc_1": {
        "texts": ["To get to the other side of this building, you have to win some epic fights against Deepest "
                  "Forests' best trainers!", "This won't be easy!"],
        "fn": None,
        "map": "playmap_13",
        "x": 33,
        "y": 6
    },
    "npc_2": {
        "texts": ["Welcome to Deepest Forest!",
                  "To get through this town you have to win against the best trainers of Deepest Forest!",
                  "I hope you have a great time!"],
        "fn": None,
        "map": "playmap_13",
        "x": 38,
        "y": 31
    },
    "npc_3": {
        "texts": ["In this cave your'll encounter the best Pokete trainers of this town.",
                  "But watch out, stone is their preference!"],
        "fn": None,
        "map": "playmap_21",
        "x": 136,
        "y": 15
    },
    "npc_4": {
        "texts": ["In this lake live...", "...Karpis."],
        "fn": None,
        "map": "playmap_21",
        "x": 64,
        "y": 12
    },
    "npc_5": {
        "texts": ["This is the town hall of Rock-ville.", "Here you can meet our mayor."],
        "fn": None,
        "map": "playmap_21",
        "x": 112,
        "y": 12
    },
    "npc_6": {
        "texts": ["Welcome to the Rocky Hotel!", "Here you can rent a room to sleep."],
        "fn": None,
        "map": "playmap_22",
        "x": 12,
        "y": 8
    },
    "npc_7": {
        "texts": ["How did you get into my room?"],
        "fn": None,
        "map": "playmap_23",
        "x": 14,
        "y": 8
    },
    "npc_8": {
        "texts": ["Isn't this a nice town?", "$100 would be very useful for a young trainer like you, wouldn't it?"],
        "fn": "playmap_23_npc_8",
        "map": "playmap_23",
        "x": 3,
        "y": 7
    },
    "npc_9": {
        "texts": ["British devs be like:", "It's a constructor, __init__?"],
        "fn": None,
        "map": "playmap_24",
        "x": 14,
        "y": 3
    },
    "major": {
        "texts": ["Hello trainer!", "I'm the mayor of Rock-ville.",
                  "Is it true that you are interested in fighting our best trainers!?", "I wish you luck!"],
        "fn": None,
        "map": "playmap_26",
        "x": 9,
        "y": 3
    },
    "boy_1": {
        "texts": [],
        "fn": "playmap_17_boy",
        "map": "playmap_17",
        "x": 4,
        "y": 3
    },
    "trader_2": {
        "texts": ["I've lived in this town for long time and therefore have \
found some cool Poketes.",
                  "Do you want to trade my cool Pokete?"],
        "fn": "playmap_20_trader",
        "map": "playmap_20",
        "x": 4,
        "y": 3
    },
    "ld_man": {
        "texts": ["Hello, fellow trainer!",
                  "You may have noticed that traveling between cities is not so comfortable nowadays.",
                  "But I can help you.", "I can give you this Learning Disc.",
                  "You can use it to teach the 'Flying' attack to one of your flying Poketes so you can ride it to "
                  "the next town.",
                  "Isn't that great?"],
        "fn": "playmap_29_ld_man",
        "map": "playmap_29",
        "x": 13,
        "y": 4
    },
    "lxgr": {
        "texts": ["Hello, fellow traveler. My name is lxgr and I created this game. ",
                  "You may be asking yourself: 'Lxgr, what are you doing in this game?', and the answer is: 'standing "
                  "around'.",
                  "I added this NPC because I'm stuck on a train somewere between Hamburg and Rostock, "
                  "and I'm bored.",
                  "You can contribute to this game at https://github.com/lxgr-linux/pokete .",
                  "If you want to hire me and stuff you can write me at lxgr@protonmail.com ."],
        "fn": None,
        "map": "playmap_30",
        "x": 4,
        "y": 2
    },
    "npc_10": {
        "texts": ["This is the great git tree of Flowy Town.", "It's our most holy monument!"],
        "fn": None,
        "map": "playmap_30",
        "x": 123,
        "y": 20
    },
    "npc_11": {
        "texts": ["This is the great Pokete arena of Flowy Town.",
                  "Here you'll have to fight our best trainers and rarest Poketes!"],
        "fn": None,
        "map": "playmap_30",
        "x": 60,
        "y": 18
    },
    "npc_12": {
        "texts": ["I think this will be helpful for you!"],
        "fn": "playmap_32_npc_12",
        "map": "playmap_32",
        "x": 8,
        "y": 4
    },
    "npc_13": {
        "texts": ["Muuuuuu!", "I'm a Mowcow!"],
        "fn": None,
        "map": "playmap_34",
        "x": 13,
        "y": 4
    },
    "npc_14": {
        "texts": ["I think this will be helpful for you!"],
        "fn": "playmap_36_npc_14",
        "map": "playmap_36",
        "x": 15,
        "y": 4
    },
    "npc_15": {
        "texts": ["Hello fellow trainer!",
                  "This is a very helpful potion that will save your Pokete in risky fights!"],
        "fn": "playmap_37_npc_15",
        "map": "playmap_37",
        "x": 4,
        "y": 3
    },
    "npc_16": {
        "texts": ["WTF r u doing here?", "Screw off!"],
        "fn": None,
        "map": "playmap_38",
        "x": 11,
        "y": 4
    },
    "chat_npc": {
        "texts": [],
        "fn": "chat",
        "chat": {
            "q": ["Hello there!"],
            "a": {
                "Hello": {
                    "q": ["Hi."],
                    "a": {}
                    },
                "How are you?": {
                    "q": ["I'm fine, thanks.", "Where are you from?"],
                    "a": {
                        "Home.": {
                            "q": ["Wow."],
                            "a": {}
                            }
                        }
                    }
                }
            },
        "map": "playmap_8",
        "x": 74,
        "y": 15
    },
    "beach_girl": {
        "texts": [],
        "fn": "chat",
        "chat": {
            "q": ["Hey there!", "What are you doing here at the beach?"],
            "a": {
                "Just chilling.": {
                    "q": ["Nice.", "This beach is the most beautiful in the region!", "Isn't the weather great today?"],
                    "a": {}
                    },
                "Searching for Poketes": {
                    "q": ["Oh cool, you're a Pokete trainer!", "Did you already find some?"],
                    "a": {
                        "Yes": {
                            "q": ["Cool!", "Have you caught a Crabbat yet?"],
                            "a": {
                                "Yes": {
                                    "q": ["That's pretty cool!", "But have you also seen a Saugh?"],
                                    "a": {
                                        "Yes": {
                                            "q": ["Those are fucking beasts!"],
                                            "a": {}
                                            },
                                        "Hell, what are those?": {
                                            "q": ["They're the dark and fiery souls of those who got burned to death by the hot sun!"],
                                            "a": {}
                                            }
                                        }
                                    },
                                "Yes, of course" : {
                                    "q": ["You're a good trainer, huh?", "I want to see you fight a Rustacean.", "They're very tough!"],
                                    "a": {}
                                    },
                                "No": {
                                    "q": ["That's too bad.", "But they're very tough!"],
                                    "a": {}
                                    }
                                }
                            },
                        "No": {
                            "q": ["That's too bad.", "You can find some in the sand fields."],
                            "a": {
                                "Thanks a lot!": {
                                    "q": ["No problem!"],
                                    "a": {}
                                    },
                                "Are you a trainer yourself?": {
                                    "q": ["No, but the guy over there is."],
                                    "a": {}
                                    }
                                }
                            }
                        }
                    }
                }
            },
        "map": "playmap_40",
        "x": 107,
        "y": 25
    },
    "npc_17": {
        "texts": ["Welcome to Agrawos!",
                  "Check out the MowCow-Burger restaurant, they have the best beef!",
                  "If you want a challenge, check out the Pokete-Arena; they have some quite heavy Poketes there!"],
        "fn": None,
        "map": "playmap_39",
        "x": 102,
        "y": 5
    },
    "npc_18": {
        "texts": ["This is the Pokete Arena of Agrawos; only go there if you're sure you can beat the challenge.",
                  "They got some very heavy Poketes in there!"],
        "fn": None,
        "map": "playmap_39",
        "x": 126,
        "y": 36
    },
    "npc_19": {
        "texts": ["This is the temple of the Wheeto, they have the goood stuff in there."],
        "fn": None,
        "map": "playmap_39",
        "x": 20,
        "y": 65
    },
    "npc_20": {
        "texts": ["Hey y'all, this town is soo famous for its' craaazy plants.",
                  "Especially Wheeto, from which healing potions can be made.",
                  "Want one?"],
        "fn": "playmap_39_npc_20",
        "map": "playmap_39",
        "x": 176,
        "y": 56
    },
    "npc_21": {
        "texts": [],
        "fn": "playmap_42_npc_21",
        "map": "playmap_42",
        "x": 7,
        "y": 3
    },
    "npc_22": {
        "texts": ["Oh man, if only I had a big and tasty MowCow-Burger...!"],
        "fn": None,
        "map": "playmap_42",
        "x": 22,
        "y": 4
    },
    "npc_23": {
        "texts": ["I'm priest of the Wheeto.",
                  "Those Poketes make you craaaaaazy!",
                  "They have some speeecial abilities!"],
        "fn": "playmap_43_npc_23",
        "map": "playmap_43",
        "x": 7,
        "y": 4
    },
    "npc_24": {
        "texts": ["I'm the mayor of Agrawos, the greatest city around.",
                  "Check out the MowCow-Burger restaurant; they have the best MowCow-Burgers! Also take a look at "
                  "the Pokete-Arena!",
                  "Here's a special tip: take a look at the temple of the Wheeto."],
        "fn": None,
        "map": "playmap_45",
        "x": 9,
        "y": 3
    },
    "npc_25": {
        "texts": [],
        "fn": "playmap_39_npc_25",
        "map": "playmap_39",
        "x": 4,
        "y": 33
    },
    "npc_26": {
        "texts": ["H-h-hello young trainer.",
                  "I've lived a looong life, b-but now it's time to go.",
                  "I'm trying to scatter all my belongings all over the world.",
                  "Since you're a Pokete trainer, you may have use for this healing potion!"],
        "fn": "playmap_47_npc_26",
        "map": "playmap_47",
        "x": 15,
        "y": 4
    },
    "npc_27": {
        "texts": ["Hello, young pal!",
                  "This city has been the home of plant Poketes for generations.",
                  "I posses one of the oldest and most powerful attacks aver known to Poketes.",
                  "'The Old Roots Hit', the most powerful of the powerful.",
                  "Sadly, all Poketes with this attack have been extinct for years.",
                  "The only thing that remained from them is this Learning Disc.",
                  "Do you want to have it?"],
        "fn": "playmap_48_npc_27",
        "map": "playmap_48",
        "x": 7,
        "y": 4
    },
    "npc_28": {
        "texts": ["Would you like a treat?", "With those treats you can level up one of your Poketes by a level!"],
        "fn": "playmap_49_npc_28",
        "map": "playmap_49",
        "x": 15,
        "y": 4
    },
    "npc_29": {
        "texts": ["Welcome to Pokete-Care!"],
        "fn": "playmap_50_npc_29",
        "map": "playmap_50",
        "x": 6,
        "y": 3
    },
}

if __name__ == "__main__":
    print("\033[31;1mDo not execute this!\033[0m")
