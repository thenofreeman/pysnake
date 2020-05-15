# main.py

import pygame
pygame.init()
from game import Game
from window import Window

window = Window(pygame)

ENTITY_SIZE = 20

running = True

game = Game(window)

# Main Game Loop
while running:
    # in milliseconds TODO replace with clock
    pygame.time.delay(100)

    game.update()
    game.draw()

    pygame.display.update()
# If loop is broken; quit game and close window
pygame.quit()
