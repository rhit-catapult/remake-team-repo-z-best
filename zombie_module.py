import pygame
import sys
import math

class Zombie:
    def __init__(self, screen, x, y, image_filename):
        self.screen = screen
        self.x = x
        self.y = y
        self.original_image = pygame.image.load(image_filename).convert_alpha()
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update_angle(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        dx = mouse_x - self.x
        dy = mouse_y - self.y
        angle = math.degrees(math.atan2(-dy, dx))  # negative dy because pygame y-axis is flipped

        # rotate image
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def draw(self):
        self.screen.blit(self.image, self.rect)
# This function is called when you run this file, and is used to test the Character class individually.
# When you create more files with different classes, copy the code below, then
# change it to properly test that class
def test_character():
    # TODO: change this function to test your class
    screen = pygame.display.set_mode((640, 480))
    character = Zombie(screen, 400, 400, "Character_Placeholder.png")
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
