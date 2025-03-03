import pokete.bs_rpc as bs_rpc

USER_EXISTS_TYPE = "pokete.error.user_exists"


class UserExists(bs_rpc.Body):
    def __init__(self, data):
        super().__init__(USER_EXISTS_TYPE, {})
