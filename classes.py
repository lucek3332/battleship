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
        self.sinked = False

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)
        pygame.draw.rect(win, self.border_color, self.rect, 1)
        if self.sinked:
            pygame.draw.line(win, self.lines_color, (self.x, self.y), (self.x + self.width, self.y + self.height))
            pygame.draw.line(win, self.lines_color, (self.x, self.y + self.height), (self.x + self.width, self.y))
        elif self.hitted:
            pygame.draw.circle(win, self.circle_color, (round(self.x + self.width/2), round(self.y + self.height/2)), 5)

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


class Ship:
    width = 40
    height = 40
    image = pygame.image.load("images/ship.png")

    def __init__(self, mast, x, y):
        self.x = x
        self.y = y
        self.mast = mast
        self.rect = (self.x, self.y, self.mast * self.width, self.height)
        self.draging = False

    def draw(self, win):
        for i in range(self.mast):
            win.blit(self.image, (self.x + i * self.width, self.y))
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
        self.rect = (self.x, self.y, self.mast * self.width, self.height)

    def drop(self):
        pos = pygame.mouse.get_pos()

