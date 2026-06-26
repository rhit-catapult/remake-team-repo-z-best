import random
import pygame



def main():
    pygame.init()
    screen = pygame.display.set_mode((1300,800))
    
class Player:
    def __init__(self, screen, x, y):
        self.screen = screen
        self.x=x
        self.y=y 
