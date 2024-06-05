import bs_rpc

SUBSCRIBE_POSITION_TYPE = "pokete.position.subscribe"


class SubscribePosition(bs_rpc.Body):
    def __init__(self, data):
        super().__init__(SUBSCRIBE_POSITION_TYPE, {})
