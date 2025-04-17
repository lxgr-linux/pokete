from .msg import EmptyMsg


class NotRegistredException(Exception):
    pass


class AlreadyRegistredException(Exception):
    pass


class Registry:
    def __init__(self):
        self.reg = {}
        self.register(EmptyMsg)

    def register(self, body_class) -> None:
        t = body_class({}).get_type()
        if t not in self.reg:
            self.reg[t] = body_class
        else:
            raise AlreadyRegistredException(
                f"Handler for `{t}` is already registered")

    def get(self, msg_type: str):
        if (type_class := self.reg.get(msg_type, None)) is None:
            raise NotRegistredException(
                f"Not handler is registered for `{msg_type}`")
        return type_class
