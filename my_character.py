import pygame
import sys
import math
import peanut_bullet_module

class MainC:
    def __init__(self, screen, x, y, image_filename):
        self.screen = screen
        self.x = x
        self.y = y
        self.original_image = pygame.image.load(image_filename).convert_alpha()
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.bullets = []
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()

    def update_angle(self):
        dx = self.mouse_x - self.x
        dy = self.mouse_y - self.y
        angle = math.degrees(math.atan2(-dy, dx))  # negative dy because pygame y-axis is flipped

        # rotate image
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def draw(self):
        self.screen.blit(self.image, self.rect)
        
    def draw_crosshairs(self):
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
        crosshair_width = 2
        crosshair_height = 30
        pygame.draw.rect(self.screen, pygame.Color("black"), (self.mouse_x - crosshair_width / 2, self.mouse_y - crosshair_height / 2, crosshair_width, crosshair_height))
        pygame.draw.rect(self.screen, pygame.Color("black"), (self.mouse_x - crosshair_height / 2, self.mouse_y - crosshair_width / 2, crosshair_height, crosshair_width))

    def fire(self):
        self.bullets.append(peanut_bullet_module.Bullet(self.screen, self.x, self.y))


def test_character():
    # TODO: change this function to test your class
    screen = pygame.display.set_mode((640, 480))
    character = MainC(screen, 400, 400, "Character_Placeholder.png")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.fill("white")
        character.draw()
        pygame.display.update()


# Testing the classes
# click the green arrow to the left or run "Current File" in PyCharm to test this class
if __name__ == "__main__":
    test_character()
