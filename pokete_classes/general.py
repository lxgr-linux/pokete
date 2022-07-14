"""Contains some stuff that's used in this module"""

import logging
from pokete_classes import movemap as mvp
from .doors import DoorToCenter
from .input import ask_ok
from .language import lang


def check_walk_back(figure, self=None):
    """Check whether the figure has to be walked back to the last Poketecenter
       or not"""
    if all(i.hp <= 0 for i in figure.pokes[:6]):
        amount = round(figure.get_money() / 3)
        figure.add_money(-amount)
        heal(figure)
        ask_ok(mvp.movemap, lang.str("dialog.attack.blackout") % amount)
        figure.remove()
        figure.map = figure.last_center_map
        logging.info(lang.str("log.fight.blackout"))
        DoorToCenter().action(figure)


def heal(figure):
    """Heals all poketes
    ARGS:
        figure: Figure object"""
    for poke in figure.pokes:
        poke.hp = poke.full_hp
        poke.effects = []
        poke.miss_chance = poke.full_miss_chance
        poke.text_hp.rechar(f"{lang.str('dialog.attack.hp')}:{poke.hp}")
        poke.set_vars()
        poke.hp_bar.make(poke.hp)
        mvp.movemap.balls_label_rechar(figure.pokes)
