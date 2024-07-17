import scrap_engine as se

from pokete_classes.input import Action
from .box import Box


class LabelBox(Box):
    """A Box just containing one label
    ARGS:
        label: The se.Text label
        name: The boxes displayed name
        info: Info that will be displayed in the bottom left corner of the box"""

    def __init__(self, label, name="", info="", overview=None):
        self.label = label
        super().__init__(
            label.height + 2, label.width + 4, name, info,
            overview=overview
        )
        self.add_ob(label, 2, 1)


class InfoBox(LabelBox):
    """Box to display basic text information in
    ARGS:
        text: String displayed
        name: The boxes displayed name
        info: Info that will be displayed in the bottom left corner of the box
        _map: The se.Map this will be shown on"""

    def __init__(
        self, text, name="",
        info=f"{Action.CANCEL.mapping}:close",
        _map=None, overview=None
    ):
        super().__init__(se.Text(text), name=name, info=info, overview=overview)
        self.map = _map

    def __enter__(self):  # Contextmanagement is fucking awesome!
        """Enter dunder for contextmanagement"""
        self.center_add(self.map)
        self.map.show()
        return self


class InputBox(InfoBox):
    """Box that promps the user to input a text
    ARGS:
        _map: The map the input box should be shown on
        infotext: The information text about the input
        introtext: The text that introduces the text field
        text: The default text in the text field
        name: The boxes desplayed name
        max_len: Max length of the text"""

    def __init__(
        self, infotext, introtext, text, max_len,
        name="", _map=None, overview=None
    ):
        height = len(infotext.split("\n")) + 3
        width = sorted([len(i) for i in infotext.split("\n")]
                       + [len(introtext) + 1 + max_len])[-1] + 4
        super(LabelBox, self).__init__(height, width, name, overview=overview)
        self.map = _map
        self.infotext = se.Text(infotext)
        self.introtext = se.Text(introtext)
        self.text = se.Text(text)
        self.add_ob(self.infotext, 2, 1)
        self.add_ob(self.introtext, 2, len(infotext.split("\n")) + 1)
        self.add_ob(self.text, self.introtext.rx + len(introtext) + 1,
                    self.introtext.ry)
