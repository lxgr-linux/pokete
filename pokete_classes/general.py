"""Contains some stuff that's used in this module"""

import logging
from pokete_classes import movemap as mvp
from .doors import DoorToCenter
from .input import ask_ok


def check_walk_back(figure, self=None):
    """Check whether the figure has to be walked back to the last Poketecenter
       or not"""
    if all(i.hp <= 0 for i in figure.pokes[:6]):
        amount = round(figure.get_money() / 3)
        figure.add_money(-amount)
        heal(figure)
        ask_ok(mvp.movemap, f"""All your Poketes have died and you ran
back to the last Pokecenter you visited to heal them!
On the way there, ${amount} fell out of your pocket!""")
        figure.remove()
        figure.map = figure.last_center_map
        logging.info("[Figure] You lost all Poketes and ran away!")
        DoorToCenter().action(figure)


def heal(figure):
    """Heals all poketes
    ARGS:
        figure: Figure object"""
    for poke in figure.pokes:
        poke.hp = poke.full_hp
        poke.effects = []
        poke.miss_chance = poke.full_miss_chance
        poke.text_hp.rechar(f"HP:{poke.hp}")
        poke.set_vars()
        poke.hp_bar.make(poke.hp)
        mvp.movemap.balls_label_rechar(figure.pokes)
