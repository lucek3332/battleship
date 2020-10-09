import pygame
from board import Board
from ship import Ship
from network import Network

pygame.init()

# Images
icon = pygame.image.load("images/icon.png")

screenWidth = 1000
screenHeight = 800
pygame.display.set_icon(icon)
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Battleship - online game")


class Button:
    buttons = []
    color_txt = (255, 255, 255)

    def __init__(self, text, x, y, width, height, color_bg):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color_bg = color_bg
        Button.buttons.append(self)

    def draw(self, win):
        pygame.draw.rect(win, self.color_bg, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("Arial", 22, True)
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
    font = pygame.font.SysFont("Arial", 40)
    txt = font.render("MY BOARD", True, (255, 255, 255), True)
    win.blit(txt, (180, 50))
    my_board.draw(win)
    enemy_board.draw(win)
    for ship in ships:
        ship.draw(win)
    for button in buttons:
        button.draw(win)
    pygame.display.update()

def redrawWindowGame(win, my_board, enemy_board, ships):
    win.fill((162, 213, 252))
    font = pygame.font.SysFont("Arial", 40)
    txt = font.render("MY BOARD", True, (255, 255, 255), True)
    win.blit(txt, (180, 50))
    my_board.draw(win)
    enemy_board.draw(win)
    for ship in ships:
        ship.draw(win)
    pygame.display.update()


def main():
    run = True
    n = Network()
    b = Board()
    ships = [Ship(4, 50, 530), Ship(3, 50, 590), Ship(3, 200, 590), Ship(2, 50, 650), Ship(2, 150, 650), Ship(2, 250, 650), Ship(1, 50, 710), Ship(1, 110, 710), Ship(1, 170, 710), Ship(1, 230, 710)]
    reset_btn = Button("RESET", 350, 520, 100, 40, (194, 8, 23))
    confirm_btn = Button("CONFIRM", 350, 580, 100, 40, (6, 122, 16))
    status_game = "menu"
    game = None
    while run:
        if not game:
            b2 = n.send(b)
            b2.x = 550
            b2.y = 100
            redrawWindow(screen, b, b2, ships, Button.buttons)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONUP and reset_btn.click() and not game:
                    b.reset_board(ships)
                if event.type == pygame.MOUSEBUTTONUP and confirm_btn.click() and b.is_ready() and not game:
                    game = n.send("ready")
                    b2.is_active = True
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
        elif not game.ready_to_play():
            b2 = n.send(b)
            game = n.send("get_game")
            b2.x = 550
            b2.y = 100
            redrawWindowGame(screen, b, b2, ships)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
        elif game.ready_to_play():
            b = n.send(b2)
            b.x = 50
            b.y = 100
            redrawWindowGame(screen, b, b2, ships)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONUP and b2.is_active:
                    for row in b2.fields:
                        for field in row:
                            if field.active and field.click():
                                print("hitted")
        print(game)
        if game is not None:
            print(game.ready_to_play())


main()
