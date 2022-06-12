#!/usr/bin/env python3
"""This script generates the Pokete wiki"""
import os
from os.path import exists, isdir
import sys
import scrap_engine as se
import release
from pokete_classes.effects import effects, effect_list
from pokete_data import pokes, attacks, types, items, maps

SILENT = False
QUIET = False
VERBOSE = True


class Wiki:
    """The class in which wiki generation behaviour is defined"""

    @staticmethod
    def start() -> str:
        """The start and title of the wiki

        Returns
        ---
        The title of the wiki page.
        """
        return f"""v{release.VERSION}

# Pokete wiki
This wiki/documentation is a compilation of all Poketes/attacks/types present in the Pokete game.
This wiki can be generated using ```$ ./gen_wiki.py```.

Use ```$./gen_wiki.py help``` to get more information about different wikis.

You can find different versions of this wiki:

- A single-page version can be found [here](wiki.md)
- A multi-page version can be found [here](https://lxgr-linux.github.io/pokete/wiki-multi/)

"""

    @staticmethod
    def overview(multi_page: bool = False) -> str:
        """A short overview of what the wiki contains.

        Arguments
        ---------
        - multi_page (boolean): if the item info should be made for a multi-page wiki or not.

        Returns
        -------
        An overview for a multi-page wiki.
        """
        return "Table of contents\n" + \
"\n".join(f"{i+1}. [{name.capitalize()}]({'' if multi_page else '#'}{name})"
          for i, name in enumerate(["poketes", "attacks", "types", "item",
                                    "effects"])) + "\n"

    @staticmethod
    def get_name(poke):
        """Returns the name of a Pokete to display in headings"""
        additional = ""
        if "_night" in poke:
            additional = " night"
        elif "_day" in poke:
            additional = " day"
        return pokes[poke]['name'] + additional

    @staticmethod
    def table_of_contents(multi_page: bool = False) -> str:
        """The table of contents of the pokete wiki

        Arguments
        ---------
        - multi_page (boolean): if the item info should be made for a multi-page wiki or not.

        Returns
        -------
        A Table of contents for a single page wiki.
        """
        out = ''

        # Table of contents
        if not multi_page:
            out += """## Table of contents
1. [Poketes](#poketes)
"""
            for i, typ in enumerate(sorted(types)):
                out += f"""   {i + 1}. [{typ.capitalize()} Poketes](#{typ}-poketes)\n"""
                for j, poke in enumerate([k for k in sorted(list(pokes)[1:]) if
                                          pokes[k]["types"][0] == typ]):
                    out += f"""       {j + 1}. [{Wiki.get_name(poke)}](#{poke.replace("_", "-")})\n"""
            out += "2. [Attacks](#attacks)\n"
            for i, typ in enumerate(sorted(types)):
                out += f"""   {i + 1}. [{typ.capitalize()} attacks](#{typ}-attacks)\n"""
                for j, atc in enumerate([k for k in sorted(attacks) if
                                         attacks[k]["types"][0] == typ]):
                    out += f"""       {j + 1}. [{attacks[atc]["name"]}](#{attacks[atc]["name"]
                            .replace(" ", "-").lower()})\n"""
            out += """3. [Types](#types)
4. [Items](#items)
"""
            for j, item in enumerate(sorted(items)):
                out += f"""   {j + 1}. [{items[item]["pretty_name"]}](#{item.replace("_", "-")})\n"""
            out += """5. [Effects](#effects)
"""
            for j, effect in enumerate(effect_list):
                out += f"""   {j + 1}. [{effect.c_name.capitalize()}](#{effect.c_name.replace("_", "-")})
"""

        else:
            out += """## Table of contents
1. [Poketes](./poketes)
"""
            for i, typ in enumerate(sorted(types)):
                out += f"""   {i + 1}. [{typ.capitalize()} Poketes](./poketes/{typ})\n"""
                for j, poke in enumerate([k for k in sorted(list(pokes)[1:]) if
                                          pokes[k]["types"][0] == typ]):
                    out += f"""       {j + 1}. [{Wiki.get_name(poke)}](./poketes/{typ}#{poke.replace("_", "-")})\n"""
            out += "2. [Attacks](./attacks)\n"
            for i, typ in enumerate(sorted(types)):
                out += f"""   {i + 1}. [{typ.capitalize()} attacks](./attacks/{typ})\n"""
                for j, atc in enumerate([k for k in sorted(attacks) if
                                         attacks[k]["types"][0] == typ]):
                    out += f"""       {j + 1}. [{attacks[atc]["name"]}](./attack/{typ}#{atc.replace("_", "-")})\n"""
            out += """3. [Types](./types)
4. [Items](./items)
"""
            for j, item in enumerate(sorted(items)):
                out += f"""   {j + 1}. [{items[item]["pretty_name"]}](./items#{item.replace("_", "-")})\n"""
            out += """5. [Effects](./effects)
"""
            for j, effect in enumerate(effect_list):
                out += f"""   {j + 1}. [{effect.c_name.capitalize()}](./effects#{effect.c_name.replace("_", "-")})
"""
        return out

    @staticmethod
    def poketes(page_mode='single', pokete_type=None) -> str:
        """The function to add all poketes and their attributes to the wiki.

        Arguments:
        ----------
        - page_mode (string): Defines for what the output will be used. Can be:
            - single: all poketes listed by their types with single-page links
            - index: Just the index of all pokete types with multi-page links
            - multi: Information about the pokete type definied in pokete_type
              with multi-page links.
        - pokete_type: Only necessary if page_mode is set to 'index': Then
          defines the pokete type to get the information and links of.

        Returns
        -------
        All poketes and their attributes as a markdown string.
        """
        if page_mode == 'single':
            out = """
## Poketes
In the following all Poketes with their attributes are displayed.

"""
            for typ in sorted(types):
                out += f"### {typ.capitalize()} Poketes"
                for poke in [k for k in sorted(list(pokes)[1:]) if
                             pokes[k]["types"][0] == typ]:
                    if VERBOSE:
                        print(f' -> Adding {pokes[poke]["name"]}')
                    out += Wiki.poke_info(poke)
            return out
        elif page_mode == 'index':
            out = """# Poketes
In the following all Poketes with their attributes are displayed.

"""
            for typ in sorted(types):
                out += f"- [{typ.capitalize()} Poketes](./{typ})\n"
            out += "\n---\n\n## All poketes sorted by their type:\n"
            for typ in sorted(types):
                out += f"- [{typ.capitalize()} Poketes](./{typ})\n"
                for poke in [k for k in sorted(list(pokes)[1:]) if
                             pokes[k]["types"][0] == typ]:
                    out += f"""  - [{pokes[poke]["name"].capitalize()}](./{typ}#{poke})\n"""
            return out
        elif page_mode == 'multi':
            if pokete_type is not None:
                out = f"# {pokete_type.capitalize()} Poketes"
                for poke in [k for k in sorted(list(pokes)[1:]) if
                             pokes[k]["types"][0] == pokete_type]:
                    if poke == sorted(list(pokes)[1:])[-1]:
                        if VERBOSE:
                            print(f'  `-> Adding {pokes[poke]["name"]}')
                    else:
                        if VERBOSE:
                            print(f'  |-> Adding {pokes[poke]["name"]}')
                    out += Wiki.poke_info(poke=poke, multi_page=True)
                return out
            raise AttributeError(
                "Pokete_type can not be none, if mode 'multi' is selected.")
        raise AttributeError("Please select a valid page mode of: 'single',"
                             "'index' or 'multi'!")

    @staticmethod
    def poke_info(poke: str, multi_page: bool = False) -> str:
        """Generates information about a specific pokete

        Arguments:
        ---------
        - poke (string): The pokete to get the information of.
        - multi_page (boolean): if the item info should be made for a multi-page
          wiki or not.

        Returns
        -------
        A markdown string of all the attributes and information of the pokete.
        """
        if (evolve_pokete := pokes[poke]["evolve_poke"]) == "":
            evolve_txt = "- Does not evolve\n"
        else:
            evolve_txt = f"""- Evolves to [{Wiki.get_name(evolve_pokete)}]({f'./{pokes[evolve_pokete]["types"][0]}'
            if multi_page else ""}#{evolve_pokete}) at level {pokes[poke]['evolve_lvl']}"""

        md_attacks = "\n   + " + "\n   + ".join(f"""[{attacks[atc]["name"]}]({
                            f'../attacks/{attacks[atc]["types"][0].capitalize()}'
                                if multi_page else ""
                            }#{atc.replace("_", "-")})"""
                        for atc in pokes[poke]["attacks"])
        # ico
        ico_map = se.Map(4, 11, background=" ")
        for ico in pokes[poke]["ico"]:
            se.Text(ico["txt"], state="float", ignore=" ").add(ico_map, 0, 0)
        ico = "".join("".join(arr) + "\n" for arr in ico_map.map)

        active = {
            True: "Night",
            False: "Day",
            None: "Always",
        }[pokes[poke].get("night_active")]

        md_locations = "\n   + ".join(maps[i]["pretty_name"] for i in maps
                                if maps[i]["poke_args"] is not None
                                and poke in maps[i]["poke_args"]["pokes"]
                                or "w_poke_args" in maps[i]
                                and poke in maps[i]["w_poke_args"]["pokes"])

        return f"""
##{'' if multi_page else '##'} {Wiki.get_name(poke)}
{pokes[poke]["desc"]}

```
{ico}
```

- Type: [{pokes[poke]["types"][0].capitalize()}]({'../types' if multi_page
        else '#types'})
- Health points: {pokes[poke]["hp"]}
- Attack factor: {pokes[poke]["atc"]}
- Defense factor: {pokes[poke]["defense"]}
- Initiative: {pokes[poke]["initiative"]}
- Missing chance: {pokes[poke]["miss_chance"]}
- Rarity: {pokes[poke]["rarity"]}
- Loosing experience: {pokes[poke]["lose_xp"]}
- Attacks:{md_attacks}
- Active: {active}
- Can be found in:
   + {md_locations if md_locations != "" else "Nowhere"}
{evolve_txt}
"""

    @staticmethod
    def attacks(multi_page: bool = False) -> str or list:
        """The function to all attacks to the wiki.

        Arguments
        ---------
        - multi_page (boolean): if the item info should be made for a multi-page
          wiki or not.

        Returns
        -------
        A markdown string of all attacks with their attributes and informations.
        """
        if multi_page:
            index = """# Attacks
Those are all attacks present in the game.
"""
            pages = []
            for typ in sorted(types):
                if VERBOSE:
                    print(f" -> Adding {typ}")
                index += f"\n- [{typ.capitalize()}](./{typ})"
                page = f"# {typ.capitalize()} attacks"
                for atc in [k for k in attacks if
                            attacks[k]["types"][0] == typ]:
                    if multi_page:
                        if atc == [k for k in attacks if
                                   attacks[k]["types"][0] == typ][-1]:
                            if VERBOSE:
                                print(f'  `-> Adding {attacks[atc]["name"]}')
                        else:
                            if VERBOSE:
                                print(f'  |-> Adding {attacks[atc]["name"]}')
                    else:
                        if VERBOSE:
                            print(f' -> Adding {attacks[atc]["name"]}')
                    page += Wiki.attack_info(atc, True)
                pages.append((f"{typ}.md", page))
            index += "\n\n---\n\n## All attacks sorted by their type:\n"
            for typ in sorted(types):
                index += f"- [{typ.capitalize()} Attacks](./{typ})\n"
                for atc in [k for k in attacks if
                            attacks[k]["types"][0] == typ]:
                    index += f"""  - [{attacks[atc]["name"].capitalize()}](./{typ}#{atc.replace('_', '-')})\n"""

            index += '\n'
            pages.insert(0, ("index.md", index))
            return pages
        out = """
## Attacks
Those are all attacks present in the game.
"""
        for typ in sorted(types):
            out += f"\n### {typ.capitalize()} attacks"
            for atc in [k for k in attacks if
                        attacks[k]["types"][0] == typ]:
                if atc == \
                    [k for k in attacks if attacks[k]["types"][0] == typ][
                        -1]:
                    if VERBOSE:
                        print(f' `-> Adding {attacks[atc]["name"]}')
                else:
                    if VERBOSE:
                        print(f' |-> Adding {attacks[atc]["name"]}')
                out += Wiki.attack_info(atc)

        return out

    @staticmethod
    def attack_info(attack: str, multi_page: bool = False) -> str:
        """The function to collect information and attributes of a specific
        attack

        Arguments
        ---------
        - attacks (string): The attack to collect the information of.
        - multi_page (boolean): if the item info should be made for a multi-page
          wiki or not.

        Returns
        -------
        A markdown string with the information about the attack.
        """
        eff = None if attacks[attack]["effect"] is None \
            else getattr(effects, attacks[attack]["effect"])
        return f"""\n##{"" if multi_page else "##"} {attacks[attack]["name"]}
{attacks[attack]["desc"]}

- Type: [{attacks[attack]["types"][0].capitalize()}]({"../types" if multi_page
                                                                 else "#types"})
- Minimum Level: {attacks[attack]["min_lvl"]}
- Attack factor: {attacks[attack]["factor"]}
- Missing chance: {attacks[attack]["miss_chance"]}
- Attack points: {attacks[attack]["ap"]}
- Effect: {"None" if eff is None else f'[{eff.c_name.capitalize()}]({"../effects" if multi_page else ""}#{eff.c_name.replace("_", "-")})'}
"""

    @staticmethod
    def types(multi_page: bool = False) -> str:
        """The function to add all types to the wiki.

        Arguments
        ---------
        - multi_page (boolean): if the item info should be made for a multi-page
          wiki or not.

        Returns
        -------
        A markdown string of all available types.
        """
        out = f"""
#{'' if multi_page else '#'} Types
Those are all the Pokete/Attack types that are present in the game with all their (in)effectivities against other types.

|Type|Effective against|Ineffective against|
|---|---|---|
"""

        for poke_type in types:
            effective, ineffective = ("".join([i.capitalize() + (", "
                                                                 if i != types[poke_type][j][-1]
                                                                 else "")
                                               for i in types[poke_type][j]])
                                      for j in ["effective", "ineffective"])
            out += f"|{poke_type.capitalize()}|{effective}|{ineffective}|\n"

        return out + '\n'

    @staticmethod
    def items(multi_page: bool = False) -> str:
        """The function to add all items to the wiki.

        Arguments
        ---------
        - multi_page (boolean): if the item info should be made for a multi-page
          wiki or not.

        Returns
        -------
        A markdown string that contains information about all items.
        """
        return f"""#{'' if multi_page else '#'} Items
Those are all items present in the game, that can be traded or found.

""" + '\n'.join(Wiki.item_info(item=item, multi_page=multi_page)
                for item in sorted(items))

    @staticmethod
    def item_info(item: str, multi_page: bool = False) -> str:
        """The function to collect information and attributes of a specific item

        Arguments
        ---------
        - item (string): The item to collect the information of.
        - multi_page (boolean): if the item info should be made for a multi-page
          wiki or not.

        Returns
        -------
        A markdown string with the information about the item.
        """
        return f"""##{'' if multi_page else '#'} {items[item]["pretty_name"]}
{items[item]["desc"]}

- Price: {items[item]["price"]}
- Can be used in fights: {"Yes" if items[item]["fn"] is not None else "No"}
"""

    @staticmethod
    def effects(multi_page: bool = False) -> str:
        """The function to add all effects to the wiki.

        Arguments
        ---------
        - multi_page (boolean): if the item info should be made for a multi-page
          wiki or not.

        Returns
        -------
        A markdown string of all the effects in the game.
        """
        if multi_page:
            out = """# Effects
Those effects can be given to a Pokete through an attack.
"""
            out += str.join("", [effect.ret_md() for effect in
                                 effect_list]).replace("###", "##")
        else:
            out = """
## Effects
Those effects can be given to a Pokete through an attack.
"""
            out += str.join("", [effect.ret_md() for effect in effect_list])
        return out

    @staticmethod
    def single(filename: str = "wiki.md") -> None:
        """The function to generate a single page wiki.

        This function creates the pokete wiki in a single file and adds the
        following to it:
        - title
        - table of contents
        - all poketes with information on them
        - all attacks with information on them
        - all types with information on them
        - all items with information on them
        - all effects with information on them

        Arguments:
        ---------
        - filename (string): The file to save the wiki to.
        """
        if QUIET or VERBOSE:
            print(":: Generating wiki.md...")
        md_str: str = ""
        for _text, obj in zip(["page start", "table of contents", "poketes",
                               "attacks", "types", "items", "effects"],
                              [Wiki.start, Wiki.table_of_contents, Wiki.poketes,
                               Wiki.attacks, Wiki.types, Wiki.items,
                               Wiki.effects]):
            if QUIET or VERBOSE:
                print(f"==> Adding {_text}...")
            md_str += obj()

        # writing to file
        if QUIET or VERBOSE:
            print("==> Writing to wiki.md...")
        with open(filename, "w+") as file:
            file.write(md_str)

    @staticmethod
    def multi(folder_name: str = "wiki") -> None:
        """The function to generate the wiki in multiple pages in a folder

        This function creates the pokete wiki in a single file and adds the
        following to it:
        - title
        - table of contents
        - all poketes with information on them
        - all attacks with information on them
        - all types with information on them
        - all items with information on them
        - all effects with information on them

        Arguments:
        ---------
        - folder_name (string): The folder to save the wiki to.
        """
        if QUIET or VERBOSE:
            print(":: Generating multi-page wiki...")
            print("==> Checking if old wiki exists...")
        for folder in ['', '/poketes', '/attacks']:
            if VERBOSE:
                print(f' -> Checking "{folder_name}{folder}": ', end='')
            if exists(folder_name + folder):
                if not isdir(folder_name + folder):
                    if VERBOSE:
                        print("Does not exist. Making...")
                    os.mkdir(folder_name + folder)
                else:
                    if VERBOSE:
                        print("Exists. Deleting and making new...")
            else:
                os.mkdir(folder_name + folder)
                if VERBOSE:
                    print("Does not exist. Making...")

        if QUIET or VERBOSE:
            print("==> Adding page start...")
        if VERBOSE:
            print(" -> Adding index...")
        index: str = Wiki.start()
        if VERBOSE:
            print(" -> Adding overview...")
        index += Wiki.overview(multi_page=True) + "\n---\n"
        if VERBOSE:
            print(" -> Adding table of contents...")
        index += Wiki.table_of_contents(multi_page=True)
        if VERBOSE:
            print(f' -> Writing to "{folder_name}/index.md"...')
        with open(f"{folder_name}/index.md", 'w') as file:
            file.write(index)

        if QUIET or VERBOSE:
            print("==> Adding poketes...")
        if VERBOSE:
            print(" -> Adding index.md...")
        with open(f"{folder_name}/poketes/index.md", 'w') as file:
            file.write(Wiki.poketes(page_mode='index'))
        for typ in types:
            with open(f"{folder_name}/poketes/{typ}.md", 'w') as file:
                file.write(Wiki.poketes(page_mode='multi', pokete_type=typ))

        if QUIET or VERBOSE:
            print("==> Adding attacks...")
        for page in Wiki.attacks(multi_page=True):
            file_name, file_contents = page
            with open(f"{folder_name}/attacks/{file_name}", 'w') as file:
                file.write(file_contents)

        for name in ["types", "items", "effects"]:
            if QUIET or VERBOSE:
                print(f"==> Adding {name}...")
            with open(f"{folder_name}/{name}.md", 'w') as file:
                file.write(getattr(Wiki, name)(multi_page=True))


def gen_pics():
    """The function to generate a markdown file with some example pictures."""
    if QUIET or VERBOSE:
        print(":: Generating pics.md...")
    md_str = """# Example pictures
""" + "\n\n".join(f"![{i}](ss/{i})" for i in sorted(os.listdir("assets/ss")))

    # writing to file
    with open("assets/pics.md", "w+") as file:
        file.write(md_str)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        SILENT, QUIET, VERBOSE = False, True, False
        Wiki.single()
        gen_pics()
    else:
        for arg in sys.argv[1:]:
            if arg.lower() in ["silent", "quite", "verbose"]:
                SILENT, QUIET, VERBOSE = False, False, False
                if arg.lower() == "silent":
                    SILENT = True
                elif arg.lower() == "quite":
                    QUIET = True
                else:
                    VERBOSE = True
            elif arg.lower() == "single":
                Wiki.single()
            elif arg.lower() == "multi":
                Wiki.multi("wiki")
            elif arg.lower() == "pics":
                gen_pics()
            else:
                print(f"""gen_wiki.py:

Usage:
------
{sys.argv[0]} OPTION1 (OPTION2 OPTION3 ...)

Options:
--------
silent:\t\tPrints no statements at all
quite:\t\tPrints only some minimal statements
verbose:\tPrints everything that it's doing
single:\t\tGenerated the `wiki.md` as a single file
multi:\t\tGenerates a folder `wiki` with the wiki files
\t\t(Warning: Links are for html pages, not markdown pages!)
pics:\t\tGenerates the `assets/pics.md` file with all sample pictures

Examples:
---------
- {sys.argv[0]} silent single verbose multi
\t`-> Creates wiki.md silently and the multi-wiki verbosely
- {sys.argv[0]} quite single multi pics
\t`-> Creates wiki.md, the multi-page wiki and pics.md quitely

Copyright (c) lxgr-linux <lxgr-linux@protonmail.com> 2021""")
                if arg.lower() not in ["-h", "--help", "help"]:
                    sys.exit(2)
