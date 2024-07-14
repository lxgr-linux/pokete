from ..ui.elements import Box
from .. import movemap as mvp


class InvBox(Box):
    """Box wrapper for inv"""

    def resize_view(self):
        """Manages recursive view resizing"""
        self.remove()
        self.overview.resize_view()
        self.add(self.map, self.overview.box.x - 19, 3)
        mvp.movemap.full_show()
