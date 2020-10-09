from field import Field


class Board:
    x_axis = list(range(10))
    y_axis = list(range(10))

    def __init__(self, x=50, y=100):
        self.x = x
        self.y = y
        self.fields = [[Field(i, j, self.x, self.y) for i in self.x_axis] for j in self.y_axis]
        self.is_active = False

    def draw(self, win):
        self.update()
        for row in self.fields:
            for field in row:
                field.draw(win)

    def update(self):
        for row in self.fields:
            for field in row:
                field.x = self.x + field.col * field.width
                field.y = self.y + field.row * field.width
                field.rect = (field.x, field.y, field.width, field.height)

    def reset_board(self, ships):
        for row in self.fields:
            for field in row:
                field.ship = False
                field.shipAvaiable = True
        for ship in ships:
            ship.reset()

    def is_ready(self):
        ship_count = sum(1 if f.ship else 0 for row in self.fields for f in row)
        if ship_count == 20:
            return True
        return False

    def __repr__(self):
        return "Board x: {} y: {}".format(self.x, self.y)
