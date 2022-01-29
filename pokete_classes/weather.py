from pokete_data import weathers


class Weather:
    def __init__(self, index):
        self.info = weathers[index]["info"]
        self.effected = weathers[index]["effected"]

    def effect(self, typ):
        return self.effected.get(typ.name, 1)
