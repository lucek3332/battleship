import pygame


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
        # pygame.draw.rect(win, (255, 0, 0), self.rect, 4)

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
        self.placed = False
        self.fields = []
        self.surrounding = []
        self.update()

    def drop(self, board):
        for row in board.fields:
            for field in row:
                if field.x <= self.x <= field.x + field.width:
                    if field.y <= self.y <= field.y + field.height:
                        if field.isShipPoss(self):
                            self.surrounding_ship_fields(field)
                            self.ship_fields(field)
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

    def ship_fields(self, field):
        self.fields = []
        if self.position == "horizontal":
            fields = [(field.row, c) for c in range(field.col, field.col + self.mast)]
        else:
            fields = [(r, field.col) for r in range(field.row, field.row + self.mast)]
        self.fields = fields

    def surrounding_ship_fields(self, field):
        self.surrounding = []
        if self.position == "horizontal":
            fields = [(r, c) for c in range(field.col - 1, field.col + self.mast + 1 ) for r in range(field.row - 1, field.row + 2)]
            fields = [f for f in fields if (f[0] >= 0 and f[0] <= 9 and f[1] >= 0 and f[1] <= 9)]
        else:
            fields = [(r, c) for c in range(field.col - 1, field.col + 2) for r in range(field.row - 1, field.row + self.mast + 1)]
            fields = [f for f in fields if (f[0] >= 0 and f[0] <= 9 and f[1] >= 0 and f[1] <= 9)]
        self.surrounding = fields
