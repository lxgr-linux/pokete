import logging
from threading import Event

import bs_rpc
from pokete_classes.context import Context
from pokete_classes.input_loops.ask import wait_event


class RemoteFight:
    def __init__(self) -> None:
        #self.active = False
        self.end = Event()
        self.__start = Event()
        self.outgoing = None
        self.incomming: bs_rpc.ChannelGenerator | None = None
        self.__start.clear()

    def start(self, ctx:Context):
        #self.__start.clear()
        logging.info(f"waiting fight {ctx.figure.name}")
        wait_event(ctx, "Waiting for fight...", self.__start)
        logging.info(f"fight starts {ctx.figure.name}")

    def ready(self, outgoing, incomming: bs_rpc.ChannelGenerator):
        self.outgoing = outgoing
        self.incomming = incomming
        #self.active = True
        self.__start.set()
        self.end.clear()


remote_fight = RemoteFight()
