import pygame


pygame.init()

# Images
icon = pygame.image.load("images/icon.png")

screenWidth = 600
screenHeight = 800
pygame.display.set_icon(icon)
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Battleship - online game")





def redrawWindow(win):
    win.fill((11, 123, 191))
    pygame.display.update()

def main():
    run = True
    redrawWindow(screen)
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()


main()