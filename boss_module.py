import pygame
import math
import sys
from zombie_module import Zombie

class level_title:
    def __init__(self, screen, room_number):
        self.screen = screen
        self.level = room_number
    def draw(self):
        self.screen.blit((pygame.image.load("level.png")),(800,0))
        if self.level is 1:
            image_filename = ("1.png")
        if self.level is 2:
            image_filename = ("2.png")
        if self.level is 3:
            image_filename = ("3.png")
        if self.level is 4: #Boss Jose
            image_filename = ("4_.png")
        if self.level is 5:
            image_filename = ("5.png")
        if self.level is 6:
            image_filename = ("6.png")
        if self.level is 7: #Boss Autumn
            image_filename = ("7_.png")
        if self.level is 8:
            image_filename = ("8.png")
        if self.level is 9:
            image_filename = ("9.png")
        if self.level is 10: #Boss Ethan
            image_filename = ("10_.png")
        if self.level is 1 or 2 or 3 or 5 or 6 or 8 or 9:
            self.x = 955
            self.y = 100
        else:
            self.x = 800
            self.y = 100
        self.screen.blit(pygame.image.load(image_filename), (self.x, self.y))


class Boss_class:
    def __init__(self, screen, x, y, image_filename, hp, size):
        self.screen = screen            
        self.x = x
        self.y = y
        self.original_image = pygame.image.load(image_filename).convert_alpha()
        
# SCALE THE ZOMBIE
        scale = size   # 50% size — change this number to whatever you want
        w = self.original_image.get_width()
        h = self.original_image.get_height()
        self.final_image = pygame.transform.scale(self.original_image, (int(w * scale), int(h * scale)))
        self.image = self.final_image
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.hp = hp
        self.radius = (self.final_image.get_width() / 2) + 2
    def follow_player(self, player, speed=2):
        # Move toward the player slowly
        dx = player.x - self.x
        dy = player.y - self.y

        distance = math.hypot(dx, dy)
        if distance == 0:
            return

        dx /= distance
        dy /= distance

        self.x += dx * speed
        self.y += dy * speed

        self.rect.center = (self.x, self.y)
    def update_angle(self, player):
        # Instantly face the player
        dx = player.x - self.x
        dy = player.y - self.y

        angle = math.degrees(math.atan2(-dy, dx))

        # Rotate the scaled image so boss size stays consistent while turning.
        self.image = pygame.transform.rotate(self.final_image, angle)
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def draw(self):
        self.screen.blit(self.image, self.rect)

def test_character():
    screen = pygame.display.set_mode((1300, 800))
    Jose = Boss_class(screen, 200, 400, "Boss_Jose.png", 20, 4)
    Autumn = Boss_class(screen, 600, 400,"Boss_Autum.png", 35, 5.5)
    Ethan = Boss_class(screen, 1000, 400, "Boss_Ethan.png", 50, 7)
    zombie = Boss_class(screen, 100, 100, "Boss_Jose.png", 5, 2)
    title = level_title(screen, 10)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.fill("white")
        Jose.draw()
        Autumn.draw()
        Ethan.draw()
        zombie.draw()
        title.draw()
        pygame.display.update()


if __name__ == "__main__":
    test_character()