import socket
import threading

import bs_rpc


class TestStreamMsg(bs_rpc.Body):
    def __init__(self, data):
        super().__init__("test.stream", data)


class TestRequestMsg(bs_rpc.Body):
    def __init__(self, data):
        super().__init__("test.request", data)


class TestResponseMsg(bs_rpc.Body):
    def __init__(self, data):
        super().__init__("test.response", data)


reg = bs_rpc.Registry()
reg.register(TestRequestMsg)
reg.register(TestResponseMsg)
reg.register(TestStreamMsg)

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

for resp in client.call_for_responses(TestStreamMsg({"Start": 7}))():
    print(resp.data)
