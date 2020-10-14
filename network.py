import socket
import pickle

HEADERSIZE = 20


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.0.220"
        self.port = 5555
        self.address = (self.server, self.port)
        self.id = self.connect()
        print(self.id)

    def connect(self):
        try:
            self.client.connect(self.address)
            return self.client.recv(2048).decode()
        except:
            pass

    def send(self, data):
        # Sending
        data_bytes = pickle.dumps(data)
        header = "{0:<20}".format(len(data_bytes))
        data = bytes(header, "utf-8") + data_bytes
        self.client.send(data)
        # Receiving
        data_bytes = b""
        new_data = True
        while True:
            if new_data:
                data_len = int(self.client.recv(20))
                new_data = False
            else:
                packet = self.client.recv(1024)
                data_bytes += packet
                if len(data_bytes) == data_len:
                    break
        return pickle.loads(data_bytes)
