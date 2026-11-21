from abc import ABC
from collections.abc import Callable
from enum import Enum
from typing import TypedDict

ResponseWriter = Callable[["Body"], None]


class Method(Enum):
    CALL_FOR_RESPONSE = "call_for_response"
    CALL_FOR_RESPONSES = "call_for_responses"
    RESPONSE_CLOSE = "response close"
    RESPONSE = "response"


class Body(ABC):
    def __init__(self, msg_type: str, data: dict) -> None:
        self.type = msg_type
        self.data: dict = data

    def call_for_response(self, context: dict) -> "Body":
        """returns Body"""
        raise NotImplementedError(f"call_for_response not implemented for {self.type}")

    def call_for_responses(
        self, context: dict, response_writer: ResponseWriter
    ) -> None:
        raise NotImplementedError(f"call_for_responses not implemented for {self.type}")

    def get_type(self) -> None:
        return self.type


class Msg(TypedDict):
    type: str
    method: str
    call: int
    body: dict


class EmptyMsg(Body):
    def __init__(self, data: dict) -> None:
        super().__init__("internal.empty", {})
