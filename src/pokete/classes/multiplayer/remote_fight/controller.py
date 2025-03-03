import logging
from threading import Event
from typing import Generator

import pokete.bs_rpc as bs_rpc
from pokete.base.context import Context
from pokete.base.input_loops.ask import wait_event
from pokete.classes.multiplayer.remote_fight.fight import RemoteFight
from pokete.classes.multiplayer.remote_fight.figure_wrapper import FigureWrapperProvider
from pokete.classes.multiplayer.remote_fight.provider import RemoteProvider
from pokete.classes.multiplayer.msg import fight


class RemoteFightController:
    def __init__(self) -> None:
        #self.active = False
        self.end = Event()
        self.__start = Event()
        self.outgoing: bs_rpc.ResponseWriter
        self.incomming: Generator[bs_rpc.Body, None, None]
        self.com_service = None
        self.__start.clear()

    def __wait_starter(self) -> str:
        resp = next(self.incomming)
        match resp.type:
            case fight.STARTER_TYPE:
                data: fight.StarterData = resp.data
                return data["name"]
            case _:
                assert False

    def start(self, ctx:Context, name:str):
        #self.__start.clear()
        logging.info(f"waiting fight {ctx.figure.name}")
        wait_event(ctx, "Waiting for fight...", self.__start)
        logging.info(f"fight starts {ctx.figure.name}")

        starter = self.__wait_starter()

        RemoteFight(starter != name)(ctx, [
            FigureWrapperProvider(ctx.figure, self.outgoing, self.incomming),
            RemoteProvider(
                name, self.outgoing, self.incomming, self.com_service
            )
        ])
        logging.info("hmm")

    def ready(self, outgoing, incomming: bs_rpc.ChannelGenerator, com_service):
        self.outgoing = outgoing
        self.incomming = incomming()
        self.com_service = com_service
        #self.active = True
        self.__start.set()
        self.end.clear()


remote_fight_controller = RemoteFightController()
