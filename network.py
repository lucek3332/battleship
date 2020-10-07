import socket

class Network():
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.0.220"
        self.port = 5555
        self.addres = (self.server, self.port)
        self.id = self.connect()
        print(self.id)

    def connect(self):
        try:
            self.client.connect(self.addres)
            return self.client.recv(2048).decode()
        except:
            pass

    def send(self, data):
        self.client.send(str.encode(data))
        return self.client.recv(2048).decode()
