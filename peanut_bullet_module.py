import pygame
import sys
import random
import time
import data_module


class Bullet:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        

    def shoot(self):
        self.x = pygame.mouse.get_pos()[0]
        self.y = pygame.mouse.get_pos()[1]
        peanut = pygame.image.load("Peanut_bullet.png")
        self.screen.blit(peanut, (self.x, self.y))
    
    def draw_crosshairs(self):
        self.x = pygame.mouse.get_pos()[0]
        self.y = pygame.mouse.get_pos()[1]
        crosshair_width = 2
        crosshair_height = 30
        pygame.draw.rect(self.screen, pygame.Color("black"), (self.x - crosshair_width / 2, self.y - crosshair_height / 2, crosshair_width, crosshair_height))
        pygame.draw.rect(self.screen, pygame.Color("black"), (self.x - crosshair_height / 2, self.y - crosshair_width / 2, crosshair_height, crosshair_width))




def main():
    pygame.init()
    pygame.display.set_caption("Cool Project")
    screen = pygame.display.set_mode((1300, 800))
    clock = pygame.time.Clock()
    mouse = data_module.MousePosition(screen)
    bullet = Bullet(screen)

    while True:
        clock.tick(20)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if mouse.is_clicked(event.pos):
                    bullet.shoot()
            
    
        screen.fill((255, 255, 255))
        bullet.draw_crosshairs()
        pygame.display.update()


if __name__ == "__main__":
    main()
