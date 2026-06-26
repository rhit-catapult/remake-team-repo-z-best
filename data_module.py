import pygame
import sys
import random
import time


class MousePosition:
    def __init__(self, screen):
        self.screen = screen
        self.x = pygame.mouse.get_pos()[0]
        self.y = pygame.mouse.get_pos()[1]

    def is_clicked(self, mouse_pos):
        if pygame.mouse.get_pressed()[0]:  # Check if left mouse button is pressed
            self.x, self.y = mouse_pos
            return True
        return False
  

def main():
    pygame.init()
    pygame.display.set_caption("Cool Project")
    screen = pygame.display.set_mode((1300, 800))
    clock = pygame.time.Clock()
    mouse = MousePosition(screen)

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if mouse.is_clicked(event.pos):
                    print("clicked")
            
    
        screen.fill((255, 255, 255))
        
        pygame.display.update()


if __name__ == "__main__":
    main()