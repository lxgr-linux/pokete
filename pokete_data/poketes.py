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
        "attacs": [],
        "miss_chance": 0,
        "desc": "",
        "lose_xp": 0,
        "rarity": 0,
        "type": "normal",
        "evolve_poke": "",
        "evolve_lvl": 0,
        "ico": """ """,
    },
    "steini": {
        "name": "Steini",
        "hp": 25,
        "atc": "self.lvl()+2",
        "defense": "self.lvl()+4",
        "attacs": ["tackle", "politure", "brick_throw"],
        "miss_chance": 0,
        "desc": "A squared stone that can casually be found on the ground.",
        "lose_xp": 3,
        "rarity": 1,
        "type": "stone",
        "evolve_poke": "",
        "evolve_lvl": 0,
        "ico": """ +-------+
 | o   o |
 |  www  |
 +-------+ """,
    },
    "poundi": {
        "name": "Poundi",
        "hp": 25,
        "atc": "self.lvl()+2",
        "defense": "self.lvl()+3",
        "attacs": ["tackle", "politure", "earch_quake"],
        "miss_chance": 0,
        "desc": "A powerfull and heavy stone Pokete that lives in mountain caves.",
        "lose_xp": 4,
        "rarity": 0.7,
        "type": "stone",
        "evolve_poke": "",
        "evolve_lvl": 0,
        "ico": """   A-A-A
  < o o >
  < --- >
   VvVvV""",
   },
   "lilstone": {
       "name": "Lilstone",
       "hp": 20,
       "atc": "self.lvl()+1",
       "defense": "self.lvl()+2",
       "attacs": ["tackle", "politure", "pepple_fire"],
       "miss_chance": 0,
       "desc": "A small but powerfull stone Pokete that lives in the mountains.",
       "lose_xp": 2,
       "rarity": 1,
       "type": "stone",
       "evolve_poke": "",
       "evolve_lvl": 0,
       "ico": """
   _____
   |'ᵕ'|
   ‾‾‾‾‾""",
  },
  "rosi": {
      "name": "Rosi",
      "hp": 20,
      "atc": "self.lvl()",
      "defense": "self.lvl()+1",
      "attacs": ["sucker", "super_sucker"],
      "miss_chance": 0,
      "desc": "A plant Pokete, that's often mistaken for a normal flower.",
      "lose_xp": 2,
      "rarity": 0.8,
      "type": "plant",
      "evolve_poke": "",
      "evolve_lvl": 0,
      "ico": """
    (@)
     |
    \|/""",
 },
  "gobost": {
      "name": "Gobost",
      "hp": 20,
      "atc": "self.lvl()+2",
      "defense": "self.lvl()+1",
      "attacs": ["tackle", "mind_blow", "heard_touch"],
      "miss_chance": 0,
      "desc": "A scary ghost Pokete that lives in caves and old houses.",
      "lose_xp": 3,
      "rarity": 1,
      "type": "undead",
      "evolve_poke": "angrilo",
      "evolve_lvl": 25,
      "ico": """ .░░░░░░░.
 ░░o░░░o░░
 ░░░░░░░░░
 ░ ░ ░ ░ ░""",
  },
   "angrilo": {
       "name": "Angrilo",
       "hp": 25,
       "atc": "self.lvl()+3",
       "defense": "self.lvl()+2",
       "attacs": ["tackle", "mind_blow", "heard_touch"],
       "miss_chance": 0,
       "desc": "A ghost Pokete that will scare your pants off.",
       "lose_xp": 4,
       "rarity": 0.6,
       "type": "undead",
       "evolve_poke": "",
       "evolve_lvl": 0,
       "ico": """ .░░░░░░░.
 ░░\░░░/░░
 .░░( )░░.
.         .""",
   },
  "vogli": {
        "name": "Vogli",
        "hp": 20,
        "atc": "self.lvl()+6",
        "defense": "self.lvl()+1",
        "attacs": ["tackle", "power_pick"],
        "miss_chance": 0,
        "desc": "A very common bird Pokete that lives everywhere.",
        "lose_xp": 2,
        "rarity": 1,
        "type": "flying",
        "evolve_poke": "voglo",
        "evolve_lvl": 20,
        "ico":"""    A
   <')
    www*
    ||     """
    },
    "voglo": {
        "name": "Voglo",
        "hp": 20,
        "atc": "self.lvl()+7",
        "defense": "self.lvl()+1",
        "attacs": ["tackle", "power_pick", "wing_hit", "brooding"],
        "miss_chance": 0,
        "desc": "A very agressive bird Pokete that can only be found in the woods.",
        "lose_xp": 3,
        "rarity": 0.8,
        "type": "flying",
        "evolve_poke": "",
        "evolve_lvl": 0,
        "ico":"""    ?
   >´)
    www*
    ||     """
    },
    "ostri": {
        "name": "Ostri",
        "hp": 20,
        "atc": "self.lvl()+8",
        "defense": "self.lvl()",
        "attacs": ["tackle", "eye_pick", "brooding"],
        "miss_chance": 0,
        "desc": "A very agressive bird Pokete that lives near deserts and will try to pick out your eyes.",
        "rarity": 0.6,
        "lose_xp": 4,
        "type": "flying",
        "evolve_poke": "",
        "evolve_lvl": 0,
        "ico":"""   !
  >´)
    \www'
     ||"""
    },
    "karpi": {
        "name": "Karpi",
        "hp": 15,
        "atc": "self.lvl()",
        "defense": "self.lvl()/2",
        "attacs": ["tackle"],
        "miss_chance": 0,
        "desc": "A very harmless water Pokete that can be found everywhere.",
        "lose_xp": 1,
        "rarity": 3,
        "type": "water",
        "evolve_poke": "",
        "evolve_lvl": 0,
        "ico":"""

  <°))))><
           """
    },
    "würgos": {
        "name": "Würgos",
        "hp": 20,
        "atc": "self.lvl()+3",
        "defense": "self.lvl()",
        "attacs": ["chocer", "bite", "poison_bite"],
        "miss_chance": 0,
        "desc": "A dangerous snake Pokete.",
        "lose_xp": 2,
        "rarity": 1,
        "type": "normal",
        "evolve_poke": "choka",
        "evolve_lvl": 25,
        "ico": """  >'({{{
  }}}}}}}
 {{{{{{{{{
           """
    },
    "choka": {
        "name": "Choka",
        "hp": 25,
        "atc": "self.lvl()+5",
        "defense": "self.lvl()+1",
        "attacs": ["chocer", "bite", "poison_bite"],
        "miss_chance": 0,
        "desc": "A dangerous and enormous snake pokete.",
        "lose_xp": 4,
        "rarity": 0.5,
        "type": "normal",
        "evolve_poke": "",
        "evolve_lvl": 0,
        "ico": """ _______
/____ * \\
 (   \   \\
\______   \\"""
    },
    "treenator": {
        "name": "Treenator",
        "hp": 25,
        "atc": "self.lvl()+2",
        "defense": "self.lvl()+2",
        "attacs": ["apple_drop", "bark_hardening", "branch_stab"],
        "miss_chance": 0,
        "desc": "A scary an dangerous apple tree.",
        "lose_xp": 2,
        "rarity": 1,
        "type": "plant",
        "evolve_poke": "",
        "evolve_lvl": 0,
        "ico": """    (()
   (()))
     H
     H"""
    },
    "bato": {
        "name": "Bato",
        "hp": 20,
        "atc": "self.lvl()+3",
        "defense": "self.lvl()+1",
        "attacs": ["bite", "cry"],
        "miss_chance": 0,
        "desc": "An annoying flying rat.",
        "lose_xp": 3,
        "rarity": 1.3,
        "type": "flying",
        "evolve_poke": "bator",
        "evolve_lvl": 20,
        "ico": """    ___
WW\/* *\/WW
   \\v-v/
"""
    },
    "bator": {
        "name": "Bator",
        "hp": 25,
        "atc": "self.lvl()+4",
        "defense": "self.lvl()+2",
        "attacs": ["bite", "cry", "poison_bite", "wing_hit"],
        "miss_chance": 0,
        "desc": "A chongus flying rat.",
        "lose_xp": 4,
        "rarity": 0.2,
        "type": "flying",
        "evolve_poke": "",
        "evolve_lvl": 0,
        "ico": """    ___
WW\/o o\/WW
   |v-v|
   \\___/
"""
    },
    "blub": {
        "name": "Blub",
        "hp": 20,
        "atc": "self.lvl()+2",
        "defense": "self.lvl()+1",
        "attacs": ["tackle", "bubble_bomb", "bubble_shield"],
        "miss_chance": 0,
        "desc": "Very delicious and low fat water Pokete.",
        "lose_xp": 5,
        "rarity": 1,
        "type": "water",
        "evolve_poke": "",
        "evolve_lvl": 0,
        "ico": """  _____
 / o   \\
 >   v  ><
 \_____/"""
    },
    "owol": {
        "name": "Owol",
        "hp": 20,
        "atc": "self.lvl()+7",
        "defense": "self.lvl()+2",
        "attacs": ["pick", "wing_hit", "cry"],
        "miss_chance": 0,
        "desc": "A night active Pokete, that is looking for lil children as a midnight snack.",
        "lose_xp": 2,
        "rarity": 0.5,
        "type": "flying",
        "evolve_poke": "",
        "evolve_lvl": 0,
        "ico": """   ,___,
   {o,o}
   /)_)
    ""
"""
    },
    "rato": {
        "name": "Rato",
        "hp": 20,
        "atc": "self.lvl()+4",
        "defense": "self.lvl()+2",
        "attacs": ["tackle", "tail_wipe"],
        "miss_chance": 0,
        "desc": "An annoying rat.",
        "lose_xp": 2,
        "rarity": 1.3,
        "type": "normal",
        "evolve_poke": "",
        "evolve_lvl": 0,
        "ico": """   ^---^
   \o o/
   >\./<
"""
    },
    "hornita": {
        "name": "Hornita",
        "hp": 20,
        "atc": "self.lvl()+6",
        "defense": "self.lvl()+2",
        "attacs": ["tackle", "meat_skewer", "tail_wipe"],
        "miss_chance": 0,
        "desc": "An majestetic horse that is always looking for something to pick with its horn.",
        "lose_xp": 3,
        "rarity": 1,
        "type": "normal",
        "evolve_poke": "",
        "evolve_lvl": 0,
        "ico": """ \\
 =')~
   (¯¯¯¯)~
   //¯¯\\\\"""
    },
    "horny": {
        "name": "Horny",
        "hp": 20,
        "atc": "self.lvl()+5",
        "defense": "self.lvl()+1",
        "attacs": ["tackle", "meat_skewer"],
        "miss_chance": 0.2,
        "desc": "A teenaged unicorn in the middle of puberty.",
        "rarity": 1,
        "lose_xp": 2,
        "type": "normal",
        "evolve_poke": "hornita",
        "evolve_lvl": 20,
        "ico": """  ,
 =')
   (¯¯¯)~
   //¯\\\\"""
    },
    "bushy": {
        "name": "Bushy",
        "hp": 25,
        "atc": "self.lvl()+2",
        "defense": "self.lvl()+1",
        "attacs": ["tackle", "bark_hardening"],
        "miss_chance": 0,
        "desc": "A bush, and just a bush. But watch out!",
        "lose_xp": 1,
        "rarity": 1,
        "type": "plant",
        "evolve_poke": "treenator",
        "evolve_lvl": 20,
        "ico": """
    (()
   (()))"""
    },
    "wolfior": {
        "name": "Wolfior",
        "hp": 20,
        "atc": "self.lvl()+6",
        "defense": "self.lvl()+3",
        "attacs": ["tackle", "fire_bite"],
        "miss_chance": 0,
        "desc": "A fiery wolf straight from hell, that likes to burn 11 years old butts of.",
        "lose_xp": 2,
        "rarity": 1,
        "type": "fire",
        "evolve_poke": "",
        "evolve_lvl": 0,
        "ico": """   ^---^
   (* *)
   >(.)<"""
    },
    "rollator": {
        "name": "Rollator",
        "hp": 25,
        "atc": "self.lvl()+2",
        "defense": "self.lvl()+5",
        "attacs": ["tackle", "power_roll"],
        "miss_chance": 0,
        "desc": "A big chunck of stone and dirt, that roles around.",
        "lose_xp": 3,
        "rarity": 0.5,
        "type": "ground",
        "evolve_poke": "",
        "evolve_lvl": 0,
        "ico": """   _____
  / o o \\
  | ___ |
  \_____/"""
    },
    "clampi": {
        "name": "Clampi",
        "hp": 25,
        "atc": "self.lvl()+2",
        "defense": "self.lvl()+7",
        "attacs": ["tackle", "bubble_bomb", "shell_pinch"],
        "miss_chance": 0,
        "desc": "A shell that lives deep in the see or near bays, that's pretty hard to crack.",
        "lose_xp": 5,
        "rarity": 0.8,
        "type": "water",
        "evolve_poke": "",
        "evolve_lvl": 0,
        "ico": """    ___
  -/ * \-
  -\___/-
"""
    },
}

if __name__ == "__main__":
    print("\033[31;1mDo not execute this!\033[0m")
