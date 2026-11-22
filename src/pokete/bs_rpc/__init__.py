import json
import logging
import threading
import time

from .channel import Channel
from .channel_generator import ChannelGenerator
from .msg import Body, EmptyMsg, Method, Msg, ResponseWriter
from .registry import Registry

__all__ = [
    "Body",
    "Channel",
    "ChannelGenerator",
    "Client",
    "EmptyMsg",
    "Method",
    "Msg",
    "Registry",
    "ResponseWriter",
]

END_SECTION = b"<END>"


class Client:
    logger = logging.getLogger("Client")

    def __init__(self, rw: "ResponseWriter", reg: Registry) -> None:
        self.rw = rw
        self.reg = reg
        self.calls: dict[int, Channel[Body]] = {}

    def __send(self, body: Body, call: int, method: Method) -> None:
        """Sends a request to the server
        ARGS:
            body: dict that is send"""
        payload = {
            "type": body.get_type(),
            "call": call,
            "method": method.value,
            "body": body.data,
        }
        self.rw.sendall(str.encode(json.dumps(payload)) + END_SECTION)

    def __get_call(self, call_id: int) -> Channel[Body]:
        if (call := self.calls.get(call_id)) is not None:
            return call
        else:
            raise KeyError(f"call id `{call_id}`for response not found")

    def __new_call_id(self) -> None:
        call_id = int(time.time())
        while call_id in self.calls:
            call_id += 1
        return call_id

    def call_for_response(self, body: Body) -> Body | None:
        ch = Channel[Body]()
        call_id = self.__new_call_id()
        self.calls[call_id] = ch
        self.__send(body, call_id, Method.CALL_FOR_RESPONSE)
        call = ch.listen()
        del self.calls[call_id]
        return call

    def call_for_responses(self, body: Body) -> ChannelGenerator:
        ch = Channel[Body]()
        call_id = self.__new_call_id()
        self.calls[call_id] = ch
        self.__send(body, call_id, Method.CALL_FOR_RESPONSES)

        def close_fn() -> None:
            del self.calls[call_id]

        return ChannelGenerator(ch, close_fn)

    def __eval_msg(self, context: dict, msg: Msg, body: Body) -> None:
        match Method(msg["method"]):
            case Method.CALL_FOR_RESPONSE:
                resp: Body = body.call_for_response(context)
                self.__send(resp, msg["call"], Method.RESPONSE)
            case Method.CALL_FOR_RESPONSES:

                def response_writer(b: Body) -> None:
                    self.__send(b, msg["call"], Method.RESPONSE)

                body.call_for_responses(context, response_writer)
                self.__send(EmptyMsg({}), msg["call"], Method.RESPONSE_CLOSE)
            case Method.RESPONSE:
                ch = self.__get_call(msg["call"])
                ch.push(body)
            case Method.RESPONSE_CLOSE:
                ch = self.__get_call(msg["call"])
                ch.close()

    def listen(self, context: dict) -> None:
        msg_buf = b""
        while True:
            data = self.rw.recv(32)
            msg_buf += data
            while END_SECTION in msg_buf:
                msg_parts = msg_buf.split(END_SECTION)

                msg: Msg = json.loads(msg_parts[0])
                # self.logger.info("[BsRpc] Received data: %s", msg)

                body: Body = self.reg.get(msg["type"])(data=msg["body"])

                threading.Thread(
                    target=self.__eval_msg, args=(context, msg, body)
                ).start()

                msg_buf = bytes.join(END_SECTION, msg_parts[1:])
