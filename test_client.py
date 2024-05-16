import socket
import threading

import bs_rpc


class TestRequestMsg(bs_rpc.Body):
    def __init__(self, data):
        super().__init__("test.request", data)


class TestResponseMsg(bs_rpc.Body):
    def __init__(self, data):
        super().__init__("test.response", data)


reg = bs_rpc.Registry()
reg.register(TestRequestMsg)
reg.register(TestResponseMsg)

con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
con.connect(("localhost", 9988))

client = bs_rpc.Client(con, reg)

listen = threading.Thread(
    target=lambda: client.listen({}),
    daemon=True)

listen.start()

print(client.call_for_response(
    TestRequestMsg({"Field1": "hmm", "Field2": "jaja"})).data)

print(client.call_for_response(
    TestRequestMsg({"Field1": "hmm", "Field2": "dock"})).data)
