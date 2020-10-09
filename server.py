import socket
from _thread import start_new_thread
from game import Game
from board import Board
import pickle


server = "192.168.0.220"  # For test connection write your local IP address here
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
    print("Server started, waiting for connections")
except socket.error as e:
    print(e)


def threaded_client(conn, player, gameID):
    conn.send(str.encode(str(player)))
    game = games[gameID]
    while True:
        try:
            data = pickle.loads(conn.recv(4096*32))
            if isinstance(data, Board):
                if not game.ready_to_play():
                    game.boards[player] = data
                    if player == 0:
                        reply = game.boards[1]
                    else:
                        reply = game.boards[0]
                else:
                    if player == 0:
                        game.boards[1] = data
                    else:
                        game.boards[0] = data
                    reply = game.boards[player]
            else:
                if data == "ready":
                    if player == 0:
                        game.p1ships = True
                    else:
                        game.p2ships = True
                reply = game
            if not data:
                print("Disconnected")
                break
            conn.sendall(pickle.dumps(reply))
        except Exception as e:
            print("bład")
            print(e)
            break
    print("Closing connection")
    conn.close()


s.listen()
currentPlayer = 0
games = {}
gameID = 0

while True:
    conn, addr = s.accept()
    print("Connected to {}".format(addr))
    p = 0
    gameID = currentPlayer // 2
    if currentPlayer % 2 == 0:
        games[gameID] = Game(gameID)
        print("Creating new game: {}".format(gameID))
    else:
        games[gameID].is_ready = True
        p = 1
    start_new_thread(threaded_client, (conn, p, gameID))
    currentPlayer += 1