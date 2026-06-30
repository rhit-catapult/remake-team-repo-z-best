import pygame

class HealthBar:
    def __init__(self, screen):
        self.screen = screen

        # Load your premade PNGs
        self.images = [
            pygame.image.load("0hearts.png"),  # 0 HP
            pygame.image.load("1hearts.png"),  # 1 HP
            pygame.image.load("2hearts.png"),  # 2 HP
            pygame.image.load("3hearts.png"),  # 3 HP
            pygame.image.load("4hearts.png"),  # 4 HP
        ]

        self.hp = 4  # start full health

    def set_hp(self, hp):
        self.hp = max(0, min(4, hp))  # clamp between 0–5

    def draw(self):
        img = self.images[self.hp]
        self.screen.blit(img, (20, 20))  # top-left corner