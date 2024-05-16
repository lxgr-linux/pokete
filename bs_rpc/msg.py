from enum import Enum
from typing import TypedDict


class Method(Enum):
    CALL_FOR_RESPONSE = "call_for_response"
    CALL_FOR_RESPONSES = "call_for_responses"
    RESPONSE_CLOSE = "response close"
    RESPONSE = "response"


class Body:
    def __init__(self, msg_type: str, data: dict):
        self.type = msg_type
        self.data = data

    def call_for_response(self, context):
        """returns Body"""
        raise Exception(f"call_for_response not implemented for {self.type}")

    def call_for_responses(self, context, response_writer):
        raise Exception(f"call_for_responses not implemented for {self.type}")

    def get_type(self):
        return self.type


class Msg(TypedDict):
    type: str
    method: str
    call: int
    body: dict


class EmptyMsg(Body):
    def __init__(self, _):
        super().__init__("internal.empty", {})
