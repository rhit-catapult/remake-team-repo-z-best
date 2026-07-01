"""Image loading and sprite management"""
import pygame
from config import TILE_SIZE, CORPSE_SIZE

def load_image(path, size, use_alpha=False):
    """Load and scale image with optional alpha channel"""
    method = "convert_alpha" if use_alpha else "convert"
    img = pygame.image.load(path)
    img = getattr(img, method)()
    return pygame.transform.scale(img, size)

# Load all sprites
tile_floor = load_image("White_Tile.png", (TILE_SIZE, TILE_SIZE))
tile_floor_blood = load_image("Blood_Tile_fixed.png", (TILE_SIZE, TILE_SIZE))
tile_wall = load_image("brick_wall.png", (TILE_SIZE, TILE_SIZE))
tile_grass = load_image("grass-tile.png", (TILE_SIZE, TILE_SIZE))
tile_fence = load_image("fence.png"(TILE_SIZE, TILE_SIZE))
box = load_image("box.png", (TILE_SIZE, TILE_SIZE), use_alpha=True)
corpse = load_image("dead_Zombie.png", (CORPSE_SIZE, TILE_SIZE), use_alpha=True)
player = load_image("Character_Placeholder.png", (TILE_SIZE, TILE_SIZE), use_alpha=True)


# Tile ID to sprite mapping (0=floor, 1=wall, 2=grass, 3=blood)
TILE_SPRITES = {0: tile_floor, 1: tile_wall, 2: tile_grass, 3: tile_floor_blood, 4:tile_fence}

# Item type to sprite mapping (10=box, 20=corpse)
ITEM_SPRITES = {10: box, 20: corpse}
