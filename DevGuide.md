# Development guide for Pokete
This guide only handles adding new types, attacks and Poketes to Pokete, for further information on class and function syntax see the html documentation or `$ pydoc <file>`.

1. [Adding Poketes](#adding-poketes)
2. [Adding attacks](#adding-attacks)
3. [Adding types](#adding-types)
4. [Adding subtypes](#adding-subtypes)

## Adding Poketes
Every Pokete has an entry the `pokes` dictionary in [`pokete_data/poketes.py`](./pokete_data/poketes.py) every entry needs to have this structure:

```Python
"steini": {  # This is the Poketes simplified name/identifier without spaces and in lowercase, which is used to refer to the Pokete in the game
        "name": "Steini",  # This is the Poketes actual pretty name
        "hp": 25,  # The Poketes max health points
        "atc": 2,  # The Poketes attack points that will added to the Poketes level
        "defense": 4,  # The Poketes defense points that will added to the Poketes level
        "attacks": ["tackle", "politure", "brick_throw"],  # The Poketes starting attacks
        "pool": [],  # List of additional ungeneric attacks the Pokete can learn
        "miss_chance": 0,  # The chance a Pokete will miss an attack, this is added to the attacks individual `miss_chance`
        "desc": "A squared stone that can casually be found on the ground.",  # The Poketes description
        "lose_xp": 3,  # The amount of experience the player gets killing the Pokete
        "rarity": 1,  # Rarity
        "types": ["stone", "normal"],  # The Poketes types
        "evolve_poke": "",  # The name/identifier of the Pokete this Pokete evolves to at a certain level
        "evolve_lvl": 0,  # The level the Pokete evolves at
        "initiative": 5,  # The Poketes initiative points that will added to the Poketes level, and determine what Pokete starts in a fight
        "ico": [{  # A list of dictionaries containing a displayed string and a color, all those strings will be layered over each other and represent the Pokete in the fight
            "txt": """ +-------+
 | o   o |
 |  www  |
 +-------+ """,
            "esc": None}],
    },
```

For more examples on the dictionaries see [`pokete_data/poketes.py`](./pokete_data/poketes.py).

### Types
Only the first type in the `"types"` list is the Poketes actual displayed type, that determines the Poketes effectivity. The other types in the list are just secondary types that determine what generic attacks a Pokete is able to learn. Those can also be subtypes. The main type can't!
For a list of all types and subtypes see [`pokete_data/types.py`](./pokete_data/types.py)

### Learning attacks
In addition the attacks in the `"attacks"` and the `"pool"` lists, a Pokete can learn all generic attacks of the Poketes types.


## Adding attacks
Every attack has an entry the `attacks` dictionary in [`pokete_data/attacks.py `](./pokete_data/attacks.py) every entry needs to have this structure:

```Python
"poison_bite": {  # This is the attacks simplified name/identifier without spaces and in lowercase, which is used to refer to the attack in the game
        "name": "Poison bite",  # The attacks displayed name
        "factor": 1,  # The attack factor, that is used to calculate damage
        "action": "",  # A String that's executed when the attack is used, to effect the Poketes or the enemies values (don't use this) 
        "world_action": "",  # An extra ability the attack can be used for
        "move": ["attack", "downgrade"],  # The moves the Pokete does using the attack
        "miss_chance": 0.3,  # The chance to miss the attack
        "min_lvl": 0,  # The minimal level a Poketes has to have to learn the attack
        "desc": "Makes the enemy weaker.",  # The attacks description
        "types": ["poison"],  # The attacks types
        "effect": "poison",  # The effect the enemy gets when the attack is used, default is None 
        "is_generic": False,  # Whether or not the attack can be learned by any Pokete of its types
        "ap": 10,  # The attack points the attack has, so the amount of times the attack can be used by a Pokete until the Pokete has to be healed
    },
```

For more examples on the dictionaries see [`pokete_data/attacks.py`](./pokete_data/attacks.py).

### Types and learning
Only the first type in the `"types"` list is the attacks real type and determines its effectivity. The other type can only be subtypes. A generic attack can only be learned by a Poketes that has all its types. An ungeneric attack can only be learned if the attack is in the Poketes `"pool"` or `"attacks"` list.

### Effects
The effect given in the `"effect"` attribute has to be the `c_name` of an effect listed in [`pokete_classes/types.py`](./pokete_classes/types.py ) or `None`.

### World action
An attacks `"world_action"` is some kind of extra ability which can be called from the Poketes detail view and be used to, for example make the player fly. The string in `"world_action"` has to be a key in the `abb_funcs` list in [`pokete.py`](./pokete.py).


## Adding types
Every type has an entry the `types` dictionary in [`pokete_data/types.py`](./pokete_data/types.py) every entry needs to have this structure:

```Python
"stone": {  # The types name
        "effective": ["flying", "fire"],  # The types the type is effective against 
        "ineffective": ["plant"],  # The types the type is ineffective against
        "color": ["grey"]  # The types label color
    },
```

## Adding subtypes
Every subtype has an entry the `sub_types` list in [`pokete_data/types.py`](./pokete_data/types.py). They have no further attributes. Subtypes are only useful to determine what Poketes can which generic attack in a type. For example to avoid that `bato` learns the generic `flying` attack `pick`.
