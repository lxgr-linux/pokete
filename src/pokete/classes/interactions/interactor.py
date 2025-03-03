import logging
import time
from abc import ABC, abstractmethod
import scrap_engine as se

from pokete.release import SPEED_OF_TIME
from pokete.base.context import Context
from .interactor_interface import InteractorInterface
from .. import movemap as mvp


class Interactor(InteractorInterface, ABC):
    """Interactor interface for map interactions"""
    x: int
    y: int
    ctx: Context
    map: se.Map
    name: str

    @abstractmethod
    def set(self, x, y):
        pass

    def text(self, text):
        """Movemap.text wrapper
        ARGS:
            text: Text that should be printed"""
        mvp.movemap.text(self.ctx, self.x, self.y, text)

    def check_walk(self, _x, _y):
        """Checks whether the NPC can walk to a point or not
        ARGS:
            _x: X-coordinate
            _y: Y-coordinate
        RETURNS:
            bool: Whether or not the walk is possible"""
        vec = se.Line(" ", _x - self.x, _y - self.y)
        ret = not any([any(j.state == "solid"
                           for j in
                           self.map.obmap[i.ry + self.y][i.rx + self.x])
                       for i in vec.obs][1:])
        logging.info("[NPC][%s] %s walk check to (%d|%d)",
                     self.name, 'Succeeded' if ret else 'Failed', _x, _y)
        return ret

    def walk_point(self, _x, _y):
        """Walks the NPC tp a certain point
        ARGS:
            _x: X-coordinate
            _y: Y-coordinate
        RETURNS:
            bool: Whether or not the walk succeeded"""
        o_x = self.x
        o_y = self.y
        vec = se.Line(" ", _x - o_x, _y - o_y)
        if not self.check_walk(_x, _y):
            return False
        for i in vec.obs:
            self.set(i.rx + o_x, i.ry + o_y)
            mvp.movemap.full_show()
            time.sleep(SPEED_OF_TIME * 0.2)
        return True

    def exclamate(self):
        """Shows the exclamation on top of a NPC"""
        exclamation = se.Object("!")
        try:
            exclamation.add(mvp.movemap, self.x - mvp.movemap.x,
                            self.y - 1 - mvp.movemap.y)
        except se.CoordinateError:
            pass
        mvp.movemap.show()
        time.sleep(SPEED_OF_TIME * 1)
        exclamation.remove()
