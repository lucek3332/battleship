import pygame


class Game:
    def __init__(self):
        pass


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
            pygame.draw.line(win, self.lines_color, (self.x, self.y), (self.x + self.width, self.y + self.height) )
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
    def __init__(self):
        pass
