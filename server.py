import socket
from _thread import start_new_thread

server = "192.168.0.220" # For test connection write your local IP address here
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
    print("Server started, waiting for connections")
except socket.error as e:
    print(e)

def threaded_client(conn, player):
    conn.send(str.encode("Connected"))
    reply = ""
    while True:
        try:
            data = conn.recv(2048).decode("utf-8")
            reply = data
            if not data:
                print("Disconnected")
                break
            else:
                print("Receiving: {}".format(data))
                print("Sending: {}".format(reply))
            conn.sendall(str.encode(reply))
        except:
            break
    print("Closing connection")
    conn.close()

s.listen(2)
currentPlayer = 0

while True:
    conn, addr = s.accept()
    print("Connected to {}".format(addr))
    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1