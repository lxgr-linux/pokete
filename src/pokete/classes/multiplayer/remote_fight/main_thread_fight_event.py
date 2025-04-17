import pokete.bs_rpc as bs_rpc
from pokete.base.context import Context
from pokete.base.input_loops.ask import ask_bool
from pokete.base.single_event import SingleEvent
from pokete.classes.multiplayer.remote_fight import remote_fight_controller


class MainThreatFightEvent(SingleEvent):
    def __init__(self, name: str):
        self.__name: str = name
        self.__chan:bs_rpc.Channel[bool] = bs_rpc.Channel[bool]()

    def wait_accepted(self) -> bool:
        return not not self.__chan.listen()

    def run(self, ctx:Context):
        accept = ask_bool(
            ctx,
            f"'{self.__name}' wants to start a fight with you"
        )
        self.__chan.push(accept)
        self.__chan.close
        remote_fight_controller.start(ctx, self.__name)
