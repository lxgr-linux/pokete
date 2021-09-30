#!/usr/bin/env python3
# This script generates the Pokete wiki
import os
import scrap_engine as se
from pokete_data import *
from pokete_classes.effects import *
import release

def gen_wiki():
    md_str = f"""v{release.VERSION}

# Pokete wiki
This wiki/documentation is a compilation of all Poketes/attacks/types present in the Pokete game.
This wiki can be generated using ```$ ./gen-wiki.py```.

## Table of contents
1. [Poketes](#poketes)
"""

    # Table of contents
    for i, typ in enumerate(sorted(types)):
        md_str += f"""   {i+1}. [{typ.capitalize()} Poketes](#{typ}-poketes)\n"""
        for j, poke in enumerate([k for k in sorted(list(pokes)[1:]) if pokes[k]["types"][0]== typ]):
            md_str += f"""       {j+1}. [{pokes[poke]["name"]}](#{poke.replace("_", "-")})\n"""
    md_str += "2. [Attacks](#attacks)\n"
    for i, typ in enumerate(sorted(types)):
        md_str += f"""   {i+1}. [{typ.capitalize()} attacks](#{typ}-attacks)\n"""
        for j, atc in enumerate([k for k in sorted(attacks) if attacks[k]["type"] == typ]):
            md_str += f"""       {j+1}. [{attacks[atc]["name"]}](#{atc.replace("_", "-")})\n"""
    md_str += """3. [Types](#types)
4. [Items](#items)
"""
    for j, item in enumerate(sorted(items)):
        md_str += f"""   {j+1}. [{items[item]["pretty_name"]}](#{item.replace("_", "-")})\n"""
    md_str += """5. [Effects](#effects)
"""
    for j, effect in enumerate(effects):
        md_str += f"""   {j+1}. [{effect.c_name.capitalize()}](#{effect.c_name.replace("_", "-")})
"""

    # Poketes
    md_str += """
## Poketes
In the following all Poketes with their attributes are displayed.
"""
    for typ in sorted(types):
        md_str += f"### {typ.capitalize()} Poketes"
        for poke in [k for k in sorted(list(pokes)[1:]) if pokes[k]["types"][0] == typ]:
            evolve_txt = f"""- Evolves to [{pokes[pokes[poke]["evolve_poke"]]["name"]}](#{pokes[poke]["evolve_poke"]}) at level {pokes[poke]["evolve_lvl"]}""" if pokes[poke]["evolve_poke"] != "" else "- Does not evolve"
            md_attacks = ""
            for atc in pokes[poke]["attacks"]:
                md_attacks += f"""\n   + [{attacks[atc]["name"]}](#{atc.replace("_", "-")})"""
            # ico
            ico_map = se.Map(4, 11, background=" ")
            for ico in pokes[poke]["ico"]:
                se.Text(ico["txt"], state="float", ignore=" ").add(ico_map, 0, 0)
            ico = "".join(["".join(arr)+"\n" for arr in ico_map.map])
            md_str += f"""
#### {pokes[poke]["name"]}
{pokes[poke]["desc"]}

```
{ico}
```

- Type: [{pokes[poke]["types"][0].capitalize()}](#types)
- Health points: {pokes[poke]["hp"]}
- Attack factor: {pokes[poke]["atc"]}
- Defense factor: {pokes[poke]["defense"]}
- Initiative: {pokes[poke]["initiative"]}
- Missing chance: {pokes[poke]["miss_chance"]}
- Rarity: {pokes[poke]["rarity"]}
- Loosing experience: {pokes[poke]["lose_xp"]}
- Attacks:{md_attacks}
{evolve_txt}
"""

    # Attacks
    md_str += """
## Attacks
Those are all attacks present in the game.
"""
    for typ in sorted(types):
        md_str += f"\n### {typ.capitalize()} attacks"
        for atc in [k for k in attacks if attacks[k]["type"] == typ]:
            md_str += f"""
#### {attacks[atc]["name"]}
{attacks[atc]["desc"]}

- Type: [{attacks[atc]["type"].capitalize()}](#types)
- Minimum Level: {attacks[atc]["min_lvl"]}
- Attack factor: {attacks[atc]["factor"]}
- Missing chance: {attacks[atc]["miss_chance"]}
- Attack points: {attacks[atc]["ap"]}
- Effect: {"None" if attacks[atc]["effect"] is None else f'[{eval(attacks[atc]["effect"]).c_name.capitalize()}](#{eval(attacks[atc]["effect"]).c_name.replace("_", "-")})'}
"""

    # Types
    md_str += """
## Types
Those are all the Pokete/Attack types that are present in the game with all their (in)effectivities against other types.
Type|Effective against|Ineffective against
---|---|---
"""

    for poke_type in types:
        effective, ineffective = ("".join([i.capitalize()+(", " 
                                                        if i != types[poke_type][j][-1] 
                                                        else "")
                                        for i in types[poke_type][j]]) 
                                for j in ["effective", "ineffective"])
        md_str += f"{poke_type.capitalize()}|{effective}|{ineffective}\n"

    # Items
    md_str += """
## Items
Those are all items present in the game, that can be traded or found.
"""

    for item in sorted(items):
        md_str += f"""
### {items[item]["pretty_name"]}
{items[item]["desc"]}

- Price: {items[item]["price"]}
- Can be used in fights: {"Yes" if items[item]["fn"] is not None else "No"}
"""

    # effects
    md_str += """
## Effects
Those effects can be given to a Pokete through an attack.
"""

    md_str += str.join("", [effect.ret_md() for effect in effects])

    # writing to file
    with open("wiki.md", "w+") as file:
        file.write(md_str)


def gen_pics():
    md_str = "# Example pictures\n"
    md_str += str.join("\n\n", [f"![{i}](ss/{i})" for i in sorted(os.listdir("assets/ss"))])

    # writing to file
    with open("assets/pics.md", "w+") as file:
        file.write(md_str)


if __name__ == "__main__":
    print(":: Generating wiki.md...")
    gen_wiki()
    print(":: Generating pics.md...")
    gen_pics()
