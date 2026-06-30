import pygame
import math

class boss:
    def __init__(self, screen, x, y, image_filename, hp, size):
        self.screen = screen            
        self.x = x
        self.y = y
        self.original_image = pygame.image.load(image_filename).convert_alpha()
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.original_image = pygame.image.load(image_filename).convert_alpha()
        self.hp = hp
# SCALE THE ZOMBIE
        scale = size   # 50% size — change this number to whatever you want
        w = self.original_image.get_width()
        h = self.original_image.get_height()
        self.original_image = pygame.transform.scale(self.original_image, (int(w * scale), int(h * scale)))
        self.radius = size + 30   # adjust to match your zombie sprite size

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

        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def draw(self):
        self.screen.blit(self.image, self.rect)

def test_character():
    screen = pygame.display.set_mode((640, 480))
    character = boss(screen, 400, 400, "Boss_Jose.png", 5, 2)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.fill("white")
        character.draw()
        pygame.display.update()


if __name__ == "__main__":
    test_character()