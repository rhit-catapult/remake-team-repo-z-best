import pygame
import sys
import random
import time
import data_module
import my_character


class Bullet:
    def __init__(self, screen: pygame.Surface, hero_x, hero_y, mouse_x, mouse_y):
        self.screen = screen
        self.peanut = pygame.image.load("Peanut_bullet.png")
        scale = 0.2
        self.peanut = pygame.transform.scale(self.peanut, (self.peanut.get_width() * scale, self.peanut.get_height() * scale))
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y
        self.bullet_x = hero_x
        self.bullet_y = hero_y
        self.change_x = self.bullet_x - self.mouse_x
        self.change_y = self.bullet_y - self.mouse_y
        # self.speed = (self.bullet_x - self.change_x) / 1 + (self.bullet_y - self.change_y)
        self.speed = 50
    def move(self):
        self.bullet_x -= self.change_x // self.speed
        self.bullet_y -= self.change_y // self.speed

    def draw(self):
        self.screen.blit(self.peanut, (self.bullet_x, self.bullet_y))
        



def main():
    pygame.init()
    pygame.display.set_caption("Cool Project")
    screen = pygame.display.set_mode((1300, 800))
    clock = pygame.time.Clock()
    mouse = data_module.MousePosition(screen)
    hero = my_character.MainC(screen, 600, 700, "Character_Placeholder.png")
    bullet = Bullet(screen, hero.x, hero.y)

    while True:
        clock.tick(20)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if mouse.is_clicked(event.pos):
                    hero.fire()
            if event.type == pygame.QUIT:
                sys.exit()
    
        screen.fill((255, 255, 255))
        
        for bullet in hero.bullets:
            bullet.move()
            bullet.draw()
            
        hero.update_angle()
        hero.draw()
        hero.draw_crosshairs()

        pygame.display.update()


if __name__ == "__main__":
    main()
