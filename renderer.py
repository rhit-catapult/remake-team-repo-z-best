"""Rendering and drawing functions"""
import pygame
from config import W, H, TILE_SIZE, screen, popup_font, VIEW_COLS, VIEW_ROWS
from assets import TILE_SPRITES, ITEM_SPRITES
from maps import full_world_map, locked_rows_count, items

def draw_full_map(view_offset_x, view_offset_y, is_unlocked):
    """Draw the complete map with camera offset"""
    start_col = int(view_offset_x)
    start_row = int(view_offset_y)

    for row_idx in range(start_row, start_row + VIEW_ROWS + 1):
        if row_idx < 0 or row_idx >= len(full_world_map):
            continue
        row_data = full_world_map[row_idx]
        for col_idx in range(start_col, start_col + VIEW_COLS + 1):
            if col_idx < 0 or col_idx >= len(row_data):
                continue
            tile_id = row_data[col_idx]
            tile_img = TILE_SPRITES[tile_id].copy()

            # Darken maps 2-4 if not unlocked.
            if row_idx < locked_rows_count and not is_unlocked:
                tile_img.set_alpha(60)

            screen_x = col_idx * TILE_SIZE - view_offset_x * TILE_SIZE
            screen_y = row_idx * TILE_SIZE - view_offset_y * TILE_SIZE
            screen.blit(tile_img, (screen_x, screen_y))

def draw_items(view_offset_x, view_offset_y):
    """Draw all items on the map"""
    for row, col, item_type in items:
        screen_x = col * TILE_SIZE - view_offset_x * TILE_SIZE
        screen_y = row * TILE_SIZE - view_offset_y * TILE_SIZE
        screen.blit(ITEM_SPRITES[item_type], (screen_x, screen_y))

def draw_popup():
    """Draw unlock popup overlay"""
    overlay = pygame.Surface((W, H), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 120))
    screen.blit(overlay, (0, 0))

    text1 = popup_font.render("Press E to unlock", True, (220, 220, 220))
    text2 = popup_font.render("Maps 2-4 are locked", True, (220, 220, 220))
    screen.blit(text1, (W/2 - text1.get_width()/2, H/2 - 40))
    screen.blit(text2, (W/2 - text2.get_width()/2, H/2 + 10))

def draw_player(player_x, player_y, view_offset_x, view_offset_y, player_sprite):
    """Draw the player character"""
    screen_x = player_x - view_offset_x * TILE_SIZE
    screen_y = player_y - view_offset_y * TILE_SIZE
    screen.blit(player_sprite, (screen_x, screen_y))
