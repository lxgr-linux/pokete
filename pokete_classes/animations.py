"""This file contains most of the animations used in Pokete"""

import time
import scrap_engine as se
import pokete_classes.game_map as gm
from release import SPEED_OF_TIME


def transition(_map, poke):
    """Transition animation for world actions
    ARGS:
        _map: se.Map object the transition happens on
        poke: Poke object shown in the transition"""
    vec_1 = se.Line(" ", _map.width, 0)
    vec_2 = se.Line(" ", _map.width, 0)

    vec_1.add(_map, 0, round(_map.height/2)-3)
    vec_2.add(_map, 0, round(_map.height/2)+3)

    for i, j in zip(reversed(vec_2.obs), vec_1.obs):
        for obj in [i, j]:
            obj.rechar("#")
        time.sleep(SPEED_OF_TIME * 0.005)
        _map.show()

    time.sleep(SPEED_OF_TIME * 0.5)
    poke.ico.add(_map, round((_map.width - 11) / 2),
                 round((_map.height - 4) / 2))
    _map.show()
    time.sleep(SPEED_OF_TIME * 1)
    poke.ico.remove()
    _map.show()

    for i, j in zip(reversed(vec_2.obs), vec_1.obs):
        for obj in [i, j]:
            obj.rechar(" ")
        time.sleep(SPEED_OF_TIME * 0.005)
        _map.show()

    vec_1.remove()
    vec_2.remove()


def fight_intro(height, width):
    """Intro animation for fight
    ARGS:
        height: Height of the animation
        width: Width of the animation"""
    fancymap = gm.GameMap(height, width)
    vec_list = [se.Line(" ", i * int(width / 2), j * int((height - 1) / 2))
                for i, j in zip([1, 1, -1, -1], [1, -1, -1, 1])]
    for i in vec_list:
        i.add(fancymap, int(width / 2), int((height - 1) / 2))
    fancymap.show()
    for i, _l in zip(list(zip(*[j.obs for j in vec_list])),
                     list(zip(*[list(2 * " ") + k
                              for k in [j.obs for j in vec_list]])), ):
        for j in i:
            j.rechar("-")
        for j in _l:
            if j != " ":
                j.rechar(" ")
        fancymap.show()
        time.sleep(SPEED_OF_TIME * 0.005)
    for i in vec_list:
        i.remove()
    del fancymap


if __name__ == "__main__":
    print("\033[31;1mDo not execute this!\033[0m")
