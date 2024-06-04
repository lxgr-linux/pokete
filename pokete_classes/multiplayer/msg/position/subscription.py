import bs_rpc


class SubscribePosition(bs_rpc.Body):
    def __init__(self, data):
        super().__init__("pokete.position.subscribe", {})
