import pygame
import sys
import random
import time



class Bullet:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        

    def draw(self):
        self.screen.blit()
       

def main():
    pygame.init()
    pygame.display.set_caption("Cool Project")
    screen = pygame.display.set_mode((1300, 800))
    clock = pygame.time.Clock()

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

    
        screen.fill((255, 255, 255))
        
        pygame.display.update()


if __name__ == "__main__":
    main()
