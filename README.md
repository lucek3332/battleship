# Battleship

## About game
Online game for 2 players written in Python/Pygame.
Server create game with 2 first, random players in queue.
Server can handle unlimited games at the same time.
Connection to server take place after setting up all ships.

## Requirements
You need Python with installed Pygame module to play this game.
Then you need to change IP address for server to your local machine IP address in server.py and network.py files.
Run server.py first, then client.py. Enjoy game!

## Controls
### Setting up ships
For setting up the ship on the board, click on the ship, drag in correct place and click again.
For rotating the ship use SPACE. When you will have sett up all ships hit the PLAY button.
If you made some mistake, hit the RESET button.

### Gameplay
According to player turn, player can shot to arbitrary fields by clicking them.
Unavailable fields for ship will be marked as hitted automatically.
If player sink entire ship, surrounding fields around ship wil be marked as hitted automatically.
Player turn is changing after missed shot.

## Winning
Player who sink all enemy ships, wins.

## Known bugs
Sometimes, when one player has disconnected, the other one gets disconnected too.