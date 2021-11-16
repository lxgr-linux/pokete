import time
import scrap_engine as se


def transition(_map, poke):
    """Transition animation for world actions"""
    vec_1 = se.Line(" ", _map.width, 0)
    vec_2 = se.Line(" ", _map.width, 0)

    vec_1.add(_map, 0, round(_map.height/2)-3)
    vec_2.add(_map, 0, round(_map.height/2)+3)

    for i, j in zip(reversed(vec_2.obs), vec_1.obs):
        for obj in [i, j]:
            obj.rechar("#")
        time.sleep(0.005)
        _map.show()

    time.sleep(0.5)
    poke.ico.add(_map, round((_map.width - 11) / 2),
                 round((_map.height - 4) / 2))
    _map.show()
    time.sleep(1)
    poke.ico.remove()
    _map.show()

    for i, j in zip(reversed(vec_2.obs), vec_1.obs):
        for obj in [i, j]:
            obj.rechar(" ")
        time.sleep(0.005)
        _map.show()

    vec_1.remove()
    vec_2.remove()
