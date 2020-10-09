from board import Board


class Game:
    def __init__(self, pk):
        self.id = pk
        self.is_ready = False
        self.turn = "0"
        self.boards = [Board(), Board()]
        self.p1ships = False
        self.p2ships = False
        self.wins = [0, 0]

    def ready_to_play(self):
        if self.p1ships and self.p2ships:
            return True
        return False

    def __str__(self):
        return "Game {}".format(self.id)