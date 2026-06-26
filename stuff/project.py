import pygame
import sys
import random
import time
from my_character import MainC

def main():
    # turn on pygame
    pygame.init()
    pygame.display.set_caption("Cool Project")
    screen = pygame.display.set_mode((1300, 800))
    # creates a Character from the my_character.py file
    character = MainC(screen, 100, 100, "Character_Placeholder.png")

    # let's set the framerate
    clock = pygame.time.Clock()
    while True:
        clock.tick(60)  # this sets the framerate of your game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            # TODO: Add you events code
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_w]:
            character.y -= 5
        if pressed_keys[pygame.K_s]:
            character.y += 5
        if pressed_keys[pygame.K_a]:
            character.x -= 5
        if pressed_keys[pygame.K_d]:
            character.x += 5
        character.update_angle()

        # TODO: Fill the screen with whatever background color you like!
        screen.fill((255, 255, 255))

        # draws the character every frame
        character.draw()

        # TODO: Add your project code

        # don't forget the update, otherwise nothing will show up!
        pygame.display.update()

main()