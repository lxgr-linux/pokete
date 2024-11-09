from threading import Event, main_thread

import bs_rpc
from pokete_classes.input_loops.ask import ask_bool
from pokete_classes.multiplayer.remote_fight import remote_fight_controller


class MainThreatFightAttacher:
    def __init__(self):
        self.__ready = False
        self.__chan: bs_rpc.Channel
        self.__name: str

    def attach(self, ctx):
        if self.__ready:
            accept = ask_bool(
                ctx,
                f"'{self.__name}' wants to start a fight with you"
            )
            self.__chan.push(accept)
            self.__chan.close
            remote_fight_controller.start(ctx, self.__name)
            self.__ready = False

    def set_ready(self, name) -> bs_rpc.Channel:
        self.__chan = bs_rpc.Channel()
        self.__ready = True
        self.__name = name
        return self.__chan

main_thread_fight_attacher = MainThreatFightAttacher()
