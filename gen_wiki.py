#!/usr/bin/env python3
"""This script generates the Pokete wiki"""
import os
from os.path import exists, isdir
import release
import scrap_engine as se
from pokete_classes.effects import effects, effect_list
from pokete_data import *


class Wiki:
    """The class in which wiki generation behaviour is defined"""
    @staticmethod
    def start() -> str:
        """The start and title of the wiki

        Returns:
        ---
        The title of the wiki page.
        """
        return f"""v{release.VERSION}

# Pokete wiki
This wiki/documentation is a compilation of all Poketes/attacks/types present in the Pokete game.
This wiki can be generated using ```$ ./gen-wiki.py```.

"""

    @staticmethod
    def overview(multi_page: bool = False) -> str:
        """A short overview of what the wiki contains.

        Returns:
        -------
        An overview for a multi-page wiki.
        """
        if multi_page:
            return """Table of contents
1. [Poketes](poketes)
2. [Attacks](attacks)
3. [Types](types)
4. [Items](items)
5. [Effects](effects)
"""
        else:
            return """Table of contents
1. [Poketes](#poketes)
2. [Attacks](#attacks)
3. [Types](#types)
4. [Items](#items)
5. [Effects](#effects)
"""

    @staticmethod
    def table_of_contents(multi_page: bool = False) -> str:
        """The table of contents of the pokete wiki

        Returns:
        -------
        A Table of contents for a single page wiki.
        """
        out = ''

        # Table of contents
        if not multi_page:
            out += f"""## Table of contents
1. [Poketes](#poketes)
"""
            for i, typ in enumerate(sorted(types)):
                out += f"""   {i + 1}. [{typ.capitalize()} Poketes](#{typ}-poketes)\n"""
                for j, poke in enumerate([k for k in sorted(list(pokes)[1:]) if pokes[k]["types"][0] == typ]):
                    out += f"""       {j + 1}. [{pokes[poke]["name"]}](#{poke.replace("_", "-")})\n"""
            out += "2. [Attacks](#attacks)\n"
            for i, typ in enumerate(sorted(types)):
                out += f"""   {i + 1}. [{typ.capitalize()} attacks](#{typ}-attacks)\n"""
                for j, atc in enumerate([k for k in sorted(attacks) if attacks[k]["types"][0] == typ]):
                    out += f"""       {j + 1}. [{attacks[atc]["name"]}](#{atc.replace("_", "-")})\n"""
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
            out += f"""## Table of contents
1. [Poketes](./poketes)
"""
            for i, typ in enumerate(sorted(types)):
                out += f"""   {i + 1}. [{typ.capitalize()} Poketes](./poketes/{typ})\n"""
                for j, poke in enumerate([k for k in sorted(list(pokes)[1:]) if pokes[k]["types"][0] == typ]):
                    out += f"""       {j + 1}. [{pokes[poke]["name"]}](./poketes/{typ}#{poke.replace("_", "-")})\n"""
            out += "2. [Attacks](./attacks)\n"
            for i, typ in enumerate(sorted(types)):
                out += f"""   {i + 1}. [{typ.capitalize()} attacks](./attacks/{typ})\n"""
                for j, atc in enumerate([k for k in sorted(attacks) if attacks[k]["types"][0] == typ]):
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
            - multi: Information about the pokete type definied in pokete_type with multi-page links.
        - pokete_type: Only necessary if page_mode is set to 'index': Then defines the pokete type to get the
          information and links of.

        Returns:
        -------
        All poketes and their attributes as a markdown string.
        """
        if page_mode == 'single':
            out = f"""
## Poketes
In the following all Poketes with their attributes are displayed.

"""
            for typ in sorted(types):
                out += f"### {typ.capitalize()} Poketes"
                for poke in [k for k in sorted(list(pokes)[1:]) if pokes[k]["types"][0] == typ]:
                    print(f' -> Adding {pokes[poke]["name"]}')
                    out += Wiki.poke_info(poke)
            return out
        elif page_mode == 'index':
            out = f"""# Poketes
In the following all Poketes with their attributes are displayed.

"""
            for typ in sorted(types):
                out += f"- [{typ.capitalize()} Poketes](./{typ})\n"
            out += "\n---\n\n## All poketes sorted by their type:\n"
            for typ in sorted(types):
                out += f"- [{typ.capitalize()} Poketes](./{typ})\n"
                for poke in [k for k in sorted(list(pokes)[1:]) if pokes[k]["types"][0] == typ]:
                    out += f"""  - [{pokes[poke]["name"].capitalize()}](./{typ}#{poke})\n"""
            return out
        elif page_mode == 'multi':
            if pokete_type is not None:
                out = f"# {pokete_type.capitalize()} Poketes"
                for poke in [k for k in sorted(list(pokes)[1:]) if pokes[k]["types"][0] == pokete_type]:
                    if poke == sorted(list(pokes)[1:])[-1]:
                        print(f'  `-> Adding {pokes[poke]["name"]}')
                    else:
                        print(f'  |-> Adding {pokes[poke]["name"]}')
                    out += Wiki.poke_info(poke=poke, multi_page=True)
                return out
            else:
                raise AttributeError("Pokete_type can not be none, if mode 'multi' is selected.")
        else:
            raise AttributeError("Please select a valid page mode of: 'single', 'index' or 'multi'!")

    @staticmethod
    def poke_info(poke: str, multi_page: bool = False) -> str:
        """Generates information about a specific pokete

        Arguments:
        ---------
        - poke (string): The pokete to get the information of.

        Returns:
        -------
        A markdown string of all the attributes and information of the pokete.
        """
        evolve_pokete = pokes[poke]["evolve_poke"]
        if evolve_pokete == "":
            evolve_txt = "- Does not evolve\n"
        else:
            evolve_txt = f"""- Evolves to [{pokes[evolve_pokete]['name']}]({f'./{pokes[evolve_pokete]["types"][0]}'
                            if multi_page else ""}#{evolve_pokete}) at level {pokes[poke]['evolve_lvl']}"""
        md_attacks = ""
        for atc in pokes[poke]["attacks"]:
            md_attacks += f"""\n   + [{attacks[atc]["name"]}]({f'../attacks/{attacks[atc]["types"][0].capitalize()}'
                          if multi_page else ""}#{atc.replace("_", "-")})"""
        # ico
        ico_map = se.Map(4, 11, background=" ")
        for ico in pokes[poke]["ico"]:
            se.Text(ico["txt"], state="float", ignore=" ").add(ico_map, 0, 0)
        ico = "".join(["".join(arr) + "\n" for arr in ico_map.map])
        return f"""
##{'' if multi_page else '##'} {pokes[poke]["name"]}
{pokes[poke]["desc"]}

```
{ico}
```

- Type: [{pokes[poke]["types"][0].capitalize()}]({'../types' if multi_page else '#types'})
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

    @staticmethod
    def attacks(multi_page: bool = False) -> str or list:
        """The function to all attacks to the wiki.

        Returns:
        -------
        A markdown string of all attacks with their attributes and informations.
        """
        if multi_page:
            index = f"""# Attacks
Those are all attacks present in the game.
"""
            pages = []
            for typ in sorted(types):
                print(f" -> Adding {typ}")
                index += f"\n- [{typ.capitalize()}](./{typ})"
                page = f"# {typ.capitalize()} attacks"
                for atc in [k for k in attacks if attacks[k]["types"][0] == typ]:
                    if multi_page:
                        if atc == [k for k in attacks if attacks[k]["types"][0] == typ][-1]:
                            print(f'  `-> Adding {attacks[atc]["name"]}')
                        else:
                            print(f'  |-> Adding {attacks[atc]["name"]}')
                    else:
                        print(f' -> Adding {attacks[atc]["name"]}')
                    page += Wiki.attack_info(atc, True)
                pages.append((f"{typ}.md", page))
            index += "\n\n---\n\n## All attacks sorted by their type:\n"
            for typ in sorted(types):
                index += f"- [{typ.capitalize()} Attacks](./{typ})\n"
                for atc in [k for k in attacks if attacks[k]["types"][0] == typ]:
                    index += f"""  - [{attacks[atc]["name"].capitalize()}](./{typ}#{atc.replace('_', '-')})\n"""

            index += '\n'
            pages.insert(0, ("index.md", index))
            return pages
        else:
            out = f"""
## Attacks
Those are all attacks present in the game.
"""
            for typ in sorted(types):
                out += f"\n### {typ.capitalize()} attacks"
                for atc in [k for k in attacks if attacks[k]["types"][0] == typ]:
                    if atc == [k for k in attacks if attacks[k]["types"][0] == typ][-1]:
                        print(f' `-> Adding {attacks[atc]["name"]}')
                    else:
                        print(f' |-> Adding {attacks[atc]["name"]}')
                    out += Wiki.attack_info(atc)

            return out

    @staticmethod
    def attack_info(attack: str, multi_page: bool = False) -> str:
        """The function to collect information and attributes of a specific attack

        Arguments:
        ---------
        - attacks (string): The attack to collect the information of.

        Returns:
        -------
        A markdown string with the information about the attack.
        """
        eff = None if attacks[attack]["effect"] is None else getattr(effects, attacks[attack]["effect"])
        if multi_page:
            out = "\n##"
        else:
            out = "\n####"
        return out + f""" {attacks[attack]["name"]}
{attacks[attack]["desc"]}

- Type: [{attacks[attack]["types"][0].capitalize()}]({"../types" if multi_page else "#types"})
- Minimum Level: {attacks[attack]["min_lvl"]}
- Attack factor: {attacks[attack]["factor"]}
- Missing chance: {attacks[attack]["miss_chance"]}
- Attack points: {attacks[attack]["ap"]}
- Effect: {"None" if eff is None else f'[{eff.c_name.capitalize()}]({"../effects" if multi_page else ""}#{eff.c_name.replace("_", "-")})'}
"""

    @staticmethod
    def types(multi_page: bool = False) -> str:
        """The function to add all types to the wiki.

        Returns:
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

        Arguments:
        ---------
        - multi_page (boolean): if the item info should be made for a multi-page wiki or not.

        Returns:
        -------
        A markdown string that contains information about all items.
        """
        out = f"""#{'' if multi_page else '#'} Items
Those are all items present in the game, that can be traded or found.
"""

        for item in sorted(items):
            out += '\n'
            out += Wiki.item_info(item=item, multi_page=multi_page)
        return out

    @staticmethod
    def item_info(item: str, multi_page: bool = False) -> str:
        """The function to collect information and attributes of a specific item

        Arguments:
        ---------
        - item (string): The item to collect the information of.
        - multi_page (boolean): if the item info should be made for a multi-page wiki or not.

        Returns:
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

        Returns:
        -------
        A markdown string of all the effects in the game.
        """
        if multi_page:
            out = """# Effects
Those effects can be given to a Pokete through an attack.
"""
            out += str.join("", [effect.ret_md() for effect in effect_list]).replace("###", "##")
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

        This function creates the pokete wiki in a single file and adds the following to it:
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
        print(":: Generating wiki.md...")
        print("==> Adding page start...")
        md_str = Wiki.start()
        print("==> Adding table of contents...")
        md_str += Wiki.table_of_contents()
        print("==> Adding poketes...")
        md_str += Wiki.poketes()
        print("==> Adding attacks...")
        md_str += Wiki.attacks()
        print("==> Adding types...")
        md_str += Wiki.types()
        print("==> Adding items...")
        md_str += Wiki.items()
        print("==> Adding effects...")
        md_str += Wiki.effects()

        # writing to file
        print("==> Writing to wiki.md...")
        with open(filename, "w+") as file:
            file.write(md_str)

    @staticmethod
    def multi(folder_name: str = "wiki") -> None:
        """The function to generate the wiki in multiple pages in a folder

        This function creates the pokete wiki in a single file and adds the following to it:
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
        print(":: Generating multi-page wiki...")
        print("==> Checking if old wiki exists...")
        for folder in ['', '/poketes', '/attacks']:
            print(f" -> Checking \"{folder_name}{folder}\": ", end='')
            if exists(folder_name + folder):
                if not isdir(folder_name + folder):
                    print("Does not exist. Making...")
                    os.mkdir(folder_name + folder)
                else:
                    print("Exists. Deleting and making new...")
            else:
                os.mkdir(folder_name + folder)
                print("Does not exist. Making...")

        print("==> Adding page start...")
        print(" -> Adding index...")
        index: str = Wiki.start()
        print(" -> Adding overview...")
        index += Wiki.overview(multi_page=True)
        index += "\n---\n"
        print(" -> Adding table of contents...")
        index += Wiki.table_of_contents(multi_page=True)
        print(f" -> Writing to \"{folder_name}/index.md\"...")
        with open(f"{folder_name}/index.md", 'w') as file:
            file.write(index)

        print("==> Adding poketes...")
        print(" -> Adding index.md...")
        with open(f"{folder_name}/poketes/index.md", 'w') as file:
            file.write(Wiki.poketes(page_mode='index'))
        for typ in types:
            with open(f"{folder_name}/poketes/{typ}.md", 'w') as file:
                file.write(Wiki.poketes(page_mode='multi', pokete_type=typ))

        print("==> Adding attacks...")
        for page in Wiki.attacks(multi_page=True):
            file_name, file_contents = page
            with open(f"{folder_name}/attacks/{file_name}", 'w') as file:
                file.write(file_contents)

        print("==> Adding types...")
        with open(f"{folder_name}/types.md", 'w') as file:
            file.write(Wiki.types(multi_page=True))

        print("==> Adding items...")
        with open(f"{folder_name}/items.md", 'w') as file:
            file.write(Wiki.items(multi_page=True))

        print("==> Adding effects...")
        with open(f"{folder_name}/effects.md", 'w') as file:
            file.write(Wiki.effects(multi_page=True))


def gen_pics():
    """The function to generate a markdown file with some example pictures."""
    md_str = "# Example pictures\n"
    md_str += str.join("\n\n", [f"![{i}](ss/{i})" for i in sorted(os.listdir("assets/ss"))])

    # writing to file
    with open("assets/pics.md", "w+") as file:
        file.write(md_str)


if __name__ == "__main__":
    Wiki.single()
    Wiki.multi("wiki")
    print(":: Generating pics.md...")
    gen_pics()
