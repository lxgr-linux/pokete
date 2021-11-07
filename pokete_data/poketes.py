# Here starts to definition of all the Poketes
# If you want to contribute Poketes, you have to keep in mind, that "ico" can be max 11x4 chars big
# and that the max for attacks is (until now) 4
# All attributes have to be present make a Pokete work
# A type has to be present
# Hornita was inspired and partly designed by Pia <pialandrath@gmail.com>

pokes = {
    "__fallback__": {
        "name": "",
        "hp": 20,
        "atc": 0,
        "defense": 0,
        "attacks": [],
        "pool": [],
        "miss_chance": 0,
        "desc": "",
        "lose_xp": 0,
        "rarity": 0,
        "types": ["normal"],
        "evolve_poke": "",
        "evolve_lvl": 0,
        "initiative": 0,
        "ico": [{
            "txt": """ """,
            "esc": None}],
    },
    "steini": {
        "name": "Steini",
        "hp": 25,
        "atc": 2,
        "defense": 4,
        "attacks": ["tackle", "politure", "brick_throw"],
        "pool": [],
        "miss_chance": 0,
        "desc": "A squared stone that can casually be found on the ground.",
        "lose_xp": 3,
        "rarity": 1,
        "types": ["stone", "normal"],
        "evolve_poke": "",
        "evolve_lvl": 0,
        "initiative": 5,
        "ico": [{
            "txt": """ +-------+
 | o   o |
 |  www  |
 +-------+ """,
            "esc": None}],
    },
    "mowcow": {
        "name": "Mowcow",
        "hp": 20,
        "atc": 2,
        "defense": 3,
        "attacks": ["tackle"],
        "pool": ["supercow_power", "meat_skewer"],
        "miss_chance": 0,
        "desc": "A cow-like creature found on meadows.",
        "lose_xp": 2,
        "rarity": 1,
        "types": ["normal"],
        "evolve_poke": "",
        "evolve_lvl": 0,
        "initiative": 2,
        "ico": [{
            "txt": """    ^__^
    (oo)
    (__)""",
            "esc": None}],
    },
    "bigstone": {
        "name": "Bigstone",
        "hp": 30,
        "atc": 2,
        "defense": 13,
        "attacks": ["snooze", "politure", "brick_throw"],
        "pool": [],
        "miss_chance": 0,
        "desc": "A big and heavy stone made from one of the hardest stones.",
        "lose_xp": 5,
        "rarity": 0.3,
        "types": ["stone", "normal"],
        "evolve_poke": "",
        "evolve_lvl": 0,
        "initiative": 5,
        "ico": [{
            "txt": """+---------+
|  o   o  |
|   ---   |
+---------+""",
            "esc": None}],
    },
    "poundi": {
        "name": "Poundi",
        "hp": 25,
        "atc": 2,
        "defense": 3,
        "attacks": ["tackle", "politure", "earch_quake"],
        "pool": [],
        "miss_chance": 0,
        "desc": "A powerful and heavy stone Pokete that lives in mountain caves.",
        "lose_xp": 4,
        "rarity": 0.7,
        "types": ["stone", "normal"],
        "evolve_poke": "",
        "evolve_lvl": 0,
        "initiative": 4,
        "ico": [{
            "txt": """   A-A-A
  < o o >
  < --- >
   VvVvV""",
            "esc": None}],
    },
    "lilstone": {
        "name": "Lilstone",
        "hp": 20,
        "atc": 1,
        "defense": 2,
        "attacks": ["tackle", "politure", "pepple_fire"],
        "pool": [],
        "miss_chance": 0,
        "desc": "A small but powerful stone Pokete that lives in the mountains.",
        "lose_xp": 2,
        "rarity": 1,
        "types": ["stone", "normal"],
        "evolve_poke": "bigstone",
        "evolve_lvl": 25,
        "initiative": 3,
        "ico": [{
            "txt": """
   _____
   |'ᵕ'|
   ‾‾‾‾‾""",
            "esc": None}],
    },
    "rosi": {
        "name": "Rosi",
        "hp": 20,
        "atc": 0,
        "defense": 1,
        "attacks": ["sucker", "super_sucker"],
        "pool": [],
        "miss_chance": 0,
        "desc": "A plant Pokete, that's often mistaken for a normal flower.",
        "lose_xp": 2,
        "rarity": 0.8,
        "types": ["plant"],
        "evolve_poke": "",
        "evolve_lvl": 0,
        "initiative": 3,
        "ico": [{
            "txt": """
    (@)
     |
    \|/""",
            "esc": None}],
    },
    "wheeto": {
        "name": "Wheeto",
        "hp": 20,
        "atc": 3,
        "defense": 2,
        "attacks": ["root_slap", "special_smell"],
        "pool": [],
        "miss_chance": 0.1,
        "desc": "A plant Pokete found in Agrawos, with special 'Powers'.",
        "lose_xp": 2,
        "rarity": 1,
        "types": ["plant"],
        "evolve_poke": "",
        "evolve_lvl": 0,
        "initiative": 2,
        "ico": [{
            "txt": """    \ /
    \|/
    \|/
     |""",
            "esc": None}],
    },
    "gobost": {
        "name": "Gobost",
        "hp": 20,
        "atc": 2,
        "defense": 1,
        "attacks": ["tackle", "mind_blow", "heart_touch"],
        "pool": ["cry"],
        "miss_chance": 0,
        "desc": "A scary ghost Pokete that lives in caves and old houses.",
        "lose_xp": 3,
        "rarity": 1,
        "types": ["undead", "normal"],
        "evolve_poke": "angrilo",
        "evolve_lvl": 25,
        "initiative": 6,
        "ico": [{
            "txt": """ .░░░░░░░.
 ░░o░░░o░░
 ░░░░░░░░░
 ░ ░ ░ ░ ░""",
            "esc": None}],
    },
    "angrilo": {
        "name": "Angrilo",
        "hp": 25,
        "atc": 3,
        "defense": 2,
        "attacks": ["tackle", "mind_blow", "wet_slap", "heart_touch"],
        "pool": ["cry"],
        "miss_chance": 0,
        "desc": "A ghost Pokete that will scare your pants off.",
        "lose_xp": 4,
        "rarity": 0.6,
        "types": ["undead", "normal", "water"],
        "evolve_poke": "",
        "evolve_lvl": 0,
        "initiative": 7,
        "ico": [{
            "txt": """ .░░░░░░░.
 ░░\░░░/░░
 .░░( )░░.
.         .""",
            "esc": None}],
    },
    "vogli": {
        "name": "Vogli",
        "hp": 20,
        "atc": 6,
        "defense": 1,
        "attacks": ["tackle", "power_pick"],
        "pool": ["cry"],
        "miss_chance": 0,
        "desc": "A very common bird Pokete that lives everywhere.",
        "lose_xp": 2,
        "rarity": 1,
        "types": ["flying", "normal", "bird"],
        "evolve_poke": "voglo",
        "initiative": 6,
        "evolve_lvl": 20,
        "ico": [{
            "txt": """    A
   <')
    www*
    ||     """,
            "esc": None}]
    },
    "voglo": {
        "name": "Voglo",
        "hp": 20,
        "atc": 7,
        "defense": 1,
        "attacks": ["tackle", "power_pick", "wing_hit", "brooding"],
        "pool": ["cry"],
        "miss_chance": 0,
        "desc": "A very aggressive bird Pokete that can only be found in the woods.",
        "lose_xp": 3,
        "rarity": 0.8,
        "types": ["flying", "normal", "bird"],
        "evolve_poke": "",
        "evolve_lvl": 0,
        "initiative": 7,
        "ico": [{
            "txt": """    ?
   >´)
    www*
    ||     """,
            "esc": None}]
    },
    "ostri": {
        "name": "Ostri",
        "hp": 20,
        "atc": 8,
        "defense": 0,
        "attacks": ["tackle", "eye_pick", "brooding"],
        "pool": ["cry"],
        "miss_chance": 0,
        "desc": "A very aggressive bird Pokete that lives near deserts and will try to pick out your eyes.",
        "rarity": 0.6,
        "lose_xp": 4,
        "types": ["flying", "normal", "bird"],
        "evolve_poke": "",
        "evolve_lvl": 0,
        "initiative": 7,
        "ico": [{
            "txt": """   !
  >´)
    \www'
     ||""",
            "esc": None}]
    },
    "karpi": {
        "name": "Karpi",
        "hp": 15,
        "atc": 0,
        "defense": 0,
        "attacks": ["tackle"],
        "pool": [],
        "miss_chance": 0,
        "desc": "A very harmless water Pokete that can be found everywhere.",
        "lose_xp": 1,
        "rarity": 3,
        "types": ["water", "normal"],
        "evolve_poke": "",
        "evolve_lvl": 0,
        "initiative": 0,
        "ico": [{
            "txt": """

  <°))))><
           """,
            "esc": None}]
    },
    "würgos": {
        "name": "Würgos",
        "hp": 20,
        "atc": 3,
        "defense": 0,
        "attacks": ["chocer", "bite", "poison_bite"],
        "pool": [],
        "miss_chance": 0,
        "desc": "A dangerous snake Pokete.",
        "lose_xp": 2,
        "rarity": 1,
        "types": ["poison", "normal", "snake"],
        "evolve_poke": "choka",
        "evolve_lvl": 30,
        "initiative": 3,
        "ico": [{
            "txt": """  >'({{{
  }}}}}}}
 {{{{{{{{{
           """,
            "esc": None}]
    },
    "choka": {
        "name": "Choka",
        "hp": 25,
        "atc": 5,
        "defense": 1,
        "attacks": ["chocer", "bite", "poison_bite", "power_bite"],
        "pool": [],
        "miss_chance": 0,
        "desc": "A fucking dangerous and enormous snake Pokete.",
        "lose_xp": 4,
        "rarity": 0.5,
        "types": ["poison", "normal", "snake"],
        "evolve_poke": "",
        "evolve_lvl": 0,
        "initiative": 4,
        "ico": [{
            "txt": """ _______
/____ * \\
 (   \   \\
\______   \\""",
            "esc": None}]
    },
    "treenator": {
        "name": "Treenator",
        "hp": 25,
        "atc": 2,
        "defense": 2,
        "attacks": ["apple_drop", "bark_hardening", "branch_stab", "root_strangler"],
        "pool": [],
        "miss_chance": 0,
        "desc": "A scary an dangerous apple tree.",
        "lose_xp": 2,
        "rarity": 1,
        "types": ["plant"],
        "evolve_poke": "",
        "evolve_lvl": 0,
        "initiative": 2,
        "ico": [{
            "txt": """    (()
   (()))
     H
     H""",
            "esc": None}]
    },
    "bato": {
        "name": "Bato",
        "hp": 20,
        "atc": 3,
        "defense": 1,
        "attacks": ["bite", "cry"],
        "pool": [],
        "miss_chance": 0,
        "desc": "An annoying flying rat.",
        "lose_xp": 3,
        "rarity": 1.3,
        "types": ["flying", "flying"],
        "evolve_poke": "bator",
        "evolve_lvl": 20,
        "initiative": 6,
        "ico": [{
            "txt": """    ___
WW\/* *\/WW
   \\v-v/""",
            "esc": None}]
    },
    "bator": {
        "name": "Bator",
        "hp": 25,
        "atc": 4,
        "defense": 2,
        "attacks": ["bite", "cry", "poison_bite", "wing_hit"],
        "pool": [],
        "miss_chance": 0,
        "desc": "A chongus flying rat.",
        "lose_xp": 4,
        "rarity": 0.2,
        "types": ["flying", "normal"],
        "evolve_poke": "",
        "evolve_lvl": 0,
        "initiative": 8,
        "ico": [{
            "txt": """    ___
WW\/o o\/WW
   |v-v|
   \\___/""",
            "esc": None}]
    },
    "blub": {
        "name": "Blub",
        "hp": 20,
        "atc": 2,
        "defense": 1,
        "attacks": ["tackle", "bubble_bomb", "bubble_shield"],
        "pool": [],
        "miss_chance": 0,
        "desc": "Very delicious and low fat water Pokete.",
        "lose_xp": 5,
        "rarity": 1,
        "types": ["water", "normal"],
        "evolve_poke": "",
        "evolve_lvl": 0,
        "initiative": 1,
        "ico": [{
            "txt": """  _____
 / o   \\
 >   v  ><
 \_____/""",
            "esc": None}]
    },
    "owol": {
        "name": "Owol",
        "hp": 20,
        "atc": 7,
        "defense": 2,
        "attacks": ["pick", "wing_hit", "cry"],
        "pool": ["cry"],
        "miss_chance": 0,
        "desc": "A night active Pokete, that is looking for lil children as a midnight snack.",
        "lose_xp": 2,
        "rarity": 0.5,
        "types": ["flying", "normal", "bird"],
        "evolve_poke": "",
        "evolve_lvl": 0,
        "initiative": 3,
        "ico": [{
            "txt": """   ,___,
   {o,o}
   /)_)
    ""
""",
            "esc": None}]
    },
    "rato": {
        "name": "Rato",
        "hp": 20,
        "atc": 4,
        "defense": 2,
        "attacks": ["tackle", "tail_wipe"],
        "pool": ["bite", "power_bite"],
        "miss_chance": 0,
        "desc": "An annoying rat.",
        "lose_xp": 2,
        "rarity": 1.3,
        "types": ["normal"],
        "evolve_poke": "",
        "evolve_lvl": 0,
        "initiative": 6,
        "ico": [{
            "txt": """   ^---^
   \o o/
   >\./<""",
            "esc": None}]
    },
    "hornita": {
        "name": "Hornita",
        "hp": 20,
        "atc": 6,
        "defense": 2,
        "attacks": ["tackle", "meat_skewer", "tail_wipe"],
        "pool": [],
        "miss_chance": 0,
        "desc": "An majestic horse that is always looking for something to pick with its horn.",
        "lose_xp": 3,
        "rarity": 1,
        "types": ["normal"],
        "evolve_poke": "",
        "evolve_lvl": 0,
        "initiative": 3,
        "ico": [{
            "txt": """ \\
 =')~
   (¯¯¯¯)~
   //¯¯\\\\""",
            "esc": None}]
    },
    "horny": {
        "name": "Horny",
        "hp": 20,
        "atc": 5,
        "defense": 1,
        "attacks": ["tackle", "meat_skewer"],
        "pool": ["tail_wipe"],
        "miss_chance": 0.2,
        "desc": "A teenage unicorn in the middle of puberty.",
        "rarity": 1,
        "lose_xp": 2,
        "types": ["normal"],
        "evolve_poke": "hornita",
        "evolve_lvl": 20,
        "initiative": 4,
        "ico": [{
            "txt": """  ,
 =')
   (¯¯¯)~
   //¯\\\\""",
            "esc": None}]
    },
    "bushy": {
        "name": "Bushy",
        "hp": 25,
        "atc": 2,
        "defense": 1,
        "attacks": ["tackle", "bark_hardening"],
        "pool": ["apple_drop"],
        "miss_chance": 0,
        "desc": "A bush, and just a bush. But watch out!",
        "lose_xp": 1,
        "rarity": 1,
        "types": ["plant", "normal"],
        "evolve_poke": "treenator",
        "evolve_lvl": 20,
        "initiative": 1,
        "ico": [{
            "txt": """
    (()
   (()))""",
            "esc": None}]
    },
    "wolfior": {
        "name": "Wolfior",
        "hp": 20,
        "atc": 6,
        "defense": 3,
        "attacks": ["tackle", "fire_bite", "ash_throw"],
        "pool": ["cry", "bite", "power_bite"],
        "miss_chance": 0,
        "desc": "A fiery wolf straight from hell, that likes to burn 11 years old butts of.",
        "lose_xp": 2,
        "rarity": 1,
        "types": ["fire", "normal"],
        "evolve_poke": "wolfiro",
        "evolve_lvl": 25,
        "initiative": 4,
        "ico": [{
            "txt": """   ^---^
   (   )
   >(.)<""",
            "esc": None},
            {
                "txt": """
    * *
        """,
                "esc": ["thicc", "red"]}]
    },
    "wolfiro": {
        "name": "Wolfiro",
        "hp": 25,
        "atc": 7,
        "defense": 4,
        "attacks": ["tackle", "fire_bite", "ash_throw", "fire_ball"],
        "pool": ["cry", "bite", "power_bite"],
        "miss_chance": 0,
        "desc": "A fiery wolf from hell on steroids.",
        "lose_xp": 4,
        "rarity": 1,
        "types": ["fire", "normal"],
        "evolve_poke": "",
        "evolve_lvl": 0,
        "initiative": 5,
        "ico": [{
            "txt": """   \^-^/
   {   }
   >{.}<""",
            "esc": None},
            {
                "txt": """
    * *
        """,
                "esc": ["thicc", "red"]}]
    },
    "rollator": {
        "name": "Rollator",
        "hp": 25,
        "atc": 2,
        "defense": 5,
        "attacks": ["tackle", "power_roll"],
        "pool": ["hiding"],
        "miss_chance": 0,
        "desc": "A big chunk of stone and dirt, that roles around.",
        "lose_xp": 3,
        "rarity": 0.5,
        "types": ["ground", "normal"],
        "evolve_poke": "",
        "evolve_lvl": 0,
        "initiative": 3,
        "ico": [{
            "txt": """   _____
  / o o \\
  | ___ |
  \_____/""",
            "esc": None}]
    },
    "clampi": {
        "name": "Clampi",
        "hp": 25,
        "atc": 2,
        "defense": 7,
        "attacks": ["tackle", "bubble_bomb", "shell_pinch"],
        "pool": [],
        "miss_chance": 0,
        "desc": "A shell that lives deep in the see or near bays, that's pretty hard to crack.",
        "lose_xp": 5,
        "rarity": 0.8,
        "types": ["water", "normal"],
        "evolve_poke": "",
        "evolve_lvl": 0,
        "initiative": 3,
        "ico": [{
            "txt": """    ___
  -/   \-
  -\___/-""",
            "esc": None},
            {
                "txt": """
     *""",
                "esc": ["lightblue"]}]
    },
    "electrode": {
        "name": "Electrode",
        "hp": 20,
        "atc": 5,
        "defense": 2,
        "attacks": ["shock", "charging", "mega_arch"],
        "pool": [],
        "miss_chance": 0,
        "desc": "A small floating ball that will give you a shock.",
        "lose_xp": 3,
        "rarity": 0.8,
        "types": ["electro"],
        "evolve_poke": "",
        "evolve_lvl": 0,
        "initiative": 4,
        "ico": [{
            "txt": """
    ( )""",
            "esc": None},
            {
                "txt": """
     +""",
                "esc": ["lightblue"]}]
    },
    "cubl": {
        "name": "Cubl",
        "hp": 20,
        "atc": 3,
        "defense": 3,
        "attacks": ["tackle", "freeze", "snow_storm"],
        "pool": [],
        "miss_chance": 0.1,
        "desc": "A small ice cube.",
        "lose_xp": 2,
        "rarity": 1.2,
        "types": ["ice", "normal"],
        "evolve_poke": "spikl",
        "evolve_lvl": 30,
        "initiative": 1,
        "ico": [{
            "txt": """   -----
   |   |
   -----""",
            "esc": None},
            {
                "txt": """
    * *""",
                "esc": ["lightblue"]},
            {
                "txt": """  /     \\

  \     /""",
                "esc": ["cyan"]
            }
        ]
    },
    "spikl": {
        "name": "Spikl",
        "hp": 25,
        "atc": 4,
        "defense": 4,
        "attacks": ["tackle", "freeze", "snow_storm", "sword_of_ice"],
        "pool": [],
        "miss_chance": 0.1,
        "desc": "A block of ice.",
        "lose_xp": 4,
        "rarity": 0.9,
        "types": ["ice", "normal", "water"],
        "evolve_poke": "",
        "evolve_lvl": 0,
        "initiative": 2,
        "ico": [{
            "txt": """  -------
  |     |
  -------""",
            "esc": None},
            {
                "txt": """
    * *""",
                "esc": ["lightblue"]},
            {
                "txt": """ /       \\

 \       /""",
                "esc": ["cyan"]
            }
        ]
    },
    "confuso": {
        "name": "Confuso",
        "hp": 20,
        "atc": 1,
        "defense": 1,
        "attacks": ["confusion"],
        "pool": [],
        "miss_chance": 0.1,
        "desc": "A ball floating around in dark woods and caves, that will confuse the shit out of you.",
        "lose_xp": 6,
        "rarity": 0.5,
        "types": ["undead"],
        "evolve_poke": "",
        "evolve_lvl": 0,
        "initiative": 2,
        "ico": [{
            "txt": """
     _
    (_) """,
            "esc": None},
            {
                "txt": """        }
      {
       }""",
                "esc": ["purple"]},
            {
                "txt": """       }
       {""",
                "esc": ["lightblue"]},
        ]
    },
    "poisopla": {
        "name": "Poisopla",
        "hp": 20,
        "atc": 3,
        "defense": 3,
        "attacks": ["root_slap", "poison_spores", "leaf_storm"],
        "pool": ["poison_thorn"],
        "miss_chance": 0.1,
        "desc": "A unsuspicious plant.",
        "lose_xp": 6,
        "rarity": 0.9,
        "types": ["plant", "poison"],
        "evolve_poke": "megapois",
        "evolve_lvl": 20,
        "initiative": 1,
        "ico": [{
            "txt": """
       .
 .__ |/|
  \_\||/""",
            "esc": None},
            {
                "txt": """
     w""",
                "esc": ["purple"]},
        ]
    },
    "megapois": {
        "name": "Megapois",
        "hp": 25,
        "atc": 3,
        "defense": 5,
        "attacks": ["root_slap", "poison_spores", "leaf_storm", "poison_thorn"],
        "pool": [],
        "miss_chance": 0.1,
        "desc": "A very unsuspicious plant.",
        "lose_xp": 6,
        "rarity": 0.9,
        "types": ["plant", "poison"],
        "evolve_poke": "",
        "evolve_lvl": 0,
        "initiative": 2,
        "ico": [{
            "txt": """
    |/.
.__\|/|
 \_\||/ """,
            "esc": None},
            {
                "txt": """    w w
  w""",
                "esc": ["purple"]},
        ]
    },
    "schmetterling": {
        "name": "Schmetterling",
        "hp": 20,
        "atc": 4,
        "defense": 2,
        "attacks": ["schmetter", "wing_hit"],
        "pool": [],
        "miss_chance": 0.1,
        "desc": "A butterfly that will schmetter you away.",
        "lose_xp": 3,
        "rarity": 1,
        "types": ["flying"],
        "evolve_poke": "",
        "evolve_lvl": 0,
        "initiative": 4,
        "ico": [{
            "txt": """
 .__ o __.
  \_\|/_/
  /_/'\_\\""",
            "esc": None}
        ]
    },
    "lil_nut": {
        "name": "Lil nut",
        "hp": 20,
        "atc": 1,
        "defense": 3,
        "attacks": ["tackle", "ground_hit"],
        "pool": ["dick_energy", "hiding"],
        "miss_chance": 0.1,
        "desc": "A very small what ever, that sticks out of the ground.",
        "lose_xp": 2,
        "rarity": 1,
        "types": ["ground", "normal"],
        "evolve_poke": "dicki",
        "evolve_lvl": 35,
        "initiative": 1,
        "ico": [{
            "txt": """

    __
   ('')""",
            "esc": None}
        ]
    },
    "dicki": {
        "name": "Dicki",
        "hp": 20,
        "atc": 2,
        "defense": 4,
        "attacks": ["tackle", "dick_energy", "hiding", "ground_hit"],
        "pool": [],
        "miss_chance": 0.1,
        "desc": "A little what ever, that sticks out of the ground.",
        "lose_xp": 2,
        "rarity": 1,
        "types": ["ground", "normal"],
        "evolve_poke": "dicko",
        "evolve_lvl": 55,
        "initiative": 2,
        "ico": [{
            "txt": """    
    __
   ('')
   |  |""",
            "esc": None}
        ]
    },
    "dicko": {
        "name": "Dicko",
        "hp": 25,
        "atc": 3,
        "defense": 5,
        "attacks": ["tackle", "dick_energy", "hiding", "ground_hit"],
        "pool": [],
        "miss_chance": 0.1,
        "desc": "An even bigger what ever, that sticks out of the ground.",
        "lose_xp": 2,
        "rarity": 1,
        "types": ["ground", "normal"],
        "evolve_poke": "",
        "evolve_lvl": 0,
        "initiative": 3,
        "ico": [{
            "txt": """    __
   ('')
   |  |
   |  |""",
            "esc": None}
        ]
    },
    "diamondos": {
        "name": "Diamondos",
        "hp": 20,
        "atc": 2,
        "defense": 15,
        "attacks": ["tackle", "politure", "dazzle"],
        "pool": ["dia_stab", "dia_spikes"],
        "miss_chance": 0.1,
        "desc": "A precious diamond, that can only be found in the darkest caves.",
        "lose_xp": 2,
        "rarity": 1,
        "types": ["stone"],
        "evolve_poke": "",
        "evolve_lvl": 0,
        "initiative": 2,
        "ico": [{
            "txt": """

    o o
     -""",
            "esc": None},
            {
                "txt": """
    /\ /
       >
   <_""",
                "esc": ["cyan"]},
            {
                "txt": """
      ^
   <
      _>""",
                "esc": ["white"]}
        ]
    },
}

if __name__ == "__main__":
    print("\033[31;1mDo not execute this!\033[0m")
