import bs_rpc


class UserExists(bs_rpc.Body):
    def __init__(self, data):
        super().__init__("pokete.error.user_exists", {})
