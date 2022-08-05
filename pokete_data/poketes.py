"""Here starts to definition of all the Poketes
  If you want to contribute Poketes, you have to keep in mind, that "ico"
  can be max 11x4 chars big
  and that the max for attacks is (until now) 4
  All attributes have to be present make a Pokete work
  A type has to be present
  Hornita was inspired and partly designed by Pia <pialandrath@gmail.com>"""

pokes = {
    "__fallback__": {
        "name": "",
        "hp": 20,
        "atc": 0,
        "defense": 0,
        "attacks": [],
        "pool": [],
        "miss_chance": 0,
        "desc": "pokete.__fallback__.description",
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
        "desc": "pokete.steini.description",
        "lose_xp": 3,
        "rarity": 1,
        "types": ["stone", "normal"],
        "evolve_poke": "",
        "evolve_lvl": 0,
        "initiative": 5,
        "ico": [{
            "txt": r""" +-------+
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
        "desc": "pokete.mowcow.description",
        "lose_xp": 2,
        "rarity": 1,
        "types": ["normal"],
        "evolve_poke": "",
        "evolve_lvl": 0,
        "initiative": 2,
        "ico": [{
            "txt": r"""    ^__^
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
        "desc": "pokete.bigstone.description",
        "lose_xp": 5,
        "rarity": 0.3,
        "types": ["stone", "normal"],
        "evolve_poke": "",
        "evolve_lvl": 0,
        "initiative": 5,
        "ico": [{
            "txt": r"""+---------+
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
        "desc": "pokete.poundi.description",
        "lose_xp": 4,
        "rarity": 0.7,
        "types": ["stone", "normal"],
        "evolve_poke": "",
        "evolve_lvl": 0,
        "initiative": 4,
        "ico": [{
            "txt": r"""   A-A-A
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
        "desc": "pokete.lilstone.description",
        "lose_xp": 2,
        "rarity": 1,
        "types": ["stone", "normal"],
        "evolve_poke": "bigstone",
        "evolve_lvl": 25,
        "initiative": 3,
        "ico": [{
            "txt": r"""
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
        "desc": "pokete.rosi.description",
        "lose_xp": 2,
        "rarity": 0.8,
        "types": ["plant"],
        "evolve_poke": "",
        "evolve_lvl": 0,
        "initiative": 3,
        "ico": [{
            "txt": r"""
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
        "desc": "pokete.wheeto.description",
        "lose_xp": 2,
        "rarity": 1,
        "types": ["plant"],
        "evolve_poke": "",
        "evolve_lvl": 0,
        "initiative": 2,
        "ico": [{
            "txt": r"""    \ /
    \|/
    \|/
     |""",
            "esc": None}],
    },
    "saugh": {
        "name": "Saugh",
        "hp": 20,
        "atc": 4,
        "defense": 2,
        "attacks": ["mind_blow", "fire_ball", "sand_throw"],
        "pool": ["hiding"],
        "miss_chance": 1,
        "desc": "pokete.saugh.description",
        "lose_xp": 4,
        "rarity": 0.5,
        "types": ["undead", "fire"],
        "evolve_poke": "",
        "evolve_lvl": 0,
        "initiative": 5,
        "ico": [{
            "txt": r"""
    .,
  , .. .
 ...,..,.""",
            "esc": ["yellow"]
                }, {
            "txt": r"""

   *  *""",
            "esc": ["thicc", "red"]
                }],
    },
    "gobost": {
        "name": "Gobost",
        "hp": 20,
        "atc": 2,
        "defense": 1,
        "attacks": ["tackle", "mind_blow", "heart_touch"],
        "pool": ["cry"],
        "miss_chance": 0,
        "desc": "pokete.gobost.description",
        "lose_xp": 3,
        "rarity": 1,
        "types": ["undead", "normal"],
        "evolve_poke": "angrilo",
        "evolve_lvl": 25,
        "initiative": 6,
        "ico": [{
            "txt": r""" .░░░░░░░.
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
        "desc": "pokete.angrilo.description",
        "lose_xp": 4,
        "rarity": 0.6,
        "types": ["undead", "normal", "water"],
        "evolve_poke": "",
        "evolve_lvl": 0,
        "initiative": 7,
        "ico": [{
            "txt": r""" .░░░░░░░.
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
        "desc": "pokete.vogli.description",
        "lose_xp": 2,
        "rarity": 1,
        "types": ["flying", "normal", "bird"],
        "evolve_poke": "voglo",
        "initiative": 6,
        "evolve_lvl": 20,
        "ico": [{
            "txt": r"""    A
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
        "desc": "pokete.voglo.description",
        "lose_xp": 3,
        "rarity": 0.8,
        "types": ["flying", "normal", "bird"],
        "evolve_poke": "voglus",
        "evolve_lvl": 35,
        "initiative": 7,
        "ico": [{
            "txt": r"""    ?
   >´)
    www*
    ||     """,
            "esc": None}]
    },
    "voglus": {
        "name": "Voglus",
        "hp": 25,
        "atc": 9,
        "defense": 3,
        "attacks": ["tackle", "power_pick", "storm_gust", "brooding"],
        "pool": ["cry"],
        "miss_chance": 0,
        "desc": "pokete.voglus.description",
        "lose_xp": 5,
        "rarity": 0.2,
        "types": ["flying", "normal", "bird"],
        "evolve_poke": "",
        "evolve_lvl": 0,
        "initiative": 8,
        "ico": [{
            "txt": r"""    /
   > }
    WWW'
    ||""",
            "esc": None}, {
            "txt": """
    ´""",
            "esc": ["thicc", "red"]}]
    },
    "ostri": {
        "name": "Ostri",
        "hp": 20,
        "atc": 8,
        "defense": 0,
        "attacks": ["tackle", "eye_pick", "brooding"],
        "pool": ["cry"],
        "miss_chance": 0,
        "desc": "pokete.ostri.description",
        "rarity": 0.6,
        "lose_xp": 4,
        "types": ["flying", "normal", "bird"],
        "evolve_poke": "",
        "evolve_lvl": 0,
        "initiative": 7,
        "ico": [{
            "txt": r"""   !
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
        "desc": "pokete.karpi.description",
        "lose_xp": 1,
        "rarity": 3,
        "types": ["water", "normal"],
        "evolve_poke": "",
        "evolve_lvl": 0,
        "initiative": 0,
        "ico": [{
            "txt": r"""

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
        "desc": "pokete.würgos.description",
        "lose_xp": 2,
        "rarity": 1,
        "types": ["poison", "normal", "snake"],
        "evolve_poke": "choka",
        "evolve_lvl": 30,
        "initiative": 3,
        "ico": [{
            "txt": r"""  >'({{{
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
        "desc": "pokete.choka.description",
        "lose_xp": 4,
        "rarity": 0.5,
        "types": ["poison", "normal", "snake"],
        "evolve_poke": "",
        "evolve_lvl": 0,
        "initiative": 4,
        "ico": [{
            "txt": r""" _______
/____ * \
 (   \   \
\______   \ """,
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
        "desc": "pokete.treenator.description",
        "lose_xp": 2,
        "rarity": 1,
        "types": ["plant"],
        "evolve_poke": "",
        "evolve_lvl": 0,
        "initiative": 2,
        "ico": [{
            "txt": r"""    (()
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
        "desc": "pokete.bato.description",
        "lose_xp": 3,
        "rarity": 1.3,
        "types": ["flying", "flying"],
        "evolve_poke": "bator",
        "evolve_lvl": 20,
        "initiative": 6,
        "ico": [{
            "txt": r"""    ___
WW\/* *\/WW
   \v-v/""",
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
        "desc": "pokete.bator.description",
        "lose_xp": 4,
        "rarity": 0.2,
        "types": ["flying", "normal"],
        "evolve_poke": "",
        "evolve_lvl": 0,
        "initiative": 8,
        "ico": [{
            "txt": r"""    ___
WW\/o o\/WW
   |v-v|
   \___/""",
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
        "desc": "pokete.blub.description",
        "lose_xp": 5,
        "rarity": 1,
        "types": ["water", "normal"],
        "evolve_poke": "",
        "evolve_lvl": 0,
        "initiative": 1,
        "ico": [{
            "txt": r"""  _____
 / o   \
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
        "desc": "pokete.owol.description",
        "lose_xp": 2,
        "rarity": 0.5,
        "types": ["flying", "normal", "bird"],
        "evolve_poke": "",
        "evolve_lvl": 0,
        "initiative": 3,
        "night_active": True,
        "ico": [{
            "txt": r"""   ,___,
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
        "desc": "pokete.rato.description",
        "lose_xp": 2,
        "rarity": 1.3,
        "types": ["normal"],
        "evolve_poke": "ratatat",
        "evolve_lvl": 25,
        "initiative": 6,
        "ico": [{
            "txt": r"""   ^---^
   \o o/
   >\./<""",
            "esc": None}]
    },
    "ratatat": {
        "name": "Ratatat",
        "hp": 25,
        "atc": 7,
        "defense": 3,
        "attacks": ["tackle", "tail_wipe", "power_bite"],
        "pool": ["bite"],
        "miss_chance": 0,
        "desc": "pokete.ratatat.description",
        "lose_xp": 2,
        "rarity": 0.7,
        "types": ["normal"],
        "evolve_poke": "",
        "evolve_lvl": 0,
        "initiative": 7,
        "ico": [{
            "txt": r"""   ^---^
   \   /
   >VvV<
    ^^^""",
            "esc": None}, {
            "txt": r"""
    * *""",
            "esc": ["thicc", "green"]}]
    },
    "hornita": {
        "name": "Hornita",
        "hp": 20,
        "atc": 6,
        "defense": 2,
        "attacks": ["tackle", "meat_skewer", "tail_wipe"],
        "pool": [],
        "miss_chance": 0,
        "desc": "pokete.hornita.description",
        "lose_xp": 3,
        "rarity": 1,
        "types": ["normal"],
        "evolve_poke": "",
        "evolve_lvl": 0,
        "initiative": 3,
        "ico": [{
            "txt": r""" \
 =')~
   (¯¯¯¯)~
   //¯¯\\ """,
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
        "desc": "pokete.horny.description",
        "rarity": 1,
        "lose_xp": 2,
        "types": ["normal"],
        "evolve_poke": "hornita",
        "evolve_lvl": 20,
        "initiative": 4,
        "ico": [{
            "txt": r"""  ,
 =')
   (¯¯¯)~
   //¯\\ """,
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
        "desc": "pokete.bushy.description",
        "lose_xp": 1,
        "rarity": 1,
        "types": ["plant", "normal"],
        "evolve_poke": "treenator",
        "evolve_lvl": 20,
        "initiative": 1,
        "ico": [{
            "txt": r"""
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
        "desc": "pokete.wolfior.description",
        "lose_xp": 2,
        "rarity": 1,
        "types": ["fire", "normal"],
        "evolve_poke": "wolfiro",
        "evolve_lvl": 25,
        "initiative": 4,
        "ico": [{
            "txt": r"""   ^---^
   (   )
   >(.)<""",
            "esc": None}, {
            "txt": r"""
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
        "desc": "pokete.wolfiro.description",
        "lose_xp": 4,
        "rarity": 1,
        "types": ["fire", "normal"],
        "evolve_poke": "",
        "evolve_lvl": 0,
        "initiative": 5,
        "ico": [{
            "txt": r"""   \^-^/
   {   }
   >{.}<""",
            "esc": None}, {
            "txt": r"""
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
        "desc": "pokete.rollator.description",
        "lose_xp": 3,
        "rarity": 0.5,
        "types": ["ground", "normal"],
        "evolve_poke": "",
        "evolve_lvl": 0,
        "initiative": 3,
        "ico": [{
            "txt": r"""   _____
  / o o \
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
        "desc": "pokete.clampi.description",
        "lose_xp": 5,
        "rarity": 0.8,
        "types": ["water", "normal"],
        "evolve_poke": "crabbat",
        "evolve_lvl": 20,
        "initiative": 3,
        "ico": [{
            "txt": r"""    ___
  -/   \-
  -\___/-""",
            "esc": None}, {
            "txt": r"""
     *""",
            "esc": ["lightblue"]}]
    },
    "crabbat": {
        "name": "Crabbat",
        "hp": 30,
        "atc": 3,
        "defense": 8,
        "attacks": ["tackle", "bubble_gun", "earch_quake", "shell_pinch"],
        "pool": [],
        "miss_chance": 0,
        "desc": "pokete.crabbat.description",
        "lose_xp": 5,
        "rarity": 0.8,
        "types": ["water", "ground", "normal"],
        "evolve_poke": "rustacean",
        "evolve_lvl": 40,
        "initiative": 4,
        "ico": [{
            "txt": r""" (  ___  )
  \-   -/
   ^   ^""",
            "esc": None}, {
            "txt": r"""
    * *""",
            "esc": ["lightblue"]}]
    },
    "rustacean": {
        "name": "Rustacean",
        "hp": 35,
        "atc": 4,
        "defense": 9,
        "attacks": ["toe_breaker", "bubble_gun", "earch_quake", "shell_pinch"],
        "pool": [],
        "miss_chance": 0,
        "desc": "pokete.rustacean.description",
        "lose_xp": 5,
        "rarity": 0.5,
        "types": ["water", "ground", "normal"],
        "evolve_poke": "",
        "evolve_lvl": 0,
        "initiative": 5,
        "ico": [{
            "txt": r""" {  ^^^  }
  \-   -/
   ^   ^""",
            "esc": None}, {
            "txt": r"""
    * *""",
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
        "desc": "pokete.electrode.description",
        "lose_xp": 3,
        "rarity": 0.8,
        "types": ["electro"],
        "evolve_poke": "",
        "evolve_lvl": 0,
        "initiative": 4,
        "ico": [{
            "txt": r"""
    ( )""",
            "esc": None}, {
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
        "desc": "pokete.cubl.description",
        "lose_xp": 2,
        "rarity": 1.2,
        "types": ["ice", "normal"],
        "evolve_poke": "spikl",
        "evolve_lvl": 30,
        "initiative": 1,
        "ico": [{
            "txt": r"""   -----
   |   |
   -----""",
            "esc": None}, {
            "txt": r"""
    * *""",
            "esc": ["lightblue"]}, {
            "txt": r"""  /     \

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
        "desc": "pokete.spikl.description",
        "lose_xp": 4,
        "rarity": 0.9,
        "types": ["ice", "normal", "water"],
        "evolve_poke": "",
        "evolve_lvl": 0,
        "initiative": 2,
        "ico": [{
            "txt": r"""  -------
  |     |
  -------""",
            "esc": None},
            {
            "txt": r"""
    * *""",
            "esc": ["lightblue"]},
            {
            "txt": r""" /       \

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
        "desc": "pokete.confuso.description",
        "lose_xp": 6,
        "rarity": 0.5,
        "types": ["undead"],
        "evolve_poke": "",
        "evolve_lvl": 0,
        "initiative": 2,
        "ico": [{
            "txt": r"""
     _
    (_) """,
            "esc": None}, {
            "txt": r"""        }
      {
       }""",
            "esc": ["purple"]}, {
            "txt": r"""       }
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
        "desc": "pokete.poisopla.description",
        "lose_xp": 6,
        "rarity": 0.9,
        "types": ["plant", "poison"],
        "evolve_poke": "megapois",
        "evolve_lvl": 20,
        "initiative": 1,
        "ico": [{
            "txt": r"""
       .
 .__ |/|
  \_\||/""",
            "esc": None}, {
            "txt": r"""
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
        "desc": "pokete.megapois.description",
        "lose_xp": 6,
        "rarity": 0.9,
        "types": ["plant", "poison"],
        "evolve_poke": "",
        "evolve_lvl": 0,
        "initiative": 2,
        "ico": [{
            "txt": r"""
    |/.
.__\|/|
 \_\||/ """,
            "esc": None}, {
            "txt": r"""    w w
  w""",
            "esc": ["purple"]},
        ]
    },
    "corcos_day": {
        "name": "Corcos",
        "hp": 15,
        "atc": 2,
        "defense": 5,
        "attacks": ["tackle", "hiding"],
        "pool": [],
        "miss_chance": 0,
        "desc": "pokete.corcos_day.description",
        "lose_xp": 1,
        "rarity": 1,
        "night_active": False,
        "types": ["ground"],
        "evolve_poke": "raupathor_day",
        "evolve_lvl": 20,
        "initiative": 1,
        "ico": [{
            "txt": r"""
    |\
    |'\
    \_|""",
            "esc": None}
        ]
    },
    "corcos_night": {
        "name": "Corcos",
        "hp": 15,
        "atc": 2,
        "defense": 5,
        "attacks": ["tackle", "hiding"],
        "pool": [],
        "miss_chance": 0,
        "desc": "pokete.corcos_night.description",
        "lose_xp": 1,
        "rarity": 1,
        "night_active": True,
        "types": ["ground"],
        "evolve_poke": "raupathor_night",
        "evolve_lvl": 20,
        "initiative": 1,
        "ico": [{
            "txt": r"""
    |\
    |'\
    \_|""",
            "esc": None}
        ]
    },
    "raupathor_day": {
        "name": "Raupathor",
        "hp": 20,
        "atc": 3,
        "defense": 4,
        "attacks": ["tackle", "hiding"],
        "pool": [],
        "miss_chance": 0.1,
        "desc": "pokete.raupathor_day.description",
        "lose_xp": 2,
        "rarity": 1,
        "night_active": False,
        "types": ["ground", "plant"],
        "evolve_poke": "schmetterling",
        "evolve_lvl": 30,
        "initiative": 3,
        "ico": [{
            "txt": r"""
  .__.__.
 ()__)__)}´
  '  '  '
 """,
            "esc": None}
        ]
    },
    "raupathor_night": {
        "name": "Raupathor",
        "hp": 20,
        "atc": 3,
        "defense": 4,
        "attacks": ["tackle", "hiding"],
        "pool": [],
        "miss_chance": 0.1,
        "desc": "pokete.raupathor_night.description",
        "lose_xp": 2,
        "rarity": 1,
        "night_active": True,
        "types": ["ground", "undead"],
        "evolve_poke": "mothor",
        "evolve_lvl": 30,
        "initiative": 3,
        "ico": [{
            "txt": r"""
   __ __
 ()__)__)}´""",
            "esc": None}, {
            "txt": r"""
  .  .  .

  '  '  '""",
    "esc": ["thicc", "blue"]}
        ]
    },
    "schmetterling": {
        "name": "Schmetterling",
        "hp": 20,
        "atc": 5,
        "defense": 2,
        "attacks": ["schmetter", "wing_hit"],
        "pool": [],
        "miss_chance": 0.1,
        "desc": "pokete.schmetterling.description",
        "lose_xp": 3,
        "rarity": 1,
        "night_active": False,
        "types": ["flying"],
        "evolve_poke": "",
        "evolve_lvl": 0,
        "initiative": 4,
        "ico": [{
            "txt": r""" .__ o __.
  \_\|/_/
  /_/'\_\ """,
            "esc": None}
        ]
    },
    "mothor": {
        "name": "Mothor",
        "hp": 20,
        "atc": 6,
        "defense": 2,
        "attacks": ["schmetter", "wing_hit"],
        "pool": [],
        "miss_chance": 0.1,
        "desc": "pokete.mothor.description",
        "lose_xp": 4,
        "rarity": 1,
        "night_active": True,
        "types": ["flying", "undead"],
        "evolve_poke": "",
        "evolve_lvl": 0,
        "initiative": 4,
        "ico": [{
            "txt": r"""  __`o´__
  \_\|/_/
  /_/'\_\ """,
            "esc": None}, {
            "txt": r""" .       .


 ´       `""",
    "esc": ["thicc", "blue"]}
        ]
    },
    "lil_nut": {
        "name": "Lil Nut",
        "hp": 20,
        "atc": 1,
        "defense": 3,
        "attacks": ["tackle", "ground_hit"],
        "pool": ["dick_energy", "hiding"],
        "miss_chance": 0.1,
        "desc": "pokete.lil_nut.description",
        "lose_xp": 2,
        "rarity": 1,
        "types": ["ground", "normal"],
        "evolve_poke": "dicki",
        "evolve_lvl": 35,
        "initiative": 1,
        "ico": [{
            "txt": r"""

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
        "desc": "pokete.dicki.description",
        "lose_xp": 2,
        "rarity": 1,
        "types": ["ground", "normal"],
        "evolve_poke": "dicko",
        "evolve_lvl": 55,
        "initiative": 2,
        "ico": [{
            "txt": r"""
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
        "desc": "pokete.dicko.description",
        "lose_xp": 2,
        "rarity": 1,
        "types": ["ground", "normal"],
        "evolve_poke": "",
        "evolve_lvl": 0,
        "initiative": 3,
        "ico": [{
            "txt": r"""    __
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
        "desc": "pokete.diamondos.description",
        "lose_xp": 2,
        "rarity": 1,
        "types": ["stone"],
        "evolve_poke": "",
        "evolve_lvl": 0,
        "initiative": 2,
        "ico": [{
            "txt": r"""

    o o
     -""",
            "esc": None}, {
            "txt": r"""
    /\ /
       >
   <_""",
            "esc": ["cyan"]}, {
            "txt": r"""
      ^
   <
      _>""",
            "esc": ["white"]}
        ]
    },
}

if __name__ == "__main__":
    print("\033[31;1mDo not execute this!\033[0m")
