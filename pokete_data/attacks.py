attacks = {
    # normal attacks
    "tackle": {
        "name": "attack.tackle.title",
        "factor": 1.5,
        "action": None,
        "world_action": "",
        "move": [
            "attack"
        ],
        "miss_chance": 0.2,
        "min_lvl": 0,
        "desc": "attack.tackle.description",
        "types": [
            "normal"
        ],
        "effect": None,
        "is_generic": True,
        "ap": 30
    },
    "cry": {
        "name": "attack.cry.title",
        "factor": 0,
        "action": "cry",
        "world_action": "",
        "move": [
            "downgrade"
        ],
        "miss_chance": 0,
        "min_lvl": 0,
        "desc": "attack.cry.description",
        "types": [
            "normal"
        ],
        "effect": None,
        "is_generic": False,
        "ap": 10
    },
    "bite": {
        "name": "attack.bite.title",
        "factor": 1.75,
        "action": None,
        "world_action": "",
        "move": [
            "attack"
        ],
        "miss_chance": 0.1,
        "min_lvl": 0,
        "desc": "attack.bite.description",
        "types": [
            "normal"
        ],
        "effect": None,
        "is_generic": False,
        "ap": 30
    },
    "power_bite": {
        "name": "attack.power_bite.title",
        "factor": 8,
        "action": None,
        "world_action": "",
        "move": [
            "attack"
        ],
        "miss_chance": 0.1,
        "min_lvl": 30,
        "desc": "attack.power_bite.description",
        "types": [
            "normal"
        ],
        "effect": None,
        "is_generic": False,
        "ap": 5
    },
    "chocer": {
        "name": "attack.chocer.title",
        "factor": 1,
        "action": "chocer",
        "world_action": "",
        "move": [
            "attack",
            "downgrade"
        ],
        "miss_chance": 0.2,
        "min_lvl": 0,
        "desc": "attack.chocer.description",
        "types": [
            "normal",
            "snake"
        ],
        "effect": "paralyzation",
        "is_generic": True,
        "ap": 15
    },
    "tail_wipe": {
        "name": "attack.tail_wipe.title",
        "factor": 2.5,
        "action": None,
        "world_action": "",
        "move": [
            "attack"
        ],
        "miss_chance": 0.5,
        "min_lvl": 10,
        "desc": "attack.tail_wipe.description",
        "types": [
            "normal"
        ],
        "effect": None,
        "is_generic": False,
        "ap": 10
    },
    "meat_skewer": {
        "name": "attack.meat_skewer.title",
        "factor": 3.5,
        "action": None,
        "world_action": "",
        "move": [
            "attack"
        ],
        "miss_chance": 0.7,
        "min_lvl": 0,
        "desc": "attack.meat_skewer.description",
        "types": [
            "normal"
        ],
        "effect": None,
        "is_generic": False,
        "ap": 10
    },
    "snooze": {
        "name": "attack.snooze.title",
        "factor": 0,
        "action": "snooze",
        "world_action": "",
        "move": [
            "downgrade"
        ],
        "miss_chance": 0.2,
        "min_lvl": 15,
        "desc": "attack.snooze.description",
        "types": [
            "normal"
        ],
        "effect": "sleep",
        "is_generic": False,
        "ap": 15
    },
    "supercow_power": {
        "name": "attack.supercow_power.title",
        "factor": 0,
        "action": "self.atc += 1",
        "world_action": "",
        "move": [
            "shine"
        ],
        "miss_chance": 0,
        "min_lvl": 10,
        "desc": "attack.supercow_power.description",
        "types": [
            "normal"
        ],
        "effect": None,
        "is_generic": False,
        "ap": 10
    },
    # poison attacks
    "poison_bite": {
        "name": "attack.poison_bite.title",
        "factor": 1,
        "action": None,
        "world_action": "",
        "move": [
            "attack",
            "downgrade"
        ],
        "miss_chance": 0.3,
        "min_lvl": 0,
        "desc": "attack.poison_bite.description",
        "types": [
            "poison",
            "snake"
        ],
        "effect": "poison",
        "is_generic": True,
        "ap": 10
    },
    "poison_thorn": {
        "name": "attack.poison_thorn.title",
        "factor": 2.75,
        "action": None,
        "world_action": "",
        "move": [
            "attack",
            "downgrade"
        ],
        "miss_chance": 0.1,
        "min_lvl": 15,
        "desc": "attack.poison_thorn.description",
        "types": [
            "poison"
        ],
        "effect": "poison",
        "is_generic": False,
        "ap": 20
    },
    # stone attacks
    "pepple_fire": {
        "name": "attack.pepple_fire.title",
        "factor": 1,
        "action": "cry",
        "world_action": "",
        "move": [
            "attack",
            "downgrade"
        ],
        "miss_chance": 0,
        "min_lvl": 0,
        "desc": "attack.pepple_fire.description",
        "types": [
            "stone"
        ],
        "effect": None,
        "is_generic": True,
        "ap": 5
    },
    "sand_throw": {
        "name": "attack.sand_throw.title",
        "factor": 1,
        "action": "cry",
        "world_action": "",
        "move": [
            "attack",
            "downgrade"
        ],
        "miss_chance": 0,
        "min_lvl": 0,
        "desc": "attack.sand_throw.description",
        "types": [
            "stone"
        ],
        "effect": None,
        "is_generic": False,
        "ap": 5
    },
    "politure": {
        "name": "attack.politure.title",
        "factor": 0,
        "action": "politure",
        "world_action": "",
        "move": [
            "shine"
        ],
        "miss_chance": 0,
        "min_lvl": 0,
        "desc": "attack.politure.description",
        "types": [
            "stone"
        ],
        "effect": None,
        "is_generic": True,
        "ap": 15
    },
    "brick_throw": {
        "name": "attack.brick_throw.title",
        "factor": 2,
        "action": None,
        "world_action": "",
        "move": [
            "throw"
        ],
        "miss_chance": 0.3,
        "min_lvl": 15,
        "desc": "attack.brick_throw.description",
        "types": [
            "stone"
        ],
        "effect": None,
        "is_generic": True,
        "ap": 20
    },
    "rock_smash": {
        "name": "attack.rock_smash.title",
        "factor": 5,
        "action": None,
        "world_action": "",
        "move": [
            "pound"
        ],
        "miss_chance": 0.1,
        "min_lvl": 15,
        "desc": "attack.rock_smash.description",
        "types": [
            "stone"
        ],
        "effect": None,
        "is_generic": True,
        "ap": 5
    },
    "dia_stab": {
        "name": "attack.dia_stab.title",
        "factor": 5,
        "action": None,
        "world_action": "",
        "move": [
            "attack"
        ],
        "miss_chance": 0.1,
        "min_lvl": 15,
        "desc": "attack.dia_stab.description",
        "types": [
            "stone"
        ],
        "effect": None,
        "is_generic": False,
        "ap": 5
    },
    "dazzle": {
        "name": "attack.dazzle.title",
        "factor": 1.5,
        "action": None,
        "world_action": "",
        "move": [
            "attack",
            "downgrade"
        ],
        "miss_chance": 0.2,
        "min_lvl": 10,
        "desc": "attack.dazzle.description",
        "types": [
            "stone"
        ],
        "effect": "paralyzation",
        "is_generic": False,
        "ap": 20
    },
    "dia_spikes": {
        "name": "attack.dia_spikes.title",
        "factor": 2,
        "action": None,
        "world_action": "",
        "move": [
            "attack"
        ],
        "miss_chance": 0,
        "min_lvl": 20,
        "desc": "attack.dia_spikes.description",
        "types": [
            "stone"
        ],
        "effect": None,
        "is_generic": False,
        "ap": 20
    },
    # ground attacks
    "earch_quake": {
        "name": "attack.earch_quake.title",
        "factor": 4,
        "action": None,
        "world_action": "",
        "move": [
            "pound"
        ],
        "miss_chance": 0,
        "min_lvl": 0,
        "desc": "attack.earch_quake.description",
        "types": [
            "ground"
        ],
        "effect": None,
        "is_generic": True,
        "ap": 10
    },
    "power_roll": {
        "name": "attack.power_roll.title",
        "factor": 2.5,
        "action": None,
        "world_action": "",
        "move": [
            "attack"
        ],
        "miss_chance": 0.2,
        "min_lvl": 0,
        "desc": "attack.power_roll.description",
        "types": [
            "ground"
        ],
        "effect": None,
        "is_generic": True,
        "ap": 15
    },
    "toe_breaker": {
        "name": "attack.toe_breaker.title",
        "factor": 2.5,
        "action": None,
        "world_action": "",
        "move": [
            "attack"
        ],
        "miss_chance": 0.3,
        "min_lvl": 0,
        "desc": "attack.toe_breaker.description",
        "types": [
            "ground"
        ],
        "effect": None,
        "is_generic": True,
        "ap": 20
    },
    "ground_hit": {
        "name": "attack.ground_hit.title",
        "factor": 3,
        "action": None,
        "world_action": "",
        "move": [
            "attack"
        ],
        "miss_chance": 0.1,
        "min_lvl": 0,
        "desc": "attack.ground_hit.description",
        "types": [
            "ground"
        ],
        "effect": None,
        "is_generic": True,
        "ap": 10
    },
    "dick_energy": {
        "name": "attack.dick_energy.title",
        "factor": 0,
        "action": "dick_energy",
        "world_action": "",
        "move": [
            "shine"
        ],
        "miss_chance": 0,
        "min_lvl": 0,
        "desc": "attack.dick_energy.description",
        "types": [
            "ground"
        ],
        "effect": None,
        "is_generic": False,
        "ap": 15
    },
    "hiding": {
        "name": "attack.hiding.title",
        "factor": 0,
        "action": "hiding",
        "world_action": "",
        "move": [
            "shine"
        ],
        "miss_chance": 0,
        "min_lvl": 20,
        "desc": "attack.hiding.description",
        "types": [
            "ground"
        ],
        "effect": None,
        "is_generic": False,
        "ap": 15
    },
    # Fire attacks
    "fire_bite": {
        "name": "attack.fire_bite.title",
        "factor": 2,
        "action": None,
        "world_action": "",
        "move": [
            "attack"
        ],
        "miss_chance": 0.2,
        "min_lvl": 0,
        "desc": "attack.fire_bite.description",
        "types": [
            "fire"
        ],
        "effect": "burning",
        "is_generic": True,
        "ap": 15
    },
    "ash_throw": {
        "name": "attack.ash_throw.title",
        "factor": 0.5,
        "action": "cry",
        "world_action": "",
        "move": [
            "attack",
            "downgrade"
        ],
        "miss_chance": 0,
        "min_lvl": 15,
        "desc": "attack.ash_throw.description",
        "types": [
            "fire"
        ],
        "effect": None,
        "is_generic": True,
        "ap": 15
    },
    "flame_throw": {
        "name": "attack.flame_throw.title",
        "factor": 2.5,
        "action": None,
        "world_action": "",
        "move": [
            "attack"
        ],
        "miss_chance": 0.3,
        "min_lvl": 15,
        "desc": "attack.flame_throw.description",
        "types": [
            "fire"
        ],
        "effect": "burning",
        "is_generic": True,
        "ap": 10
    },
    "fire_ball": {
        "name": "attack.fire_ball.title",
        "factor": 4,
        "action": None,
        "world_action": "",
        "move": [
            "fireball"
        ],
        "miss_chance": 0,
        "min_lvl": 25,
        "desc": "attack.fire_ball.description",
        "types": [
            "fire"
        ],
        "effect": None,
        "is_generic": True,
        "ap": 10
    },
    # flying attacks
    "flying": {
        "name": "attack.flying.title",
        "factor": 1.5,
        "action": None,
        "world_action": "teleport",
        "move": [
            "attack"
        ],
        "miss_chance": 0.1,
        "min_lvl": 0,
        "desc": "attack.flying.description",
        "types": [
            "flying"
        ],
        "effect": None,
        "is_generic": False,
        "ap": 30
    },
    "pick": {
        "name": "attack.pick.title",
        "factor": 1.7,
        "action": None,
        "world_action": "",
        "move": [
            "attack"
        ],
        "miss_chance": 0.1,
        "min_lvl": 0,
        "desc": "attack.pick.description",
        "types": [
            "flying",
            "bird"
        ],
        "effect": None,
        "is_generic": True,
        "ap": 30
    },
    "wind_blow": {
        "name": "attack.wind_blow.title",
        "factor": 2,
        "action": None,
        "world_action": "",
        "move": [
            "attack"
        ],
        "miss_chance": 0,
        "min_lvl": 0,
        "desc": "attack.wind_blow.description",
        "types": [
            "flying"
        ],
        "effect": None,
        "is_generic": True,
        "ap": 20
    },
    "storm_gust": {
        "name": "attack.storm_gust.title",
        "factor": 6,
        "action": None,
        "world_action": "",
        "move": [
            "attack"
        ],
        "miss_chance": 0,
        "min_lvl": 0,
        "desc": "attack.storm_gust.description",
        "types": [
            "flying"
        ],
        "effect": None,
        "is_generic": True,
        "ap": 10
    },
    "schmetter": {
        "name": "attack.schmetter.title",
        "factor": 1.7,
        "action": None,
        "world_action": "",
        "move": [
            "attack"
        ],
        "miss_chance": 0.1,
        "min_lvl": 0,
        "desc": "attack.schmetter.description",
        "types": [
            "flying"
        ],
        "effect": None,
        "is_generic": False,
        "ap": 30
    },
    "eye_pick": {
        "name": "attack.eye_pick.title",
        "factor": 2.5,
        "action": "eye_pick",
        "world_action": "",
        "move": [
            "attack",
            "downgrade"
        ],
        "miss_chance": 0.6,
        "min_lvl": 0,
        "desc": "attack.eye_pick.description",
        "types": [
            "flying",
            "bird"
        ],
        "effect": None,
        "is_generic": True,
        "ap": 10
    },
    "wing_hit": {
        "name": "attack.wing_hit.title",
        "factor": 2.5,
        "action": None,
        "world_action": "",
        "move": [
            "attack"
        ],
        "miss_chance": 0.5,
        "min_lvl": 0,
        "desc": "attack.wing_hit.description",
        "types": [
            "flying"
        ],
        "effect": None,
        "is_generic": True,
        "ap": 10
    },
    "brooding": {
        "name": "attack.brooding.title",
        "factor": 0,
        "action": "brooding",
        "world_action": "",
        "move": [
            "shine"
        ],
        "miss_chance": 0,
        "min_lvl": 15,
        "desc": "attack.brooding.description",
        "types": [
            "flying",
            "bird"
        ],
        "effect": None,
        "is_generic": True,
        "ap": 10
    },
    "power_pick": {
        "name": "attack.power_pick.title",
        "factor": 2,
        "action": None,
        "world_action": "",
        "move": [
            "attack"
        ],
        "miss_chance": 0.4,
        "min_lvl": 0,
        "desc": "attack.power_pick.description",
        "types": [
            "flying",
            "bird"
        ],
        "effect": None,
        "is_generic": True,
        "ap": 10
    },
    # water attacks
    "bubble_gun": {
        "name": "attack.bubble_gun.title",
        "factor": 2,
        "action": None,
        "world_action": "",
        "move": [
            "gun"
        ],
        "miss_chance": 0.2,
        "min_lvl": 0,
        "desc": "attack.bubble_gun.description",
        "types": [
            "water"
        ],
        "effect": None,
        "is_generic": True,
        "ap": 20
    },
    "bubble_bomb": {
        "name": "attack.bubble_bomb.title",
        "factor": 6,
        "action": "cry",
        "world_action": "",
        "move": [
            "bomb",
            "downgrade"
        ],
        "miss_chance": 0,
        "min_lvl": 0,
        "desc": "attack.bubble_bomb.description",
        "types": [
            "water"
        ],
        "effect": None,
        "is_generic": True,
        "ap": 10
    },
    "bubble_shield": {
        "name": "attack.bubble_shield.title",
        "factor": 0,
        "action": "hiding",
        "world_action": "",
        "move": [
            "shine"
        ],
        "miss_chance": 0,
        "min_lvl": 0,
        "desc": "attack.bubble_shield.description",
        "types": [
            "water"
        ],
        "effect": None,
        "is_generic": True,
        "ap": 10
    },
    "wet_slap": {
        "name": "attack.wet_slap.title",
        "factor": 2.5,
        "action": None,
        "world_action": "",
        "move": [
            "attack"
        ],
        "miss_chance": 0.1,
        "min_lvl": 10,
        "desc": "attack.wet_slap.description",
        "types": [
            "water"
        ],
        "effect": None,
        "is_generic": True,
        "ap": 15
    },
    "shell_pinch": {
        "name": "attack.shell_pinch.title",
        "factor": 2.5,
        "action": None,
        "world_action": "",
        "move": [
            "attack"
        ],
        "miss_chance": 0.1,
        "min_lvl": 15,
        "desc": "attack.shell_pinch.description",
        "types": [
            "water"
        ],
        "effect": None,
        "is_generic": False,
        "ap": 20
    },
    # undead attacks
    "heart_touch": {
        "name": "attack.heart_touch.title",
        "factor": 4,
        "action": "heart_touch",
        "world_action": "",
        "move": [
            "attack",
            "downgrade"
        ],
        "miss_chance": 0,
        "min_lvl": 20,
        "desc": "attack.heart_touch.description",
        "types": [
            "undead"
        ],
        "effect": None,
        "is_generic": True,
        "ap": 10
    },
    "confusion": {
        "name": "attack.confusion.title",
        "factor": 0,
        "action": None,
        "world_action": "",
        "move": [
            "downgrade"
        ],
        "miss_chance": 0.2,
        "min_lvl": 0,
        "desc": "attack.confusion.description",
        "types": [
            "undead"
        ],
        "effect": "confusion",
        "is_generic": True,
        "ap": 40
    },
    "mind_blow": {
        "name": "attack.mind_blow.title",
        "factor": 0,
        "action": None,
        "world_action": "",
        "move": [
            "downgrade"
        ],
        "miss_chance": 0.2,
        "min_lvl": 0,
        "desc": "attack.mind_blow.description",
        "types": [
            "undead"
        ],
        "effect": "confusion",
        "is_generic": True,
        "ap": 15
    },
    # electro attacks
    "shock": {
        "name": "attack.shock.title",
        "factor": 1.5,
        "action": None,
        "world_action": "",
        "move": [
            "arch"
        ],
        "miss_chance": 0.2,
        "min_lvl": 0,
        "desc": "attack.shock.description",
        "types": [
            "electro"
        ],
        "effect": None,
        "is_generic": True,
        "ap": 30
    },
    "charging": {
        "name": "attack.charging.title",
        "factor": 0,
        "action": "dick_energy",
        "world_action": "",
        "move": [
            "shine"
        ],
        "miss_chance": 0,
        "min_lvl": 10,
        "desc": "attack.charging.description",
        "types": [
            "electro"
        ],
        "effect": None,
        "is_generic": True,
        "ap": 15
    },
    "mega_arch": {
        "name": "attack.mega_arch.title",
        "factor": 5,
        "action": None,
        "world_action": "",
        "move": [
            "arch"
        ],
        "miss_chance": 0.2,
        "min_lvl": 15,
        "desc": "attack.mega_arch.description",
        "types": [
            "electro"
        ],
        "effect": "paralyzation",
        "is_generic": True,
        "ap": 10
    },
    # plant attacks
    "special_smell": {
        "name": "attack.special_smell.title",
        "factor": 0,
        "action": None,
        "world_action": "",
        "move": [
            "downgrade"
        ],
        "miss_chance": 0.1,
        "min_lvl": 0,
        "desc": "attack.special_smell.description",
        "types": [
            "plant"
        ],
        "effect": "confusion",
        "is_generic": False,
        "ap": 10
    },
    "apple_drop": {
        "name": "attack.apple_drop.title",
        "factor": 1.7,
        "action": None,
        "world_action": "",
        "move": [
            "attack"
        ],
        "miss_chance": 0.3,
        "min_lvl": 0,
        "desc": "attack.apple_drop.description",
        "types": [
            "plant"
        ],
        "effect": None,
        "is_generic": False,
        "ap": 30
    },
    "super_sucker": {
        "name": "attack.super_sucker.title",
        "factor": 0,
        "action": "super_sucker",
        "world_action": "",
        "move": [
            "downgrade",
            "shine"
        ],
        "miss_chance": 0,
        "min_lvl": 0,
        "desc": "attack.super_sucker.description",
        "types": [
            "plant"
        ],
        "effect": None,
        "is_generic": False,
        "ap": 10
    },
    "sucker": {
        "name": "attack.sucker.title",
        "factor": 0,
        "action": "sucker",
        "world_action": "",
        "move": [
            "downgrade",
            "shine"
        ],
        "miss_chance": 0,
        "min_lvl": 0,
        "desc": "attack.sucker.description",
        "types": [
            "plant"
        ],
        "effect": None,
        "is_generic": False,
        "ap": 20
    },
    "root_strangler": {
        "name": "attack.root_strangler.title",
        "factor": 1,
        "action": None,
        "world_action": "",
        "move": [
            "attack",
            "downgrade"
        ],
        "miss_chance": 0.2,
        "min_lvl": 20,
        "desc": "attack.root_strangler.description",
        "types": [
            "plant"
        ],
        "effect": "paralyzation",
        "is_generic": True,
        "ap": 15
    },
    "root_slap": {
        "name": "attack.root_slap.title",
        "factor": 1.5,
        "action": None,
        "world_action": "",
        "move": [
            "attack"
        ],
        "miss_chance": 0.2,
        "min_lvl": 0,
        "desc": "attack.root_slap.description",
        "types": [
            "plant"
        ],
        "effect": None,
        "is_generic": True,
        "ap": 30
    },
    "the_old_roots_hit": {
        "name": "attack.the_old_roots_hit.title",
        "factor": 50,
        "action": None,
        "world_action": "",
        "move": [
            "shine",
            "shine",
            "attack"
        ],
        "miss_chance": 0,
        "min_lvl": 0,
        "desc": "attack.the_old_roots_hit.description",
        "types": [
            "plant"
        ],
        "effect": None,
        "is_generic": False,
        "ap": 1
    },
    "leaf_storm": {
        "name": "attack.leaf_storm.title",
        "factor": 5,
        "action": None,
        "world_action": "",
        "move": [
            "attack"
        ],
        "miss_chance": 0,
        "min_lvl": 20,
        "desc": "attack.leaf_storm.description",
        "types": [
            "plant"
        ],
        "effect": None,
        "is_generic": True,
        "ap": 10
    },
    "bark_hardening": {
        "name": "attack.bark_hardening.title",
        "factor": 0,
        "action": "bark_hardening",
        "world_action": "",
        "move": [
            "shine"
        ],
        "miss_chance": 0,
        "min_lvl": 0,
        "desc": "attack.bark_hardening.description",
        "types": [
            "plant"
        ],
        "effect": None,
        "is_generic": True,
        "ap": 15
    },
    "poison_spores": {
        "name": "attack.poison_spores.title",
        "factor": 0,
        "action": None,
        "world_action": "",
        "move": [
            "downgrade"
        ],
        "miss_chance": 0,
        "min_lvl": 0,
        "desc": "attack.poison_spores.description",
        "types": [
            "plant"
        ],
        "effect": "poison",
        "is_generic": False,
        "ap": 15
    },
    "branch_stab": {
        "name": "attack.branch_stab.title",
        "factor": 4,
        "action": "cry",
        "world_action": "",
        "move": [
            "attack",
            "downgrade"
        ],
        "miss_chance": 0.2,
        "min_lvl": 15,
        "desc": "attack.branch_stab.description",
        "types": [
            "plant"
        ],
        "effect": None,
        "is_generic": True,
        "ap": 10
    },
    # ice attacks
    "freeze": {
        "name": "attack.freeze.title",
        "factor": 0,
        "action": None,
        "world_action": "",
        "move": [
            "downgrade"
        ],
        "miss_chance": 0.1,
        "min_lvl": 10,
        "desc": "attack.freeze.description",
        "types": [
            "ice"
        ],
        "effect": "freezing",
        "is_generic": True,
        "ap": 10
    },
    "snow_storm": {
        "name": "attack.snow_storm.title",
        "factor": 2.5,
        "action": None,
        "world_action": "",
        "move": [
            "attack"
        ],
        "miss_chance": 0,
        "min_lvl": 0,
        "desc": "attack.snow_storm.description",
        "types": [
            "ice"
        ],
        "effect": None,
        "is_generic": True,
        "ap": 20
    },
    "sword_of_ice": {
        "name": "attack.sword_of_ice.title",
        "factor": 5,
        "action": None,
        "world_action": "",
        "move": [
            "attack"
        ],
        "miss_chance": 0.3,
        "min_lvl": 20,
        "desc": "attack.sword_of_ice.description",
        "types": [
            "ice"
        ],
        "effect": None,
        "is_generic": True,
        "ap": 10
    },
    "spikes": {
        "name": "attack.spikes.title",
        "factor": 1.75,
        "action": None,
        "world_action": "",
        "move": [
            "attack"
        ],
        "miss_chance": 0,
        "min_lvl": 0,
        "desc": "attack.spikes.description",
        "types": [
            "ice"
        ],
        "effect": None,
        "is_generic": True,
        "ap": 30
    }
}

if __name__ == "__main__":
    print("\033[31;1mDo not execute this!\033[0m")
