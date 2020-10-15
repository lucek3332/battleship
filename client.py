import pygame
from board import Board
from ship import Ship
from network import Network


pygame.init()

# Images
icon = pygame.image.load("images/icon.png")

# Music / sounds
pygame.mixer.music.load("sounds/music.wav")
pygame.mixer.music.play(-1)
play_sound = pygame.mixer.Sound("sounds/yessir.wav")
hitted_sound = pygame.mixer.Sound("sounds/canon.wav")
winner_sound = pygame.mixer.Sound("sounds/winner.wav")
lost_sound = pygame.mixer.Sound("sounds/lost.wav")

# General display settings
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

# Helper drawing functions for each game status
def redrawWindowSetting(win, my_board, ships, buttons, wins, loses):
    win.fill((162, 213, 252))
    font = pygame.font.SysFont("Arial", 40)
    txt = font.render("SETT UP YOUR SHIPS", True, (0, 0, 0), True)
    win.blit(txt, (80, 50))
    font2 = pygame.font.SysFont("Arial", 30)
    txt2 = font2.render("For setting up the ship on the board, click on", True, (0, 0, 0))
    txt3 = font2.render("the ship, drag in correct place and click again.", True, (0, 0, 0))
    txt4 = font2.render("For rotating the ship use SPACE. When you", True, (0, 0, 0))
    txt5 = font2.render("will have sett up all ships hit the PLAY button.", True, (0, 0, 0))
    txt6 = font2.render("If you made some mistake, hit the RESET", True, (0, 0, 0))
    txt7 = font2.render("button.", True, (0, 0, 0))
    win.blit(txt2, (470, 100))
    win.blit(txt3, (470, 160))
    win.blit(txt4, (470, 220))
    win.blit(txt5, (470, 280))
    win.blit(txt6, (470, 340))
    win.blit(txt7, (470, 400))
    my_board.draw(win)
    for ship in ships:
        ship.draw(win)
    for button in buttons:
        button.draw(win)
    score = font2.render("W: {} / L: {}".format(wins, loses), True, (0, 0, 0), True)
    win.blit(score, (820, 720))
    pygame.display.update()


def redrawWindowDisconnected(win):
    win.fill((162, 213, 252))
    font = pygame.font.SysFont("Arial", 60)
    txt = font.render("OPPONENT HAS DISCONNECTED", True, (255, 0, 0), True)
    win.blit(txt, (round(win.get_width()/2 - txt.get_width()/2), round(win.get_height()/2 - txt.get_height()/2)))
    pygame.display.update()


def redrawWindowWinner(win, game, playerID):
    win.fill((162, 213, 252))
    font = pygame.font.SysFont("Arial", 60)
    if game.winner == playerID:
        txt = font.render("YOU WIN!", True, (255, 0, 0), True)
        win.blit(txt, (round(win.get_width()/2 - txt.get_width()/2), round(win.get_height()/2 - txt.get_height()/2)))
    else:
        txt = font.render("YOU LOST...", True, (0, 0, 0), True)
        win.blit(txt, (round(win.get_width()/2 - txt.get_width()/2), round(win.get_height()/2 - txt.get_height()/2)))
    pygame.display.update()


def redrawWindowWaiting(win, my_board, ships, wins, loses):
    win.fill((162, 213, 252))
    font = pygame.font.SysFont("Arial", 60)
    txt = font.render("WAITING FOR", True, (0, 0, 0), True)
    txt2 = font.render("OTHER PLAYER", True, (0, 0, 0), True)
    font2 = pygame.font.SysFont("Arial", 30)
    win.blit(txt, (540, 200))
    win.blit(txt2, (520, 300))
    my_board.draw(win)
    for ship in ships:
        ship.draw(win)
    score = font2.render("W: {} / L: {}".format(wins, loses), True, (0, 0, 0), True)
    win.blit(score, (820, 720))
    pygame.display.update()


def redrawWindowPlaying(win, my_board, enemy_board, ships, playerID, game, ships_count, wins, loses):
    win.fill((162, 213, 252))
    enemy_board.draw(win)
    my_board.draw(win)
    font = pygame.font.SysFont("Arial", 30)
    if playerID == game.turn:
        txt = font.render("YOUR TURN", True, (255, 0, 0), True)
        win.blit(txt, (670, 50))
    else:
        txt = font.render("OPPONENT TURN", True, (0, 0, 0), True)
        win.blit(txt, (140, 50))
    for ship in ships:
        ship.draw(win)
    score = font.render("W: {} / L: {}".format(wins, loses), True, (0, 0, 0), True)
    ships_counter = font.render("Ships: {} / 20".format(ships_count), True, (0, 0, 0), True)
    win.blit(score, (820, 720))
    win.blit(ships_counter, (820, 660))
    pygame.display.update()

# Main game loop
def main():
    run = True
    b = Board()
    ships = [Ship(4, 50, 530), Ship(3, 50, 590), Ship(3, 200, 590), Ship(2, 50, 650), Ship(2, 150, 650), Ship(2, 250, 650), Ship(1, 50, 710), Ship(1, 110, 710), Ship(1, 170, 710), Ship(1, 230, 710)]
    reset_btn = Button("RESET", 350, 520, 100, 40, (194, 8, 23))
    play_btn = Button("PLAY", 350, 580, 100, 40, (6, 122, 16))
    ships_count = 0
    wins = 0
    loses = 0
    status_game = "setting up"
    while run:
        # Setting up your ships
        if status_game == 'setting up':
            redrawWindowSetting(screen, b, ships, Button.buttons, wins, loses)
            for event in pygame.event.get():
                # Quit game
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                # Reset ships
                if event.type == pygame.MOUSEBUTTONUP and reset_btn.click():
                    b.reset_board(ships)
                # Ready to play
                if event.type == pygame.MOUSEBUTTONUP and play_btn.click() and b.is_ready():
                    status_game = "connecting"
                    play_sound.play()
                    pygame.time.delay(100)
                # Drag, rotate ships
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
        # Connecting to server
        elif status_game == "connecting":
            n = Network()
            status_game = "waiting"
        # Waiting for another player
        elif status_game == "waiting":
            # Sending board, receiving game
            game = n.send(b)
            redrawWindowWaiting(screen, b, ships, wins, loses)
            for event in pygame.event.get():
                # Quit game
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
            # Another player has connected
            if game.both_connected:
                status_game = "playing"
        # Main part - gameplay
        elif status_game == "playing":
            # Checking another player disconnection, if so start new game and reset board
            if not game.both_connected:
                status_game = "player disconnected"
                b.reset_board(ships)
                continue
            # Getting game with actual boards from server
            game = n.send("get game")
            if n.id == "0":
                b = game.boards[0]
                b2 = game.boards[1]
            else:
                b = game.boards[1]
                b2 = game.boards[0]
            b.x = 50
            b.y = 100
            b2.x = 550
            b2.y = 100

            # Checking win condition
            if game.is_winner():
                status_game = "winner"

            redrawWindowPlaying(screen, b, b2, ships, n.id, game, ships_count, wins, loses)

            for event in pygame.event.get():
                # Quit game
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                # Shooting
                if event.type == pygame.MOUSEBUTTONUP and game.turn == n.id:
                    for row in b2.fields:
                        for field in row:
                            if field.click():
                                if field.ship:
                                    b2.looking_ship(field.row, field.col)
                                    n.send(("hitted", b2))
                                    hitted_sound.play()
                                    ships_count += 1
                                    if ships_count > 19:
                                        ships_count = 0
                                else:
                                    n.send(("missed", b2))
        # End of game - reset board, closing socket
        elif status_game == "winner":
            redrawWindowWinner(screen, game, n.id)
            if n.id == game.winner:
                wins += 1
                winner_sound.play()
            else:
                loses += 1
                lost_sound.play()
            pygame.time.delay(2000)
            status_game = "setting up"
            b.reset_board(ships)
            n.close()
        # Another player has disconnected - start new game, reset board, closing socket
        elif status_game == "player disconnected":
            redrawWindowDisconnected(screen)
            pygame.time.delay(2000)
            n.close()
            status_game = "setting up"


main()
