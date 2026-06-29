import pygame
import sys
import random
import time



class Map:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.red_r = pygame.image.load("RoseHulmanRedR.png")
        self.red_r = pygame.transform.scale(self.red_r, (630, 758))
        self.grey_r = pygame.transform.grayscale(self.red_r)
    
    def draw(self):
        self.screen.blit(self.grey_r, (self.screen.get_width() / 2 - self.grey_r.get_width() / 2, self.screen.get_height() / 2 - self.grey_r.get_height() / 2))

class Rooms:
    def __init__(self,screen: pygame.Surface):
        self.screen = screen
        self.room_1 = pygame.image.load("room1.png")
        self.room_1 = pygame.transform.scale(self.room_1, (630, 758))

    def draw(self):
        self.screen.blit(self.room_1,(self.screen.get_width() / 2 - self.room_1.get_width() / 2, self.screen.get_height() / 2 - self.room_1.get_height() / 2))

def main():
    pygame.init()
    pygame.display.set_caption("Cool Project")
    screen = pygame.display.set_mode((1300, 800))
    big_r = Map(screen)
    clock = pygame.time.Clock()
    mapped_room_1 = Rooms(screen)

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        


    
        screen.fill((255, 255, 255))
        big_r.draw()
        mapped_room_1.draw()
        pygame.display.update()


if __name__ == "__main__":
    main()
