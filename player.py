"""Player movement and control"""
import pygame
from config import TILE_SIZE, VIEW_COLS, VIEW_ROWS, PLAYER_SPEED
from collision import is_wall_collision, is_out_of_screen
from maps import full_world_map

def player_movement(player_x, player_y, view_offset_x, view_offset_y):
    """Handle player movement and camera update"""
    keys = pygame.key.get_pressed()
    dx, dy = 0, 0

    if keys[pygame.K_UP]:
        dy -= PLAYER_SPEED
    if keys[pygame.K_DOWN]:
        dy += PLAYER_SPEED
    if keys[pygame.K_LEFT]:
        dx -= PLAYER_SPEED
    if keys[pygame.K_RIGHT]:
        dx += PLAYER_SPEED

    # Move X independently
    new_x = player_x + dx
    if not is_wall_collision(new_x, player_y, TILE_SIZE, TILE_SIZE) and not is_out_of_screen(new_x, player_y, TILE_SIZE, TILE_SIZE):
        player_x = new_x

    # Move Y independently
    new_y = player_y + dy
    if not is_wall_collision(player_x, new_y, TILE_SIZE, TILE_SIZE) and not is_out_of_screen(player_x, new_y, TILE_SIZE, TILE_SIZE):
        player_y = new_y

    # Update camera to follow player
    view_offset_x = player_x / TILE_SIZE - VIEW_COLS / 2
    view_offset_y = player_y / TILE_SIZE - VIEW_ROWS / 2

    # Clamp camera to map bounds
    max_view_col = len(full_world_map[0]) - VIEW_COLS
    max_view_row = len(full_world_map) - VIEW_ROWS
    view_offset_x = max(0, min(view_offset_x, max_view_col))
    view_offset_y = max(0, min(view_offset_y, max_view_row))

    return player_x, player_y, view_offset_x, view_offset_y
