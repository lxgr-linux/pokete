"""Manages responses from the server"""
from pokete_classes.multiplayer import connector
from pokete_classes.multiplayer.pc_manager import pc_manager


class ResponseManager:
    """Manages responses from the server"""
    
    def __call__(self):
        while True:
            if (d := connector.connector.receive_data())["Type"] == 1:
                b = d["Body"]
                pc_manager.set(b["Name"], b["Position"]["Map"],
                               b["Position"]["X"], b["Position"]["Y"])
            elif d["Type"] == 4:
                pass
            elif d["Type"] == 5:
                pc_manager.remove(d["Body"])
