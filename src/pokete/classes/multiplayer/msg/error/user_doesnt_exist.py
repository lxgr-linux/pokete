import pokete.bs_rpc as bs_rpc

USER_DOESNT_EXIST_TYPE = "pokete.error.user_doesnt_exist"


class UserDoesntExist(bs_rpc.Body):
    def __init__(self, data):
        super().__init__(USER_DOESNT_EXIST_TYPE, {})
