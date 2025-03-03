from pokete.base.ui.elements import Box


class InvBox(Box):
    """Box wrapper for inv"""

    def resize_view(self):
        """Manages recursive view resizing"""
        self.remove()
        self.overview.resize_view()
        self.add(self.map, self.overview.box.x - 19, 3)
