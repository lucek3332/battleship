import pygame


class Game:
    def __init__(self, pk):
        self.id = pk


class Field:
    width = 40
    height = 40
    border_color = (0, 0, 0)
    lines_color = (255, 0, 0)
    color = (255, 255, 255)
    circle_color = (0, 0, 0)

    def __init__(self, col, row, start_x, start_y):
        self.col = col
        self.row = row
        self.start_x = start_x
        self.start_y = start_y
        self.x = self.start_x + self.col * self.width
        self.y = self.start_y + self.row * self.width
        self.rect = (self.x, self.y, self.width, self.height)
        self.active = True
        self.hitted = False
        self.ship = False
        self.shipAvaiable = True
        self.sinked = False

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)
        pygame.draw.rect(win, self.border_color, self.rect, 1)
        if self.sinked:
            pygame.draw.line(win, self.lines_color, (self.x, self.y), (self.x + self.width, self.y + self.height))
            pygame.draw.line(win, self.lines_color, (self.x, self.y + self.height), (self.x + self.width, self.y))
        elif self.hitted:
            pygame.draw.circle(win, self.circle_color, (round(self.x + self.width/2), round(self.y + self.height/2)), 5)
        if not self.shipAvaiable:
            pygame.draw.rect(win, (0, 255, 0), self.rect)

    def click(self):
        pos = pygame.mouse.get_pos()
        if self.x <= pos[0] <= self.x + self.width and self.active:
            if self.y <= pos[1] <= self.y + self.height:
                if self.ship:
                    self.sinked = True
                else:
                    self.hitted = True
                self.active = False
                return True
        return False

    def isShipPoss(self, ship):
        if ship.position == "horizontal":
            if self.col + ship.mast <= 10:
                return True
            return False
        else:
            if self.row + ship.mast <= 10:
                return True
            return False

    def __repr__(self):
        return "Field ({}, {})".format(self.col, self.row)


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

    # add to Ship class later, remove from Board, algorithm need to be improved
    def surrounding_ship_fields(self, field, ship):
        ship.surrounding = []
        if ship.position == "horizontal":
            if field.row == 0:
                if field.col == 0:
                    fields = [(r, c) for c in range(ship.mast + 1) for r in range(field.row + 2)]
                elif field.col + ship.mast == 10:
                    fields = [(r, c) for c in range(field.col - 1, 10) for r in range(field.row + 2)]
                else:
                    fields = [(r, c) for c in range(field.col - 1, field.col + ship.mast + 1) for r in range(field.row + 2)]
            elif field.row == 9:
                if field.col == 0:
                    fields = [(r, c) for c in range(ship.mast + 1) for r in range(8, 10)]
                elif field.col + ship.mast == 10:
                    fields = [(r, c) for c in range(field.col - 1, 10) for r in range(8, 10)]
                else:
                    fields = [(r, c) for c in range(field.col - 1, field.col + ship.mast + 1) for r in range(8, 10)]
            elif field.col == 0:
                fields = [(r, c) for c in range(ship.mast + 1) for r in range(field.row - 1, field.row + 2)]
            elif field.col + ship.mast == 10:
                fields = [(r, c) for c in range(field.col - 1, 10) for r in range(field.row - 1, field.row + 2)]
            else:
                fields = [(r, c) for c in range(field.col - 1, field.col + ship.mast + 1) for r in range(field.row - 1, field.row + 2)]

        else:
            if field.row == 0:
                if field.col == 0:
                    fields = [(r, c) for c in range(2) for r in range(ship.mast + 1)]
                elif field.col == 9:
                    fields = [(r, c) for c in range(8, 10) for r in range(ship.mast + 1)]
                else:
                    fields = [(r, c) for c in range(field.col - 1, field.col + 2) for r in range(ship.mast + 1)]
            elif field.row + ship.mast == 10:
                if field.col == 0:
                    fields = [(r, c) for c in range(2) for r in range(field.row - 1, 10)]
                elif field.col == 9:
                    fields = [(r, c) for c in range(8, 10) for r in range(field.row - 1, 10)]
                else:
                    fields = [(r, c) for c in range(field.col - 1, field.col + 2) for r in range(field.row - 1, 10)]
            elif field.col == 0:
                fields = [(r, c) for c in range(2) for r in range(field.row - 1, field.row + ship.mast + 1)]
            elif field.col == 9:
                fields = [(r, c) for c in range(8, 10) for r in range(field.row - 1, field.row + ship.mast + 1)]
            else:
                fields = [(r, c) for c in range(field.col - 1, field.col + 2) for r in range(field.row - 1, field.row + ship.mast + 1)]

        ship.surrounding = fields

    # add to Ship class later, remove from Board
    def ship_fields(self, field, ship):
        ship.fields = []
        if ship.position == "horizontal":
            fields = [(field.row, c) for c in range(field.col, field.col + ship.mast)]
        else:
            fields = [(r, field.col) for r in range(field.row, field.row + ship.mast)]
        ship.fields = fields


class Ship:
    width = 40
    height = 40
    image = pygame.image.load("images/ship.png")

    def __init__(self, mast, x, y):
        self.x = x
        self.y = y
        self.start_x = x
        self.start_y = y
        self.mast = mast
        self.rect = (self.x, self.y, self.mast * self.width, self.height)
        self.draging = False
        self.position = "horizontal"
        self.placed = False
        self.fields = []
        self.surrounding = []
        self.sinked = False

    def draw(self, win):
        if self.position == "horizontal":
            for i in range(self.mast):
                win.blit(self.image, (self.x + i * self.width, self.y))
        else:
            for i in range(self.mast):
                win.blit(self.image, (self.x, self.y + i * self.height))
        pygame.draw.rect(win, (255, 0, 0), self.rect, 4)

    def click(self):
        pos = pygame.mouse.get_pos()
        if self.x <= pos[0] <= self.x + (self.width * self.mast):
            if self.y <= pos[1] <= self.y + self.height:
                return True
        return False

    def drag(self):
        pos = pygame.mouse.get_pos()
        self.x = pos[0]
        self.y = pos[1]
        self.update()

    def reset(self):
        self.x = self.start_x
        self.y = self.start_y
        self.position = "horizontal"
        self.surrounding = []
        self.update()

    def drop(self, board):
        for row in board.fields:
            for field in row:
                if field.x <= self.x <= field.x + field.width:
                    if field.y <= self.y <= field.y + field.height:
                        if field.isShipPoss(self):
                            board.surrounding_ship_fields(field, self)
                            board.ship_fields(field, self)
                            for f in self.fields:
                                if not board.fields[f[0]][f[1]].shipAvaiable:
                                    self.reset()
                                    return False
                            for f in self.surrounding:
                                if board.fields[f[0]][f[1]].ship:
                                    self.reset()
                                    return False
                            for f in self.fields:
                                board.fields[f[0]][f[1]].ship = True
                            for f in self.surrounding:
                                board.fields[f[0]][f[1]].shipAvaiable = False
                            self.x = field.x
                            self.y = field.y
                            self.placed = True
                            self.update()
                            return True

        self.reset()
        return False

    def update(self):
        if self.position == "horizontal":
            self.rect = (self.x, self.y, self.mast * self.width, self.height)
        else:
            self.rect = (self.x, self.y, self.width, self.mast * self.height)

    def rotate(self):
        if self.position == "horizontal":
            self.position = "vertical"
        else:
            self.position = "horizontal"
        self.update()
