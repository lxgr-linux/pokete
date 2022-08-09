"""Contains some stuff that's used in this module"""

import logging
from . import movemap as mvp
from .doors import DoorToCenter
from .input import ask_ok


def check_walk_back(figure, self=None):
    """Check whether the figure has to be walked back to the last Poketecenter
       or not"""
    if all(i.hp <= 0 for i in figure.pokes[:6]):
        amount = round(figure.get_money() / 3)
        figure.add_money(-amount)
        figure.heal()
        ask_ok(mvp.movemap, f"""All your Poketes have died and you ran
back to the last Pokecenter you visited to heal them!
On the way there, ${amount} fell out of your pocket!""")
        figure.remove()
        figure.map = figure.last_center_map
        logging.info("[Figure] You lost all Poketes and ran away!")
        DoorToCenter().action(figure)
