import pygame
import sys
import math
from collision import is_wall_collision, is_out_of_screen

class Zombie:
    def __init__(self, screen, x, y, image_filename):
        self.screen = screen
        self.x = x
        self.y = y
        self.hp = 3
# SCALE THE ZOMBIE
        scale = 0.5   # 50% size — change this number to whatever you want
        w = self.original_image.get_width()
        h = self.original_image.get_height()
        self.original_image = pygame.transform.scale(self.original_image, (int(w * scale), int(h * scale)))
         self.image = self.original_image
         self.rect = self.image.get_rect(center=(self.x, self.y))
        self.radius = 40   # adjust to match your zombie sprite size

    def follow_player(self, player, speed=2):
        # Move toward the player slowly
        dx = player.x - self.x
        dy = player.y - self.y

        distance = math.hypot(dx, dy)
        if distance == 0:
            return

        dx /= distance
        dy /= distance

        move_x = dx * speed
        move_y = dy * speed

        # Resolve movement axis-by-axis so zombies cannot clip through walls/fences.
        new_x = self.x + move_x
        if not is_wall_collision(new_x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2) and not is_out_of_screen(new_x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2):
            self.x = new_x

        new_y = self.y + move_y
        if not is_wall_collision(self.x - self.radius, new_y - self.radius, self.radius * 2, self.radius * 2) and not is_out_of_screen(self.x - self.radius, new_y - self.radius, self.radius * 2, self.radius * 2):
            self.y = new_y

        self.rect.center = (self.x, self.y)
    def update_angle(self, player):
        # Instantly face the player
        dx = player.x - self.x
        dy = player.y - self.y

        angle = math.degrees(math.atan2(-dy, dx))

        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def draw(self):
        self.screen.blit(self.image, self.rect)


def test_character():
    screen = pygame.display.set_mode((640, 480))
    character = Zombie(screen, 400, 400, "ZombieFIXED.png")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.fill("white")
        character.draw()
        pygame.display.update()


if __name__ == "__main__":
    test_character()