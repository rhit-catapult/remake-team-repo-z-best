"""Game configuration and constants"""
import pygame

# Screen dimensions
W, H = 1300, 800
TILE_SIZE = 100
CORPSE_SIZE = 200

# Calculated values
VIEW_COLS = W // TILE_SIZE
VIEW_ROWS = H // TILE_SIZE

# Game settings
PLAYER_SPEED = 5
FPS = 60

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()
popup_font = pygame.font.Font(None, 48)
