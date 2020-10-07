import pygame
from classes import Board

pygame.init()

# Images
icon = pygame.image.load("images/icon.png")

screenWidth = 1000
screenHeight = 800
pygame.display.set_icon(icon)
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Battleship - online game")


def redrawWindow(win, my_board, enemy_board):
    win.fill((162, 213, 252))
    my_board.draw(win)
    enemy_board.draw(win)
    pygame.display.update()

def main():
    run = True
    b = Board()
    b2 = Board(550, 100)
    while run:
        redrawWindow(screen, b, b2)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONUP:
                for row in b.fields:
                    for field in row:
                        if field.active and field.click():
                            print("hitted")

main()
