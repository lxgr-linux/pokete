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
        "atc": "0",
        "defense": "0",
        "attacks": [],
        "miss_chance": 0,
        "desc": "",
        "lose_xp": 0,
        "rarity": 0,
        "type": "normal",
        "evolve_poke": "",
        "evolve_lvl": 0,
        "initiative": "self.lvl()",
        "ico": [{
            "txt": """ """,
            "esc": None}],
    },
    "steini": {
        "name": "Steini",
        "hp": 25,
        "atc": "self.lvl()+2",
        "defense": "self.lvl()+4",
        "attacks": ["tackle", "politure", "brick_throw"],
        "miss_chance": 0,
        "desc": "A squared stone that can casually be found on the ground.",
        "lose_xp": 3,
        "rarity": 1,
        "type": "stone",
        "evolve_poke": "",
        "evolve_lvl": 0,
        "initiative": "self.lvl()+5",
        "ico": [{
            "txt": """ +-------+
 | o   o |
 |  www  |
 +-------+ """,
            "esc": None}],
    },
    "bigstone": {
        "name": "Bigstone",
        "hp": 30,
        "atc": "self.lvl()+2",
        "defense": "self.lvl()+13",
        "attacks": ["snooze", "politure", "brick_throw"],
        "miss_chance": 0,
        "desc": "A big and heavy stone made from one of the hardest stones.",
        "lose_xp": 5,
        "rarity": 0.3,
        "type": "stone",
        "evolve_poke": "",
        "evolve_lvl": 0,
        "initiative": "self.lvl()+5",
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
        "atc": "self.lvl()+2",
        "defense": "self.lvl()+3",
        "attacks": ["tackle", "politure", "earch_quake"],
        "miss_chance": 0,
        "desc": "A powerfull and heavy stone Pokete that lives in mountain caves.",
        "lose_xp": 4,
        "rarity": 0.7,
        "type": "stone",
        "evolve_poke": "",
        "evolve_lvl": 0,
        "initiative": "self.lvl()+4",
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
       "atc": "self.lvl()+1",
       "defense": "self.lvl()+2",
       "attacks": ["tackle", "politure", "pepple_fire"],
       "miss_chance": 0,
       "desc": "A small but powerfull stone Pokete that lives in the mountains.",
       "lose_xp": 2,
       "rarity": 1,
       "type": "stone",
       "evolve_poke": "bigstone",
       "evolve_lvl": 25,
       "initiative": "self.lvl()+3",
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
      "atc": "self.lvl()",
      "defense": "self.lvl()+1",
      "attacks": ["sucker", "super_sucker"],
      "miss_chance": 0,
      "desc": "A plant Pokete, that's often mistaken for a normal flower.",
      "lose_xp": 2,
      "rarity": 0.8,
      "type": "plant",
      "evolve_poke": "",
      "evolve_lvl": 0,
      "initiative": "self.lvl()+3",
      "ico": [{
            "txt": """
    (@)
     |
    \|/""",
            "esc": None}],
 },
  "gobost": {
      "name": "Gobost",
      "hp": 20,
      "atc": "self.lvl()+2",
      "defense": "self.lvl()+1",
      "attacks": ["tackle", "mind_blow", "heart_touch"],
      "miss_chance": 0,
      "desc": "A scary ghost Pokete that lives in caves and old houses.",
      "lose_xp": 3,
      "rarity": 1,
      "type": "undead",
      "evolve_poke": "angrilo",
      "evolve_lvl": 25,
      "initiative": "self.lvl()+6",
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
       "atc": "self.lvl()+3",
       "defense": "self.lvl()+2",
       "attacks": ["tackle", "mind_blow", "wet_slap", "heart_touch"],
       "miss_chance": 0,
       "desc": "A ghost Pokete that will scare your pants off.",
       "lose_xp": 4,
       "rarity": 0.6,
       "type": "undead",
       "evolve_poke": "",
       "evolve_lvl": 0,
       "initiative": "self.lvl()+7",
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
        "atc": "self.lvl()+6",
        "defense": "self.lvl()+1",
        "attacks": ["tackle", "power_pick"],
        "miss_chance": 0,
        "desc": "A very common bird Pokete that lives everywhere.",
        "lose_xp": 2,
        "rarity": 1,
        "type": "flying",
        "evolve_poke": "voglo",
        "initiative": "self.lvl()+6",
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
        "atc": "self.lvl()+7",
        "defense": "self.lvl()+1",
        "attacks": ["tackle", "power_pick", "wing_hit", "brooding"],
        "miss_chance": 0,
        "desc": "A very agressive bird Pokete that can only be found in the woods.",
        "lose_xp": 3,
        "rarity": 0.8,
        "type": "flying",
        "evolve_poke": "",
        "evolve_lvl": 0,
        "initiative": "self.lvl()+7",
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
        "atc": "self.lvl()+8",
        "defense": "self.lvl()",
        "attacks": ["tackle", "eye_pick", "brooding"],
        "miss_chance": 0,
        "desc": "A very agressive bird Pokete that lives near deserts and will try to pick out your eyes.",
        "rarity": 0.6,
        "lose_xp": 4,
        "type": "flying",
        "evolve_poke": "",
        "evolve_lvl": 0,
        "initiative": "self.lvl()+7",
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
        "atc": "self.lvl()",
        "defense": "self.lvl()/2",
        "attacks": ["tackle"],
        "miss_chance": 0,
        "desc": "A very harmless water Pokete that can be found everywhere.",
        "lose_xp": 1,
        "rarity": 3,
        "type": "water",
        "evolve_poke": "",
        "evolve_lvl": 0,
        "initiative": "self.lvl()",
        "ico": [{
            "txt": """

  <°))))><
           """,
            "esc": None}]
    },
    "würgos": {
        "name": "Würgos",
        "hp": 20,
        "atc": "self.lvl()+3",
        "defense": "self.lvl()",
        "attacks": ["chocer", "bite", "poison_bite"],
        "miss_chance": 0,
        "desc": "A dangerous snake Pokete.",
        "lose_xp": 2,
        "rarity": 1,
        "type": "normal",
        "evolve_poke": "choka",
        "evolve_lvl": 30,
        "initiative": "self.lvl()+3",
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
        "atc": "self.lvl()+5",
        "defense": "self.lvl()+1",
        "attacks": ["chocer", "bite", "poison_bite", "power_bite"],
        "miss_chance": 0,
        "desc": "A fucking dangerous and enormous snake pokete.",
        "lose_xp": 4,
        "rarity": 0.5,
        "type": "normal",
        "evolve_poke": "",
        "evolve_lvl": 0,
        "initiative": "self.lvl()+4",
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
        "atc": "self.lvl()+2",
        "defense": "self.lvl()+2",
        "attacks": ["apple_drop", "bark_hardening", "branch_stab", "root_strangler"],
        "miss_chance": 0,
        "desc": "A scary an dangerous apple tree.",
        "lose_xp": 2,
        "rarity": 1,
        "type": "plant",
        "evolve_poke": "",
        "evolve_lvl": 0,
        "initiative": "self.lvl()+2",
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
        "atc": "self.lvl()+3",
        "defense": "self.lvl()+1",
        "attacks": ["bite", "cry"],
        "miss_chance": 0,
        "desc": "An annoying flying rat.",
        "lose_xp": 3,
        "rarity": 1.3,
        "type": "flying",
        "evolve_poke": "bator",
        "evolve_lvl": 20,
        "initiative": "self.lvl()+6",
        "ico": [{
            "txt": """    ___
WW\/* *\/WW
   \\v-v/""",
            "esc": None}]
    },
    "bator": {
        "name": "Bator",
        "hp": 25,
        "atc": "self.lvl()+4",
        "defense": "self.lvl()+2",
        "attacks": ["bite", "cry", "poison_bite", "wing_hit"],
        "miss_chance": 0,
        "desc": "A chongus flying rat.",
        "lose_xp": 4,
        "rarity": 0.2,
        "type": "flying",
        "evolve_poke": "",
        "evolve_lvl": 0,
        "initiative": "self.lvl()+8",
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
        "atc": "self.lvl()+2",
        "defense": "self.lvl()+1",
        "attacks": ["tackle", "bubble_bomb", "bubble_shield"],
        "miss_chance": 0,
        "desc": "Very delicious and low fat water Pokete.",
        "lose_xp": 5,
        "rarity": 1,
        "type": "water",
        "evolve_poke": "",
        "evolve_lvl": 0,
        "initiative": "self.lvl()+1",
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
        "atc": "self.lvl()+7",
        "defense": "self.lvl()+2",
        "attacks": ["pick", "wing_hit", "cry"],
        "miss_chance": 0,
        "desc": "A night active Pokete, that is looking for lil children as a midnight snack.",
        "lose_xp": 2,
        "rarity": 0.5,
        "type": "flying",
        "evolve_poke": "",
        "evolve_lvl": 0,
        "initiative": "self.lvl()+3",
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
        "atc": "self.lvl()+4",
        "defense": "self.lvl()+2",
        "attacks": ["tackle", "tail_wipe"],
        "miss_chance": 0,
        "desc": "An annoying rat.",
        "lose_xp": 2,
        "rarity": 1.3,
        "type": "normal",
        "evolve_poke": "",
        "evolve_lvl": 0,
        "initiative": "self.lvl()+6",
        "ico": [{
            "txt": """   ^---^
   \o o/
   >\./<""",
            "esc": None}]
    },
    "hornita": {
        "name": "Hornita",
        "hp": 20,
        "atc": "self.lvl()+6",
        "defense": "self.lvl()+2",
        "attacks": ["tackle", "meat_skewer", "tail_wipe"],
        "miss_chance": 0,
        "desc": "An majestetic horse that is always looking for something to pick with its horn.",
        "lose_xp": 3,
        "rarity": 1,
        "type": "normal",
        "evolve_poke": "",
        "evolve_lvl": 0,
        "initiative": "self.lvl()+3",
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
        "atc": "self.lvl()+5",
        "defense": "self.lvl()+1",
        "attacks": ["tackle", "meat_skewer"],
        "miss_chance": 0.2,
        "desc": "A teenaged unicorn in the middle of puberty.",
        "rarity": 1,
        "lose_xp": 2,
        "type": "normal",
        "evolve_poke": "hornita",
        "evolve_lvl": 20,
        "initiative": "self.lvl()+4",
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
        "atc": "self.lvl()+2",
        "defense": "self.lvl()+1",
        "attacks": ["tackle", "bark_hardening"],
        "miss_chance": 0,
        "desc": "A bush, and just a bush. But watch out!",
        "lose_xp": 1,
        "rarity": 1,
        "type": "plant",
        "evolve_poke": "treenator",
        "evolve_lvl": 20,
        "initiative": "self.lvl()+1",
        "ico": [{
            "txt": """
    (()
   (()))""",
            "esc": None}]
    },
    "wolfior": {
        "name": "Wolfior",
        "hp": 20,
        "atc": "self.lvl()+6",
        "defense": "self.lvl()+3",
        "attacks": ["tackle", "fire_bite", "ash_throw"],
        "miss_chance": 0,
        "desc": "A fiery wolf straight from hell, that likes to burn 11 years old butts of.",
        "lose_xp": 2,
        "rarity": 1,
        "type": "fire",
        "evolve_poke": "wolfiro",
        "evolve_lvl": 25,
        "initiative": "self.lvl()+4",
        "ico": [{
            "txt": """   ^---^
   (   )
   >(.)<""",
            "esc": None},
        {
            "txt": """
    * *
        """,
            "esc": "Color.thicc+Color.red"}]
    },
    "wolfiro": {
        "name": "Wolfiro",
        "hp": 25,
        "atc": "self.lvl()+7",
        "defense": "self.lvl()+4",
        "attacks": ["tackle", "fire_bite", "ash_throw", "fire_ball"],
        "miss_chance": 0,
        "desc": "A fiery wolf from hell on steroids.",
        "lose_xp": 4,
        "rarity": 1,
        "type": "fire",
        "evolve_poke": "",
        "evolve_lvl": 0,
        "initiative": "self.lvl()+5",
        "ico": [{
            "txt": """   \^-^/
   {   }
   >{.}<""",
            "esc": None},
        {
            "txt": """
    * *
        """,
            "esc": "Color.thicc+Color.red"}]
    },
    "rollator": {
        "name": "Rollator",
        "hp": 25,
        "atc": "self.lvl()+2",
        "defense": "self.lvl()+5",
        "attacks": ["tackle", "power_roll"],
        "miss_chance": 0,
        "desc": "A big chunck of stone and dirt, that roles around.",
        "lose_xp": 3,
        "rarity": 0.5,
        "type": "ground",
        "evolve_poke": "",
        "evolve_lvl": 0,
        "initiative": "self.lvl()+3",
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
        "atc": "self.lvl()+2",
        "defense": "self.lvl()+7",
        "attacks": ["tackle", "bubble_bomb", "shell_pinch"],
        "miss_chance": 0,
        "desc": "A shell that lives deep in the see or near bays, that's pretty hard to crack.",
        "lose_xp": 5,
        "rarity": 0.8,
        "type": "water",
        "evolve_poke": "",
        "evolve_lvl": 0,
        "initiative": "self.lvl()+3",
        "ico": [{
            "txt": """    ___
  -/   \-
  -\___/-""",
            "esc": None},
        {
            "txt": """
     *""",
            "esc": "Color.lightblue"}]
    },
    "electrode": {
        "name": "Electrode",
        "hp": 20,
        "atc": "self.lvl()+5",
        "defense": "self.lvl()+2",
        "attacks": ["shock", "charging", "mega_arch"],
        "miss_chance": 0,
        "desc": "A small floating ball that will give you a shock.",
        "lose_xp": 3,
        "rarity": 0.8,
        "type": "electro",
        "evolve_poke": "",
        "evolve_lvl": 0,
        "initiative": "self.lvl()+4",
        "ico": [{
            "txt": """
    ( )""",
            "esc": None},
        {
            "txt": """
     +""",
            "esc": "Color.lightblue"}]
    },
    "cubl": {
        "name": "Cubl",
        "hp": 20,
        "atc": "self.lvl()+3",
        "defense": "self.lvl()+3",
        "attacks": ["tackle", "freeze", "snow_storm"],
        "miss_chance": 0.1,
        "desc": "A small ice cube.",
        "lose_xp": 2,
        "rarity": 1.2,
        "type": "ice",
        "evolve_poke": "spikl",
        "evolve_lvl": 30,
        "initiative": "self.lvl()+1",
        "ico": [{
            "txt": """   -----
   |   |
   -----""",
            "esc": None},
            {
            "txt": """
    * *""",
            "esc": "Color.lightblue"},
            {
            "txt": """  /     \\

  \     /""",
            "esc": "Color.cyan"
            }
                ]
    },
    "spikl": {
        "name": "Spikl",
        "hp": 25,
        "atc": "self.lvl()+4",
        "defense": "self.lvl()+4",
        "attacks": ["tackle", "freeze", "snow_storm", "sword_of_ice"],
        "miss_chance": 0.1,
        "desc": "A block of ice.",
        "lose_xp": 4,
        "rarity": 0.9,
        "type": "ice",
        "evolve_poke": "",
        "evolve_lvl": 0,
        "initiative": "self.lvl()+2",
        "ico": [{
            "txt": """  -------
  |     |
  -------""",
            "esc": None},
            {
            "txt": """
    * *""",
            "esc": "Color.lightblue"},
            {
            "txt": """ /       \\

 \       /""",
            "esc": "Color.cyan"
            }
                ]
    },
}

if __name__ == "__main__":
    print("\033[31;1mDo not execute this!\033[0m")
