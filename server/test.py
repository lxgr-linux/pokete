import socket, time, json, sys

HOST = "localhost"  # The server's hostname or IP address
PORT = 9988  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    response = {
            "Type": 1,
            "Body": {
                "UserName": sys.argv[1],
                "Version": "0.9.1"
            }
    }
    s.sendall(str.encode(json.dumps(response)))
    while True:
        data = s.recv(1048576)
        print(data)
        time.sleep(1)
        #print(f"Received {json.dumps(json.loads(data), indent=4)}")
        s.sendall(str.encode(json.dumps({
            "Type": 0,
            "Body": {
                "X": 4,
                "Y": 5,
            }
        })))
        s.sendall(str.encode(json.dumps({
            "Type": 0,
            "Body": {
                "X": 5,
                "Y": 5,
            }
        })))
        time.sleep(1)
