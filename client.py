import pygame
from classes import Board, Ship

pygame.init()

# Images
icon = pygame.image.load("images/icon.png")

screenWidth = 1000
screenHeight = 800
pygame.display.set_icon(icon)
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Battleship - online game")


class Button:
    color_bg = (255, 0, 0)
    color_txt = (255, 255, 255)

    def __init__(self, text, x, y, width, height):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, win):
        pygame.draw.rect(win, self.color_bg, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("comicsans", 30)
        txt = font.render(self.text, True, self.color_txt)
        win.blit(txt, (round(self.x + self.width/2 - txt.get_width()/2), round(self.y + self.height/2 - txt.get_height()/2)))

    def click(self):
        pos = pygame.mouse.get_pos()
        if self.x <= pos[0] <= self.x + self.width:
            if self.y <= pos[1] <= self.y + self.height:
                return True
        return False


def redrawWindow(win, my_board, enemy_board, ships, buttons):
    win.fill((162, 213, 252))
    my_board.draw(win)
    enemy_board.draw(win)
    for ship in ships:
        ship.draw(win)
    for button in buttons:
        button.draw(win)
    pygame.display.update()


def main():
    buttons = []
    run = True
    b = Board()
    b2 = Board(550, 100)
    ships = [Ship(4, 100, 530), Ship(3, 100, 590), Ship(3, 250, 590), Ship(2, 100, 650), Ship(2, 200, 650), Ship(2, 300, 650), Ship(1, 100, 710), Ship(1, 160, 710), Ship(1, 220, 710), Ship(1, 280, 710)]
    reset_btn = Button("RESET", 350, 520, 100, 40)
    buttons.append(reset_btn)
    while run:
        redrawWindow(screen, b, b2, ships, buttons)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONUP:
                for row in b.fields:
                    for field in row:
                        if field.active and field.click():
                            print("hitted")
            if event.type == pygame.MOUSEBUTTONUP and reset_btn.click():
                b.reset_board(ships)
            for ship in ships:
                if event.type == pygame.MOUSEBUTTONUP and ship.click() and not ship.placed:
                    if ship.draging:
                        ship.drop(b)
                    ship.draging = not ship.draging
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and ship.draging is True:
                        ship.rotate()
                elif event.type == pygame.MOUSEMOTION and ship.draging is True:
                    ship.drag()



main()
