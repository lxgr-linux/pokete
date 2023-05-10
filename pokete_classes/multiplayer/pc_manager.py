import scrap_engine as se

from pokete_classes import ob_maps as obmp


class PCManager:
    def __init__(self):
        self.reg = {}
        
    def set(self, name, _map, x, y):
        if name not in self.reg:
            self.reg[name] = se.Object("a", "float")
        self.reg[name].remove()
        self.reg[name].add(obmp.ob_maps[_map], x, y)
        
    def remove(self, name):
        self.reg[name].remove()
        del self.reg[name]
        

pc_manager = PCManager()
            