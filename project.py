import pygame
import sys
import random
import time
from my_character import MainC
from zombie_module import Zombie

def main():
    # turn on pygame
    pygame.init()
    pygame.display.set_caption("peanut apocolypse")
    screen = pygame.display.set_mode((1300, 800))
    # creates a Character from the my_character.py file
    player = MainC(screen, 100, 100, "Character_Placeholder.png")
    zombie = Zombie(screen, 600, 300, "ZombieFIXED.png")

    # let's set the framerate
    clock = pygame.time.Clock()
    while True:
        clock.tick(60)  # this sets the framerate of your game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        pressed_keys = pygame.key.get_pressed()
#############################Player Movement###############################
        if pressed_keys[pygame.K_w]:
            player.y -= 5
        if pressed_keys[pygame.K_s]:
            player.y += 5
        if pressed_keys[pygame.K_a]:
            player.x -= 5
        if pressed_keys[pygame.K_d]:
            player.x += 5
        player.update_angle()
############################################################################
        zombie.follow_player(player)
        zombie.update_angle(player)


        # TODO: Fill the screen with whatever background color you like!
        screen.fill((255, 255, 255))

        # draws the character every frame
        player.draw()
        zombie.draw()

        # TODO: Add your project code

        # don't forget the update, otherwise nothing will show up!
        pygame.display.update()

main()