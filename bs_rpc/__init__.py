import json
import logging
import time
import threading

from bs_rpc.msg import Body, Method, Msg, EmptyMsg
from .registry import Registry

END_SECTION = b"<END>"


class Client:
    def __init__(self, rw, reg: Registry):
        self.rw = rw
        self.reg = reg
        self.calls: dict[int: tuple[threading.Event, list[Body]]] = {}

    def __send(self, body: Body, call: int, method: Method):
        """Sends a request to the server
        ARGS:
            body: dict that is send"""
        payload = {
            "type": body.get_type(),
            "call": call,
            "method": method.value,
            "body": body.data
        }
        self.rw.sendall(
            str.encode(
                json.dumps(payload)
            ) + END_SECTION
        )

    def __get_call(self, call_id: int) -> tuple[threading.Event, list[Body]]:
        if (
            call := self.calls.get(call_id)
        ) is not None:
            return call
        else:
            raise Exception("call id for response not found")

    def call_for_response(self, body: Body) -> Body:
        event = threading.Event()
        call_id = int(time.time())
        self.__send(body, call_id, Method.CALL_FOR_RESPONSE)
        self.calls[call_id] = (event, [])
        event.wait()
        call = self.__get_call(call_id)[1]
        del self.calls[call_id]
        return call[0]

    def listen(self, context):
        msg_buf = b""
        while True:
            data = self.rw.recv(32)
            msg_buf += data
            if END_SECTION in data:
                msg_parts = msg_buf.split(END_SECTION)

                msg: Msg = json.loads(msg_parts[0])
                logging.info("[BsRpc] Received data: %s", msg)

                body: Body = self.reg.get(msg["type"])(
                    data=msg["body"]
                )

                match Method(msg["method"]):
                    case Method.CALL_FOR_RESPONSE:
                        resp: Body = body.call_for_response(context)
                        self.__send(
                            resp, msg["call"],
                            Method.RESPONSE
                        )
                    case Method.CALL_FOR_RESPONSES:
                        def response_writer(b: Body):
                            self.__send(b, msg["call"], Method.RESPONSE)

                        body.call_for_responses(context, response_writer)
                        self.__send(
                            EmptyMsg({}), msg["call"],
                            Method.RESPONSE_CLOSE
                        )
                    case Method.RESPONSE:
                        call = self.__get_call(msg["call"])
                        call[1].append(body)
                        call[0].set()
                        call[0].clear()
                    case Method.RESPONSE_CLOSE:
                        self.__get_call(msg["call"])
                        del self.calls[msg["call"]]

                msg_buf = bytes.join(END_SECTION, msg_parts[1:])
