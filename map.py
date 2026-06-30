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
#level_counter = 0
class Rooms:
    def __init__(self, screen: pygame.Surface, level_counter):
        self.level_counter = level_counter
        self.screen = screen
        self.room_1 = pygame.image.load("room1.png")
        self.room_1 = pygame.transform.scale(self.room_1, (630, 758))
        self.room_2 = pygame.image.load("room2.png")
        self.room_2 = pygame.transform.scale(self.room_2, (630, 758))
        self.room_3 = pygame.image.load("room3.png")
        self.room_3 = pygame.transform.scale(self.room_3, (630, 758))
        self.room_4 = pygame.image.load("room4.png")
        self.room_4 = pygame.transform.scale(self.room_4, (630, 758))
        self.room_5 = pygame.image.load("room5.png")
        self.room_5 = pygame.transform.scale(self.room_5, (630, 758))
        self.room_6 = pygame.image.load("room6.png")
        self.room_6 = pygame.transform.scale(self.room_6, (630, 758))
        self.room_7 = pygame.image.load("room7.png")
        self.room_7 = pygame.transform.scale(self.room_7, (630, 758))
        self.room_8 = pygame.image.load("room8.png")
        self.room_8 = pygame.transform.scale(self.room_8, (630, 758))
        self.room_9 = pygame.image.load("room9.png")
        self.room_9 = pygame.transform.scale(self.room_9, (630, 758))
        self.room_10 = pygame.image.load("room10.png")
        self.room_10 = pygame.transform.scale(self.room_10, (630, 758))

    def draw(self):
        if self.level_counter is 1:
            self.screen.blit(self.room_1,(self.screen.get_width() / 2 - self.room_1.get_width() / 2, self.screen.get_height() / 2 - self.room_1.get_height() / 2))
        if self.level_counter is 2:
            self.screen.blit(self.room_1,(self.screen.get_width() / 2 - self.room_1.get_width() / 2, self.screen.get_height() / 2 - self.room_1.get_height() / 2))
            self.screen.blit(self.room_2,(self.screen.get_width() / 2 - self.room_2.get_width() / 2, self.screen.get_height() / 2 - self.room_2.get_height() / 2))
        if self.level_counter is 3:
            self.screen.blit(self.room_1,(self.screen.get_width() / 2 - self.room_1.get_width() / 2, self.screen.get_height() / 2 - self.room_1.get_height() / 2))
            self.screen.blit(self.room_2,(self.screen.get_width() / 2 - self.room_2.get_width() / 2, self.screen.get_height() / 2 - self.room_2.get_height() / 2))
            self.screen.blit(self.room_3,(self.screen.get_width() / 2 - self.room_3.get_width() / 2, self.screen.get_height() / 2 - self.room_3.get_height() / 2))
        if self.level_counter is 4:
            self.screen.blit(self.room_1,(self.screen.get_width() / 2 - self.room_1.get_width() / 2, self.screen.get_height() / 2 - self.room_1.get_height() / 2))
            self.screen.blit(self.room_2,(self.screen.get_width() / 2 - self.room_2.get_width() / 2, self.screen.get_height() / 2 - self.room_2.get_height() / 2))
            self.screen.blit(self.room_3,(self.screen.get_width() / 2 - self.room_3.get_width() / 2, self.screen.get_height() / 2 - self.room_3.get_height() / 2))
            self.screen.blit(self.room_4,(self.screen.get_width() / 2 - self.room_4.get_width() / 2, self.screen.get_height() / 2 - self.room_4.get_height() / 2))
        if self.level_counter is 5:
            self.screen.blit(self.room_1,(self.screen.get_width() / 2 - self.room_1.get_width() / 2, self.screen.get_height() / 2 - self.room_1.get_height() / 2))
            self.screen.blit(self.room_2,(self.screen.get_width() / 2 - self.room_2.get_width() / 2, self.screen.get_height() / 2 - self.room_2.get_height() / 2))
            self.screen.blit(self.room_3,(self.screen.get_width() / 2 - self.room_3.get_width() / 2, self.screen.get_height() / 2 - self.room_3.get_height() / 2))
            self.screen.blit(self.room_4,(self.screen.get_width() / 2 - self.room_4.get_width() / 2, self.screen.get_height() / 2 - self.room_4.get_height() / 2))
            self.screen.blit(self.room_5,(self.screen.get_width() / 2 - self.room_5.get_width() / 2, self.screen.get_height() / 2 - self.room_5.get_height() / 2))
        if self.level_counter is 6:
            self.screen.blit(self.room_1,(self.screen.get_width() / 2 - self.room_1.get_width() / 2, self.screen.get_height() / 2 - self.room_1.get_height() / 2))
            self.screen.blit(self.room_2,(self.screen.get_width() / 2 - self.room_2.get_width() / 2, self.screen.get_height() / 2 - self.room_2.get_height() / 2))
            self.screen.blit(self.room_3,(self.screen.get_width() / 2 - self.room_3.get_width() / 2, self.screen.get_height() / 2 - self.room_3.get_height() / 2))
            self.screen.blit(self.room_4,(self.screen.get_width() / 2 - self.room_4.get_width() / 2, self.screen.get_height() / 2 - self.room_4.get_height() / 2))
            self.screen.blit(self.room_5,(self.screen.get_width() / 2 - self.room_5.get_width() / 2, self.screen.get_height() / 2 - self.room_5.get_height() / 2))
            self.screen.blit(self.room_6,(self.screen.get_width() / 2 - self.room_6.get_width() / 2, self.screen.get_height() / 2 - self.room_6.get_height() / 2))
        if self.level_counter is 7:
            self.screen.blit(self.room_1,(self.screen.get_width() / 2 - self.room_1.get_width() / 2, self.screen.get_height() / 2 - self.room_1.get_height() / 2))
            self.screen.blit(self.room_2,(self.screen.get_width() / 2 - self.room_2.get_width() / 2, self.screen.get_height() / 2 - self.room_2.get_height() / 2))
            self.screen.blit(self.room_3,(self.screen.get_width() / 2 - self.room_3.get_width() / 2, self.screen.get_height() / 2 - self.room_3.get_height() / 2))
            self.screen.blit(self.room_4,(self.screen.get_width() / 2 - self.room_4.get_width() / 2, self.screen.get_height() / 2 - self.room_4.get_height() / 2))
            self.screen.blit(self.room_5,(self.screen.get_width() / 2 - self.room_5.get_width() / 2, self.screen.get_height() / 2 - self.room_5.get_height() / 2))
            self.screen.blit(self.room_6,(self.screen.get_width() / 2 - self.room_6.get_width() / 2, self.screen.get_height() / 2 - self.room_6.get_height() / 2))
        if self.level_counter is 8:
            self.screen.blit(self.room_1,(self.screen.get_width() / 2 - self.room_1.get_width() / 2, self.screen.get_height() / 2 - self.room_1.get_height() / 2))
            self.screen.blit(self.room_2,(self.screen.get_width() / 2 - self.room_2.get_width() / 2, self.screen.get_height() / 2 - self.room_2.get_height() / 2))
            self.screen.blit(self.room_3,(self.screen.get_width() / 2 - self.room_3.get_width() / 2, self.screen.get_height() / 2 - self.room_3.get_height() / 2))
            self.screen.blit(self.room_4,(self.screen.get_width() / 2 - self.room_4.get_width() / 2, self.screen.get_height() / 2 - self.room_4.get_height() / 2))
            self.screen.blit(self.room_5,(self.screen.get_width() / 2 - self.room_5.get_width() / 2, self.screen.get_height() / 2 - self.room_5.get_height() / 2))
            self.screen.blit(self.room_6,(self.screen.get_width() / 2 - self.room_6.get_width() / 2, self.screen.get_height() / 2 - self.room_6.get_height() / 2))
        if self.level_counter is 9:
            self.screen.blit(self.room_1,(self.screen.get_width() / 2 - self.room_1.get_width() / 2, self.screen.get_height() / 2 - self.room_1.get_height() / 2))
            self.screen.blit(self.room_2,(self.screen.get_width() / 2 - self.room_2.get_width() / 2, self.screen.get_height() / 2 - self.room_2.get_height() / 2))
            self.screen.blit(self.room_3,(self.screen.get_width() / 2 - self.room_3.get_width() / 2, self.screen.get_height() / 2 - self.room_3.get_height() / 2))
            self.screen.blit(self.room_4,(self.screen.get_width() / 2 - self.room_4.get_width() / 2, self.screen.get_height() / 2 - self.room_4.get_height() / 2))
            self.screen.blit(self.room_5,(self.screen.get_width() / 2 - self.room_5.get_width() / 2, self.screen.get_height() / 2 - self.room_5.get_height() / 2))
            self.screen.blit(self.room_6,(self.screen.get_width() / 2 - self.room_6.get_width() / 2, self.screen.get_height() / 2 - self.room_6.get_height() / 2))
        if self.level_counter is 10:
            self.screen.blit(self.room_1,(self.screen.get_width() / 2 - self.room_1.get_width() / 2, self.screen.get_height() / 2 - self.room_1.get_height() / 2))
            self.screen.blit(self.room_2,(self.screen.get_width() / 2 - self.room_2.get_width() / 2, self.screen.get_height() / 2 - self.room_2.get_height() / 2))
            self.screen.blit(self.room_3,(self.screen.get_width() / 2 - self.room_3.get_width() / 2, self.screen.get_height() / 2 - self.room_3.get_height() / 2))
            self.screen.blit(self.room_4,(self.screen.get_width() / 2 - self.room_4.get_width() / 2, self.screen.get_height() / 2 - self.room_4.get_height() / 2))
            self.screen.blit(self.room_5,(self.screen.get_width() / 2 - self.room_5.get_width() / 2, self.screen.get_height() / 2 - self.room_5.get_height() / 2))
            self.screen.blit(self.room_6,(self.screen.get_width() / 2 - self.room_6.get_width() / 2, self.screen.get_height() / 2 - self.room_6.get_height() / 2))
            self.screen.blit(self.room_7,(self.screen.get_width() / 2 - self.room_7.get_width() / 2, self.screen.get_height() / 2 - self.room_7.get_height() / 2))
            self.screen.blit(self.room_8,(self.screen.get_width() / 2 - self.room_8.get_width() / 2, self.screen.get_height() / 2 - self.room_8.get_height() / 2))
            self.screen.blit(self.room_9,(self.screen.get_width() / 2 - self.room_9.get_width() / 2, self.screen.get_height() / 2 - self.room_9.get_height() / 2))
            self.screen.blit(self.room_10,(self.screen.get_width() / 2 - self.room_10.get_width() / 2, self.screen.get_height() / 2 - self.room_10.get_height() / 2))
            


def main():
    pygame.init()
    pygame.display.set_caption("Cool Project")
    screen = pygame.display.set_mode((1300, 800))
    big_r = Map(screen)
    clock = pygame.time.Clock()
    mapped_room = Rooms(screen, level_counter = 5)
    

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
               
       
        screen.fill((255, 255, 255))
        # level_counter += 1
        big_r.draw()
        mapped_room.draw()
        pygame.display.update()


if __name__ == "__main__":
    main()
