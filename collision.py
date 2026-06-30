"""Collision detection functions"""
from config import TILE_SIZE
from maps import full_world_map

def is_wall_collision(x, y, w, h):
    """Check if position collides with walls"""
    left_col = int(x // TILE_SIZE)
    right_col = int((x + w - 1) // TILE_SIZE)
    top_row = int(y // TILE_SIZE)
    bottom_row = int((y + h - 1) // TILE_SIZE)

    for r in range(top_row, bottom_row + 1):
        if r < 0 or r >= len(full_world_map):
            continue
        for c in range(left_col, right_col + 1):
            if c < 0 or c >= len(full_world_map[r]):
                continue
            if full_world_map[r][c] == 1:
                return True
    return False

def is_out_of_screen(x, y, w, h):
    """Check if position is outside map bounds"""
    map_width = len(full_world_map[0]) * TILE_SIZE
    map_height = len(full_world_map) * TILE_SIZE
    return x < 0 or y < 0 or (x + w) > map_width or (y + h) > map_height
