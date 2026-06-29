import pygame
import sys
import random
import time
from peanut_bullet_module import Bullet
from my_character import MainC
from zombie_module import Zombie

def main():
    pygame.init()
    pygame.display.set_caption("peanut apocolypse")
    screen = pygame.display.set_mode((1300, 800))

    player = MainC(screen, 100, 100, "Character_Placeholder.png")
    zombie = Zombie(screen, 600, 300, "ZombieFIXED.png")

    clock = pygame.time.Clock()

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            
            if event.type == pygame.MOUSEBUTTONDOWN:
                player.fire()

        pressed_keys = pygame.key.get_pressed()

        ############################# Player Movement ###############################
        if pressed_keys[pygame.K_w]:
            player.y -= 5
        if pressed_keys[pygame.K_s]:
            player.y += 5
        if pressed_keys[pygame.K_a]:
            player.x -= 5
        if pressed_keys[pygame.K_d]:
            player.x += 5
        
        ############################################################################
        player.mouse_x, player.mouse_y = pygame.mouse.get_pos()
        player.update_angle()
        
        zombie.follow_player(player)
        zombie.update_angle(player)

        screen.fill((255, 255, 255))
        for bullet in player.bullets:
            bullet.move()
            bullet.draw()

        player.draw()
        zombie.draw()

        pygame.display.update()

main()