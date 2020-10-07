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


def redrawWindow(win, my_board, enemy_board, ships):
    win.fill((162, 213, 252))
    my_board.draw(win)
    enemy_board.draw(win)
    for ship in ships:
        ship.draw(win)
    pygame.display.update()

def main():
    run = True
    b = Board()
    b2 = Board(550, 100)
    ships = [Ship(4, 500, 600), Ship(3, 500, 660)]
    while run:
        redrawWindow(screen, b, b2, ships)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONUP:
                for row in b.fields:
                    for field in row:
                        if field.active and field.click():
                            print("hitted")
            for ship in ships:
                if event.type == pygame.MOUSEBUTTONUP and ship.click():
                    ship.draging = not ship.draging
                elif event.type == pygame.MOUSEMOTION and ship.draging == True:
                    ship.drag()


main()
