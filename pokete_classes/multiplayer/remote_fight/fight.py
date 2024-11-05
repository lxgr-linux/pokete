import logging
from threading import Event

import bs_rpc
from pokete_classes.context import Context
from pokete_classes.fight import Fight
from pokete_classes.input_loops.ask import wait_event
from pokete_classes.multiplayer.remote_fight.provider import RemoteProvider


class RemoteFight:
    def __init__(self) -> None:
        #self.active = False
        self.end = Event()
        self.__start = Event()
        self.outgoing: bs_rpc.ResponseWriter
        self.incomming: bs_rpc.ChannelGenerator
        self.com_service = None
        self.__start.clear()

    def start(self, ctx:Context, name:str):
        #self.__start.clear()
        logging.info(f"waiting fight {ctx.figure.name}")
        wait_event(ctx, "Waiting for fight...", self.__start)
        logging.info(f"fight starts {ctx.figure.name}")
        Fight()(ctx, [
            ctx.figure,
            RemoteProvider(
                name, self.outgoing, self.incomming, self.com_service
            )
        ])
        logging.info("hmm")

    def ready(self, outgoing, incomming: bs_rpc.ChannelGenerator, com_service):
        self.outgoing = outgoing
        self.incomming = incomming
        self.com_service = com_service
        #self.active = True
        self.__start.set()
        self.end.clear()


remote_fight = RemoteFight()
