from field import Field


class Board:
    x_axis = list(range(10))
    y_axis = list(range(10))

    def __init__(self, x=50, y=100):
        self.x = x
        self.y = y
        self.fields = [[Field(i, j, self.x, self.y) for i in self.x_axis] for j in self.y_axis]

    def draw(self, win):
        for row in self.fields:
            for field in row:
                field.draw(win)

    def reset_board(self, ships):
        for row in self.fields:
            for field in row:
                field.ship = False
                field.shipAvaiable = True
        for ship in ships:
            ship.reset()
