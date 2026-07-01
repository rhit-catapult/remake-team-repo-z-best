import pygame
import sys
import random
import math
from healthbar import HealthBar
from my_character import MainC
from zombie_module import Zombie
from map import Rooms
from maps import full_world_map, map1_start_row, map2_start_row, map3_start_row, map3_start_col, map3_room_rows_count, map3_room_cols_count, map4_start_row, map5_start_row, map5_start_col, map5_rows_count, map5_cols_count, map7_start_row, map7_start_col, map7_rows_count, map7_cols_count, map8_start_row, map8_start_col, map8_rows_count, map8_cols_count, room6_passage_start_row, room6_passage_end_row, room6_passage_start_col, room6_passage_end_col, items
from assets import TILE_SPRITES, ITEM_SPRITES
from config import TILE_SIZE
from collision import is_wall_collision, is_out_of_screen
from boss_module import Boss_class

# ---------------- START SCREEN ---------------- #

def start_screen(screen):
    start_img = pygame.image.load("Welcome_page.png").convert_alpha()
    start_img = pygame.transform.scale(start_img, (1300, 800))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                return

        screen.blit(start_img, (0, 0))
        pygame.display.update()


def death_screen(screen):
    death_img = pygame.image.load("you_died.png").convert_alpha()
    death_img = pygame.transform.scale(death_img, (1300, 800))

    start_time = pygame.time.get_ticks()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.time.get_ticks() - start_time > 1000:
                    return

        screen.blit(death_img, (0, 0))
        pygame.display.update()


def escaped_screen(screen):
    popup_font = pygame.font.Font(None, 104)
    hint_font = pygame.font.Font(None, 44)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return

        screen.fill((8, 26, 22))
        title_text = popup_font.render("YOU ESCAPED", True, (230, 246, 233))
        hint_text = hint_font.render("Press any key to continue", True, (205, 225, 212))

        screen.blit(title_text, (1300 / 2 - title_text.get_width() / 2, 800 / 2 - 90))
        screen.blit(hint_text, (1300 / 2 - hint_text.get_width() / 2, 800 / 2 + 20))
        pygame.display.update()


def _player_in_final_room(player):
    col_idx = int(player.x // TILE_SIZE)
    row_idx = int(player.y // TILE_SIZE)

    in_bounds = (
        map8_start_row <= row_idx < (map8_start_row + map8_rows_count)
        and map8_start_col <= col_idx < (map8_start_col + map8_cols_count)
    )
    if not in_bounds:
        return False

    if row_idx < 0 or row_idx >= len(full_world_map):
        return False
    if col_idx < 0 or col_idx >= len(full_world_map[row_idx]):
        return False

    return full_world_map[row_idx][col_idx] not in (1, 4)


def _player_in_room6_passage(player):
    col_idx = int(player.x // TILE_SIZE)
    row_idx = int(player.y // TILE_SIZE)

    in_bounds = (
        room6_passage_start_row <= row_idx <= room6_passage_end_row
        and room6_passage_start_col <= col_idx <= room6_passage_end_col
    )
    if not in_bounds:
        return False

    if row_idx < 0 or row_idx >= len(full_world_map):
        return False
    if col_idx < 0 or col_idx >= len(full_world_map[row_idx]):
        return False

    return full_world_map[row_idx][col_idx] not in (1, 4)


def _player_in_room3(player):
    return _intersects_room(
        player.x,
        player.y,
        player.radius,
        map3_start_row,
        map3_start_col,
        map3_room_rows_count,
        map3_room_cols_count,
    )


def _intersects_room(player_x, player_y, radius, room_start_row, room_start_col, room_rows, room_cols):
    left = player_x - radius
    right = player_x + radius
    top = player_y - radius
    bottom = player_y + radius

    room_left = room_start_col * TILE_SIZE
    room_right = (room_start_col + room_cols) * TILE_SIZE
    room_top = room_start_row * TILE_SIZE
    room_bottom = (room_start_row + room_rows) * TILE_SIZE

    return right >= room_left and left < room_right and bottom >= room_top and top < room_bottom


# ---------------- ZOMBIE SPAWNING ---------------- #

def spawn_zombies(screen, player, count=5):
    zombies = []
    spawn_radius = 40
    for _ in range(count):
        while True:
            x = random.randint(50, 1250)
            y = random.randint(50, 750)

            dx = player.x - x
            dy = player.y - y
            distance = math.hypot(dx, dy)
            collides_with_map = is_wall_collision(
                x - spawn_radius,
                y - spawn_radius,
                spawn_radius * 2,
                spawn_radius * 2,
            )
            if distance > (player.radius + 100) and not collides_with_map:  # safe buffer + valid spawn tile
                zombie = Zombie(screen, x, y, "ZombieFIXED.png")
                zombie.hp = 3
                zombies.append(zombie)
                break

    return zombies


def spawn_zombies_in_room(screen, player, count, room_start_row, room_start_col, room_rows, room_cols):
    zombies = []
    spawn_radius = 40

    min_x = room_start_col * TILE_SIZE + spawn_radius
    max_x = (room_start_col + room_cols) * TILE_SIZE - spawn_radius
    min_y = room_start_row * TILE_SIZE + spawn_radius
    max_y = (room_start_row + room_rows) * TILE_SIZE - spawn_radius

    if min_x >= max_x or min_y >= max_y:
        return zombies

    for _ in range(count):
        for _attempt in range(200):
            x = random.randint(int(min_x), int(max_x))
            y = random.randint(int(min_y), int(max_y))

            dx = player.x - x
            dy = player.y - y
            distance = math.hypot(dx, dy)
            collides_with_map = is_wall_collision(
                x - spawn_radius,
                y - spawn_radius,
                spawn_radius * 2,
                spawn_radius * 2,
            )
            if distance > (player.radius + 100) and not collides_with_map:
                zombie = Zombie(screen, x, y, "ZombieFIXED.png")
                zombie.hp = 3
                zombies.append(zombie)
                break

    return zombies


def spawn_patrol_zombies_in_room(screen, player, count, room_start_row, room_start_col, room_rows, room_cols):
    zombies = []
    spawn_radius = 40

    min_x = room_start_col * TILE_SIZE + spawn_radius
    max_x = (room_start_col + room_cols) * TILE_SIZE - spawn_radius
    min_y = room_start_row * TILE_SIZE + spawn_radius
    max_y = (room_start_row + room_rows) * TILE_SIZE - spawn_radius

    if min_x >= max_x or min_y >= max_y:
        return zombies

    for _ in range(count):
        for _attempt in range(200):
            x = random.randint(int(min_x), int(max_x))
            y = random.randint(int(min_y), int(max_y))

            collides_with_map = is_wall_collision(
                x - spawn_radius,
                y - spawn_radius,
                spawn_radius * 2,
                spawn_radius * 2,
            )
            if not collides_with_map:
                zombie = Zombie(screen, x, y, "ZombieFIXED.png")
                zombie.hp = 3
                zombie.patrol_mode = True
                zombie.patrol_dir = random.choice((-1, 1))
                zombie.patrol_speed = 2.0
                zombie.wave_tag = "room2_patrol"
                zombies.append(zombie)
                break

    return zombies


def spawn_corner_zombies_in_room(screen, player, count, room_start_row, room_start_col, room_rows, room_cols):
    zombies = []
    spawn_radius = 40

    room_left = room_start_col * TILE_SIZE
    room_right = (room_start_col + room_cols) * TILE_SIZE
    room_top = room_start_row * TILE_SIZE
    room_bottom = (room_start_row + room_rows) * TILE_SIZE

    corners = [
        (room_left + spawn_radius + 30, room_top + spawn_radius + 30),
        (room_right - spawn_radius - 30, room_top + spawn_radius + 30),
        (room_left + spawn_radius + 30, room_bottom - spawn_radius - 30),
        (room_right - spawn_radius - 30, room_bottom - spawn_radius - 30),
    ]

    for idx in range(count):
        base_x, base_y = corners[idx % len(corners)]
        placed = False

        for _attempt in range(120):
            x = int(base_x + random.randint(-35, 35))
            y = int(base_y + random.randint(-35, 35))

            x = max(int(room_left + spawn_radius), min(x, int(room_right - spawn_radius)))
            y = max(int(room_top + spawn_radius), min(y, int(room_bottom - spawn_radius)))

            collides_with_map = is_wall_collision(
                x - spawn_radius,
                y - spawn_radius,
                spawn_radius * 2,
                spawn_radius * 2,
            )
            if collides_with_map:
                continue

            dx = player.x - x
            dy = player.y - y
            if math.hypot(dx, dy) <= (player.radius + 100):
                continue

            zombie = Zombie(screen, x, y, "ZombieFIXED.png")
            zombie.hp = 3
            zombie.wave_tag = "wave1"
            zombies.append(zombie)
            placed = True
            break

        if not placed:
            # Safe fallback: search anywhere in the room, but only on walkable tiles.
            for _fallback_attempt in range(400):
                x = random.randint(int(room_left + spawn_radius), int(room_right - spawn_radius))
                y = random.randint(int(room_top + spawn_radius), int(room_bottom - spawn_radius))

                collides_with_map = is_wall_collision(
                    x - spawn_radius,
                    y - spawn_radius,
                    spawn_radius * 2,
                    spawn_radius * 2,
                )
                if collides_with_map:
                    continue

                dx = player.x - x
                dy = player.y - y
                if math.hypot(dx, dy) <= (player.radius + 100):
                    continue

                zombie = Zombie(screen, x, y, "ZombieFIXED.png")
                zombie.hp = 3
                zombie.wave_tag = "wave1"
                zombies.append(zombie)
                placed = True
                break

    return zombies


def keep_zombie_in_room(zombie, room_start_row, room_start_col, room_rows, room_cols):
    min_x = room_start_col * TILE_SIZE + zombie.radius
    max_x = (room_start_col + room_cols) * TILE_SIZE - zombie.radius
    min_y = room_start_row * TILE_SIZE + zombie.radius
    max_y = (room_start_row + room_rows) * TILE_SIZE - zombie.radius

    zombie.x = max(min_x, min(zombie.x, max_x))
    zombie.y = max(min_y, min(zombie.y, max_y))
    zombie.rect.center = (zombie.x, zombie.y)


def move_patrol_zombie(zombie, room_start_row, room_start_col, room_rows, room_cols):
    min_x = room_start_col * TILE_SIZE + zombie.radius
    max_x = (room_start_col + room_cols) * TILE_SIZE - zombie.radius
    min_y = room_start_row * TILE_SIZE + zombie.radius
    max_y = (room_start_row + room_rows) * TILE_SIZE - zombie.radius

    next_x = zombie.x + zombie.patrol_dir * zombie.patrol_speed

    hits_wall = is_wall_collision(next_x - zombie.radius, zombie.y - zombie.radius, zombie.radius * 2, zombie.radius * 2)
    out_of_bounds = is_out_of_screen(next_x - zombie.radius, zombie.y - zombie.radius, zombie.radius * 2, zombie.radius * 2)
    hits_room_side = next_x <= min_x or next_x >= max_x

    if hits_wall or out_of_bounds or hits_room_side:
        zombie.patrol_dir *= -1
        next_x = zombie.x + zombie.patrol_dir * zombie.patrol_speed

    zombie.x = max(min_x, min(next_x, max_x))
    zombie.y = max(min_y, min(zombie.y, max_y))

    # Face the direction of patrol movement: right=0deg, left=180deg.
    facing_angle = 0 if zombie.patrol_dir > 0 else 180
    zombie.image = pygame.transform.rotate(zombie.original_image, facing_angle)
    zombie.rect = zombie.image.get_rect(center=(zombie.x, zombie.y))


# ---------------- MAP RENDERING ---------------- #

def _is_fence_tile(row_idx, col_idx):
    """Return True when the map tile exists and is a fence tile."""
    if row_idx < 0 or row_idx >= len(full_world_map):
        return False
    row = full_world_map[row_idx]
    if col_idx < 0 or col_idx >= len(row):
        return False
    return row[col_idx] == 4


def _get_fence_overlay(row_idx, col_idx):
    """Rotate fence sprite to match neighbor direction where possible."""
    up = _is_fence_tile(row_idx - 1, col_idx)
    down = _is_fence_tile(row_idx + 1, col_idx)
    left = _is_fence_tile(row_idx, col_idx - 1)
    right = _is_fence_tile(row_idx, col_idx + 1)

    fence_img = TILE_SPRITES[4].copy()

    # If this segment connects mostly vertically, rotate the fence texture.
    if (up or down) and not (left or right):
        fence_img = pygame.transform.rotate(fence_img, 90)

    return fence_img

def draw_map(screen, view_offset_x, view_offset_y, unlocked_min_row, room5_unlocked, room7_unlocked, room8_unlocked):
    view_cols = 1300 // TILE_SIZE
    view_rows = 800 // TILE_SIZE
    start_col = int(view_offset_x)
    start_row = int(view_offset_y)
    
    for row_idx in range(start_row, start_row + view_rows + 1):
        if row_idx < 0 or row_idx >= len(full_world_map):
            continue
        row = full_world_map[row_idx]
        for col_idx in range(start_col, start_col + view_cols + 1):
            if col_idx < 0 or col_idx >= len(row):
                continue
            tile_id = row[col_idx]
            if tile_id in TILE_SPRITES:
                screen_x = col_idx * TILE_SIZE - view_offset_x * TILE_SIZE
                screen_y = row_idx * TILE_SIZE - view_offset_y * TILE_SIZE
                should_darken = False
                if row_idx < unlocked_min_row:
                    should_darken = True
                if (not room5_unlocked) and row_idx >= map5_start_row and row_idx < (map5_start_row + map5_rows_count) and col_idx >= map5_start_col:
                    should_darken = True
                if (not room7_unlocked) and row_idx >= map7_start_row and row_idx < (map7_start_row + map7_rows_count) and col_idx >= map7_start_col and col_idx < (map7_start_col + map7_cols_count):
                    should_darken = True
                if (not room8_unlocked) and row_idx >= map8_start_row and row_idx < (map8_start_row + map8_rows_count) and col_idx >= map8_start_col and col_idx < (map8_start_col + map8_cols_count):
                    should_darken = True

                # Fence tile uses grass as base with a transparent fence overlay.
                if tile_id == 4:
                    base_img = TILE_SPRITES[2].copy()
                    fence_img = _get_fence_overlay(row_idx, col_idx)
                    screen.blit(base_img, (screen_x, screen_y))
                    # Slight overlap helps hide seams at tile boundaries.
                    screen.blit(fence_img, (screen_x - 1, screen_y - 1))
                    if should_darken:
                        dark_overlay = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
                        dark_overlay.fill((0, 0, 0, 210))
                        screen.blit(dark_overlay, (screen_x, screen_y))
                else:
                    tile_img = TILE_SPRITES[tile_id].copy()
                    screen.blit(tile_img, (screen_x, screen_y))
                    if should_darken:
                        dark_overlay = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
                        dark_overlay.fill((0, 0, 0, 210))
                        screen.blit(dark_overlay, (screen_x, screen_y))


def draw_map_items(screen, view_offset_x, view_offset_y):
    for row, col, item_type in items:
        if item_type in ITEM_SPRITES:
            screen_x = col * TILE_SIZE - view_offset_x * TILE_SIZE
            screen_y = row * TILE_SIZE - view_offset_y * TILE_SIZE
            screen.blit(ITEM_SPRITES[item_type], (screen_x, screen_y))


def draw_unlock_prompt(screen, next_map_number):
    prompt_bg = pygame.Surface((420, 54), pygame.SRCALPHA)
    prompt_bg.fill((15, 15, 15, 190))
    screen.blit(prompt_bg, (1300 / 2 - 210, 24))

    popup_font = pygame.font.Font(None, 42)
    prompt_text = popup_font.render(f"Press E to unlock Map {next_map_number}", True, (230, 230, 230))
    screen.blit(prompt_text, (1300 / 2 - prompt_text.get_width() / 2, 35))


def draw_level2_popup(screen, kills, elapsed_seconds):
    overlay = pygame.Surface((1300, 800), pygame.SRCALPHA)
    overlay.fill((10, 25, 40, 120))
    screen.blit(overlay, (0, 0))

    title_font = pygame.font.Font(None, 120)
    stat_font = pygame.font.Font(None, 56)

    mins = elapsed_seconds // 60
    secs = elapsed_seconds % 60
    time_text = f"Time: {mins:02d}:{secs:02d}"

    stage_text = title_font.render("STAGE 2", True, (240, 240, 240))
    kills_text = stat_font.render(f"Zombies Killed: {kills}", True, (225, 235, 245))
    elapsed_text = stat_font.render(time_text, True, (225, 235, 245))

    screen.blit(stage_text, (1300 / 2 - stage_text.get_width() / 2, 800 / 2 - 150))
    screen.blit(kills_text, (1300 / 2 - kills_text.get_width() / 2, 800 / 2 - 20))
    screen.blit(elapsed_text, (1300 / 2 - elapsed_text.get_width() / 2, 800 / 2 + 40))


def draw_level3_popup(screen, kills, elapsed_seconds):
    overlay = pygame.Surface((1300, 800), pygame.SRCALPHA)
    overlay.fill((25, 12, 40, 120))
    screen.blit(overlay, (0, 0))

    title_font = pygame.font.Font(None, 120)
    stat_font = pygame.font.Font(None, 56)

    mins = elapsed_seconds // 60
    secs = elapsed_seconds % 60
    time_text = f"Time: {mins:02d}:{secs:02d}"

    stage_text = title_font.render("STAGE 3", True, (240, 240, 240))
    kills_text = stat_font.render(f"Zombies Killed: {kills}", True, (225, 235, 245))
    elapsed_text = stat_font.render(time_text, True, (225, 235, 245))

    screen.blit(stage_text, (1300 / 2 - stage_text.get_width() / 2, 800 / 2 - 150))
    screen.blit(kills_text, (1300 / 2 - kills_text.get_width() / 2, 800 / 2 - 20))
    screen.blit(elapsed_text, (1300 / 2 - elapsed_text.get_width() / 2, 800 / 2 + 40))


def draw_stage1_popup(screen):
    overlay = pygame.Surface((1300, 800), pygame.SRCALPHA)
    overlay.fill((20, 20, 30, 120))
    screen.blit(overlay, (0, 0))

    popup_font = pygame.font.Font(None, 120)
    stage_text = popup_font.render("STAGE 1", True, (240, 240, 240))
    screen.blit(stage_text, (1300 / 2 - stage_text.get_width() / 2, 800 / 2 - stage_text.get_height() / 2))


def draw_escape_prompt(screen):
    prompt_bg = pygame.Surface((380, 54), pygame.SRCALPHA)
    prompt_bg.fill((10, 32, 26, 190))
    screen.blit(prompt_bg, (1300 / 2 - 190, 84))

    popup_font = pygame.font.Font(None, 42)
    prompt_text = popup_font.render("Press G to escape", True, (222, 245, 232))
    screen.blit(prompt_text, (1300 / 2 - prompt_text.get_width() / 2, 95))


def draw_pause_popup(screen, zombies_killed):
    """Draw transparent pause popup with kill counter."""
    overlay = pygame.Surface((1300, 800), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 120))
    screen.blit(overlay, (0, 0))

    panel = pygame.Surface((540, 260), pygame.SRCALPHA)
    panel.fill((20, 20, 20, 185))
    panel_x = 1300 / 2 - 270
    panel_y = 800 / 2 - 130
    screen.blit(panel, (panel_x, panel_y))
    pygame.draw.rect(screen, (230, 230, 230), (panel_x, panel_y, 540, 260), 2)

    title_font = pygame.font.Font(None, 96)
    text_font = pygame.font.Font(None, 44)

    title_text = title_font.render("PAUSE", True, (245, 245, 245))
    kills_text = text_font.render(f"Zombies killed: {zombies_killed}", True, (230, 230, 230))
    hint_text = text_font.render("Press Space to Resume", True, (210, 210, 210))

    screen.blit(title_text, (1300 / 2 - title_text.get_width() / 2, panel_y + 25))
    screen.blit(kills_text, (1300 / 2 - kills_text.get_width() / 2, panel_y + 130))
    screen.blit(hint_text, (1300 / 2 - hint_text.get_width() / 2, panel_y + 180))


def draw_zombie_health_bar(screen, zombie, view_offset_x, view_offset_y):
    max_hp = 3
    hp = max(0, min(zombie.hp, max_hp))

    bar_width = 54
    bar_height = 7
    border = 1

    screen_x = zombie.x - view_offset_x * TILE_SIZE
    screen_y = zombie.y - view_offset_y * TILE_SIZE

    bar_x = int(screen_x - bar_width / 2)
    bar_y = int(screen_y - zombie.radius - 16)

    pygame.draw.rect(screen, (18, 18, 18), (bar_x - border, bar_y - border, bar_width + border * 2, bar_height + border * 2))
    pygame.draw.rect(screen, (120, 30, 30), (bar_x, bar_y, bar_width, bar_height))

    if hp > 0:
        fill_width = int((hp / max_hp) * bar_width)
        if hp <= 1:
            hp_color = (220, 55, 55)
        elif hp == 2:
            hp_color = (235, 150, 45)
        else:
            hp_color = (60, 220, 90)
        pygame.draw.rect(screen, hp_color, (bar_x, bar_y, fill_width, bar_height))

    text_font = pygame.font.Font(None, 18)
    hp_text = text_font.render(f"{hp}/{max_hp}", True, (240, 240, 240))
    text_x = int(screen_x - hp_text.get_width() / 2)
    text_y = bar_y - hp_text.get_height() - 1
    screen.blit(hp_text, (text_x, text_y))


def draw_boss_health_bar(screen, boss, max_hp, view_offset_x, view_offset_y):
    if max_hp <= 0:
        return

    hp = max(0, min(boss.hp, max_hp))
    hp_ratio = hp / max_hp

    bar_width = 130
    bar_height = 10
    border = 2

    screen_x = boss.x - view_offset_x * TILE_SIZE
    screen_y = boss.y - view_offset_y * TILE_SIZE

    bar_x = int(screen_x - bar_width / 2)
    bar_y = int(screen_y - boss.radius - 24)

    if hp_ratio <= 0.35:
        hp_color = (220, 52, 52)
    elif hp_ratio <= 0.65:
        hp_color = (232, 182, 48)
    else:
        hp_color = (76, 214, 108)

    pygame.draw.rect(screen, (14, 14, 14), (bar_x - border, bar_y - border, bar_width + border * 2, bar_height + border * 2))
    pygame.draw.rect(screen, (95, 30, 30), (bar_x, bar_y, bar_width, bar_height))

    if hp > 0:
        fill_width = int(hp_ratio * bar_width)
        pygame.draw.rect(screen, hp_color, (bar_x, bar_y, fill_width, bar_height))

    text_font = pygame.font.Font(None, 24)
    hp_text = text_font.render(f"{hp}/{max_hp}", True, (240, 240, 240))
    text_x = int(screen_x - hp_text.get_width() / 2)
    text_y = bar_y - hp_text.get_height() - 2
    screen.blit(hp_text, (text_x, text_y))


def draw_minimap(screen, player, zombies, unlocked_min_row, room5_unlocked, room7_unlocked, room8_unlocked, x, y):
    """Draw a full-map minimap with player/zombie markers and lock shading."""
    map_rows = len(full_world_map)
    map_cols = len(full_world_map[0])

    panel_w = 250
    panel_h = 200
    padding = 8

    playable_w = panel_w - padding * 2
    playable_h = panel_h - padding * 2
    cell_size = min(playable_w / map_cols, playable_h / map_rows)

    minimap_w = map_cols * cell_size
    minimap_h = map_rows * cell_size
    map_x = x + (panel_w - minimap_w) / 2
    map_y = y + (panel_h - minimap_h) / 2

    panel = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
    panel.fill((10, 10, 10, 165))
    screen.blit(panel, (x, y))
    pygame.draw.rect(screen, (210, 210, 210), (x, y, panel_w, panel_h), 2)

    tile_colors = {
        0: (205, 205, 205),
        1: (95, 95, 95),
        2: (85, 155, 85),
        3: (150, 75, 75),
        4: (100, 140, 80),
    }

    for row_idx, row_data in enumerate(full_world_map):
        for col_idx, tile_id in enumerate(row_data):
            color = tile_colors.get(tile_id, (120, 120, 120))

            # Match main-map lock behavior: locked rooms remain dark on minimap.
            if row_idx < unlocked_min_row:
                color = (color[0] // 4, color[1] // 4, color[2] // 4)
            if (not room5_unlocked) and row_idx >= map5_start_row and row_idx < (map5_start_row + map5_rows_count) and col_idx >= map5_start_col:
                color = (color[0] // 4, color[1] // 4, color[2] // 4)
            if (not room7_unlocked) and row_idx >= map7_start_row and row_idx < (map7_start_row + map7_rows_count) and col_idx >= map7_start_col and col_idx < (map7_start_col + map7_cols_count):
                color = (color[0] // 4, color[1] // 4, color[2] // 4)
            if (not room8_unlocked) and row_idx >= map8_start_row and row_idx < (map8_start_row + map8_rows_count) and col_idx >= map8_start_col and col_idx < (map8_start_col + map8_cols_count):
                color = (color[0] // 4, color[1] // 4, color[2] // 4)

            tile_rect = pygame.Rect(
                map_x + col_idx * cell_size,
                map_y + row_idx * cell_size,
                max(1, cell_size + 0.2),
                max(1, cell_size + 0.2),
            )
            pygame.draw.rect(screen, color, tile_rect)

    # Draw zombies first so player marker stays visible on top.
    for zombie in zombies:
        zx = map_x + (zombie.x / TILE_SIZE) * cell_size
        zy = map_y + (zombie.y / TILE_SIZE) * cell_size
        pygame.draw.circle(screen, (210, 55, 55), (int(zx), int(zy)), 3)

    px = map_x + (player.x / TILE_SIZE) * cell_size
    py = map_y + (player.y / TILE_SIZE) * cell_size
    pygame.draw.circle(screen, (70, 200, 255), (int(px), int(py)), 4)


# ---------------- MAIN GAME ---------------- #

def main():
    current_level = 1
    boss_spawned = False
    boss = None
    boss_max_hp = 0

    pygame.init()
    pygame.display.set_caption("peanut apocolypse")
    screen = pygame.display.set_mode((1300, 800))

    font = pygame.font.Font(None, 40)

    level_clear_img = pygame.image.load("level_complete.png").convert_alpha()
    level_clear_img = pygame.transform.scale(level_clear_img, (600, 300))

    start_screen(screen)

    player = MainC(screen, TILE_SIZE * 6, TILE_SIZE * (map1_start_row + 4), "Character_Placeholder.png")
    healthbar = HealthBar(screen)
    minimap_x = 20
    minimap_y = 20 + healthbar.images[4].get_height() + 12
    
    view_offset_x = player.x / TILE_SIZE - (1300 // TILE_SIZE) / 2
    view_offset_y = player.y / TILE_SIZE - (800 // TILE_SIZE) / 2
    unlocked_min_row = map1_start_row
    room5_unlocked = False
    room7_unlocked = False
    room8_unlocked = False
    show_popup = False
    next_map_number = 2
    is_paused = False
    zombies_killed = 0
    show_level2_popup = False
    level2_popup_started_at = 0
    level2_popup_duration_ms = 1800
    stage1_started_at = pygame.time.get_ticks()
    stage2_summary_kills = 0
    stage2_summary_time_s = 0
    show_level3_popup = False
    level3_popup_started_at = 0
    level3_popup_duration_ms = 1800
    stage2_started_at = None
    stage2_kills_started = 0
    stage3_summary_kills = 0
    stage3_summary_time_s = 0
    show_stage1_popup = True
    stage1_popup_started_at = pygame.time.get_ticks()
    stage1_popup_duration_ms = 1800
    first_wave_started = False
    first_wave_completed = False
    room3_entry_started_at = None
    room3_chase_delay_ms = 1000
    map2_start_col = 0
    map2_room_rows_count = map1_start_row - map2_start_row
    map2_room_cols_count = map3_room_cols_count

    zombies = []

    clock = pygame.time.Clock()
    hurt_sound = pygame.mixer.Sound("Roblox - Oof Death (Sound Effect).mp3")

    while True:
        clock.tick(100)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                is_paused = not is_paused
                continue

            if event.type == pygame.MOUSEBUTTONDOWN and not is_paused:
                player.fire()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_g and _player_in_final_room(player):
                escaped_screen(screen)
                return
            
            # E key unlocks one map layer at a time.
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e and show_popup:
                if unlocked_min_row == map1_start_row:
                    unlocked_min_row = map2_start_row
                    next_map_number = 3
                    patrol_zombies = spawn_patrol_zombies_in_room(
                        screen,
                        player,
                        3,
                        map2_start_row,
                        map2_start_col,
                        map2_room_rows_count,
                        map2_room_cols_count,
                    )
                    zombies.extend(patrol_zombies)
                elif unlocked_min_row == map2_start_row:
                    unlocked_min_row = map3_start_row
                    next_map_number = 4
                    if not first_wave_started:
                        wave1_zombies = spawn_corner_zombies_in_room(
                            screen,
                            player,
                            5,
                            map3_start_row,
                            map3_start_col,
                            map3_room_rows_count,
                            map3_room_cols_count,
                        )
                        zombies.extend(wave1_zombies)
                        first_wave_started = True
                        room3_entry_started_at = None
                elif unlocked_min_row == map3_start_row:
                    unlocked_min_row = map4_start_row
                    next_map_number = 5
                elif next_map_number == 5:
                    room5_unlocked = True
                    next_map_number = 6
                    stage2_summary_kills = zombies_killed
                    stage2_summary_time_s = max(0, (pygame.time.get_ticks() - stage1_started_at) // 1000)
                    stage2_started_at = pygame.time.get_ticks()
                    stage2_kills_started = zombies_killed
                    show_level2_popup = True
                    level2_popup_started_at = pygame.time.get_ticks()
                elif next_map_number == 6:
                    room7_unlocked = True
                    next_map_number = 7
                elif next_map_number == 7:
                    room8_unlocked = True
                    next_map_number = None
                show_popup = False

        if is_paused:
            screen.fill((255, 255, 255))
            draw_map(screen, view_offset_x, view_offset_y, unlocked_min_row, room5_unlocked, room7_unlocked, room8_unlocked)
            draw_map_items(screen, view_offset_x, view_offset_y)

            for bullet in player.bullets:
                screen.blit(bullet.peanut, (bullet.bullet_x - view_offset_x * TILE_SIZE, bullet.bullet_y - view_offset_y * TILE_SIZE))

            player.rect.center = (player.x - view_offset_x * TILE_SIZE, player.y - view_offset_y * TILE_SIZE)
            player.draw()

            for zombie in zombies:
                old_x, old_y = zombie.rect.x, zombie.rect.y
                zombie.rect.center = (zombie.x - view_offset_x * TILE_SIZE, zombie.y - view_offset_y * TILE_SIZE)
                zombie.draw()
                zombie.rect.x, zombie.rect.y = old_x, old_y
                draw_zombie_health_bar(screen, zombie, view_offset_x, view_offset_y)

            healthbar.draw()
            draw_minimap(screen, player, zombies, unlocked_min_row, room5_unlocked, room7_unlocked, room8_unlocked, minimap_x, minimap_y)
            draw_pause_popup(screen, zombies_killed)
            pygame.display.update()
            continue

        pressed_keys = pygame.key.get_pressed()

        dx, dy = 0, 0
        if pressed_keys[pygame.K_w]:
            dy -= 5
        if pressed_keys[pygame.K_s]:
            dy += 5
        if pressed_keys[pygame.K_a]:
            dx -= 5
        if pressed_keys[pygame.K_d]:
            dx += 5
        
        new_x = player.x + dx
        enters_locked_room5_x = (not room5_unlocked) and (new_x + player.radius >= map5_start_col * TILE_SIZE) and (player.y + player.radius >= map5_start_row * TILE_SIZE) and (player.y - player.radius < (map5_start_row + map5_rows_count) * TILE_SIZE)
        enters_locked_room7_x = (not room7_unlocked) and _intersects_room(new_x, player.y, player.radius, map7_start_row, map7_start_col, map7_rows_count, map7_cols_count)
        enters_locked_room8_x = (not room8_unlocked) and _intersects_room(new_x, player.y, player.radius, map8_start_row, map8_start_col, map8_rows_count, map8_cols_count)
        if not enters_locked_room5_x and not enters_locked_room7_x and not enters_locked_room8_x and not is_wall_collision(new_x - player.radius, player.y - player.radius, player.radius * 2, player.radius * 2) and not is_out_of_screen(new_x - player.radius, player.y - player.radius, player.radius * 2, player.radius * 2):
            player.x = new_x
        
        new_y = player.y + dy
        entering_locked_rows = (new_y - player.radius) < (unlocked_min_row * TILE_SIZE)
        enters_locked_room5_y = (not room5_unlocked) and (player.x + player.radius >= map5_start_col * TILE_SIZE) and (new_y + player.radius >= map5_start_row * TILE_SIZE) and (new_y - player.radius < (map5_start_row + map5_rows_count) * TILE_SIZE)
        enters_locked_room7_y = (not room7_unlocked) and _intersects_room(player.x, new_y, player.radius, map7_start_row, map7_start_col, map7_rows_count, map7_cols_count)
        enters_locked_room8_y = (not room8_unlocked) and _intersects_room(player.x, new_y, player.radius, map8_start_row, map8_start_col, map8_rows_count, map8_cols_count)
        if not entering_locked_rows and not enters_locked_room5_y and not enters_locked_room7_y and not enters_locked_room8_y and not is_wall_collision(player.x - player.radius, new_y - player.radius, player.radius * 2, player.radius * 2) and not is_out_of_screen(player.x - player.radius, new_y - player.radius, player.radius * 2, player.radius * 2):
            player.y = new_y
        
        if next_map_number in (2, 3, 4):
            unlock_prompt_y = TILE_SIZE * (unlocked_min_row + 1)
            show_popup = player.y <= unlock_prompt_y
        elif next_map_number == 5:
            near_room5_gate_x = player.x >= (map5_start_col * TILE_SIZE - TILE_SIZE)
            near_room5_gate_y = player.y <= (map5_start_row + map5_rows_count) * TILE_SIZE
            show_popup = near_room5_gate_x and near_room5_gate_y
        elif next_map_number == 6:
            near_room7_gate_x = player.x >= (map7_start_col * TILE_SIZE - 2 * TILE_SIZE)
            near_room7_gate_y = player.y >= (map7_start_row * TILE_SIZE - TILE_SIZE) and player.y <= (map7_start_row + map7_rows_count) * TILE_SIZE
            show_popup = near_room7_gate_x and near_room7_gate_y
        elif next_map_number == 7:
            near_room8_gate_x = player.x >= (map8_start_col * TILE_SIZE - 2 * TILE_SIZE)
            near_room8_gate_y = player.y >= (map8_start_row * TILE_SIZE - TILE_SIZE) and player.y <= (map8_start_row + map8_rows_count) * TILE_SIZE
            show_popup = near_room8_gate_x and near_room8_gate_y
        else:
            show_popup = False

        if show_level2_popup and (pygame.time.get_ticks() - level2_popup_started_at >= level2_popup_duration_ms):
            show_level2_popup = False
        if show_level3_popup and (pygame.time.get_ticks() - level3_popup_started_at >= level3_popup_duration_ms):
            show_level3_popup = False
        if show_stage1_popup and (pygame.time.get_ticks() - stage1_popup_started_at >= stage1_popup_duration_ms):
            show_stage1_popup = False

        if _player_in_room6_passage(player) and current_level < 3:
            current_level = 3
            if stage2_started_at is not None:
                stage3_summary_time_s = max(0, (pygame.time.get_ticks() - stage2_started_at) // 1000)
            else:
                stage3_summary_time_s = 0
            stage3_summary_kills = max(0, zombies_killed - stage2_kills_started)
            show_level3_popup = True
            level3_popup_started_at = pygame.time.get_ticks()

        if first_wave_started and (not first_wave_completed) and room3_entry_started_at is None and _player_in_room3(player):
            room3_entry_started_at = pygame.time.get_ticks()

        if (not first_wave_started) and unlocked_min_row <= map3_start_row and _player_in_room3(player):
            wave1_zombies = spawn_corner_zombies_in_room(
                screen,
                player,
                5,
                map3_start_row,
                map3_start_col,
                map3_room_rows_count,
                map3_room_cols_count,
            )
            zombies.extend(wave1_zombies)
            first_wave_started = True
            room3_entry_started_at = pygame.time.get_ticks()
        
        view_offset_x = player.x / TILE_SIZE - (1300 // TILE_SIZE) / 2
        view_offset_y = player.y / TILE_SIZE - (800 // TILE_SIZE) / 2
        
        max_view_col = len(full_world_map[0]) - (1300 // TILE_SIZE)
        max_view_row = len(full_world_map) - (800 // TILE_SIZE)
        view_offset_x = max(0, min(view_offset_x, max_view_col))
        view_offset_y = max(0, min(view_offset_y, max_view_row))

        player.mouse_x, player.mouse_y = pygame.mouse.get_pos()
        player.mouse_x += int(view_offset_x * TILE_SIZE)
        player.mouse_y += int(view_offset_y * TILE_SIZE)
        player.update_angle()

        current_time = pygame.time.get_ticks()

        # ---------------- ZOMBIE MOVEMENT ---------------- #
        room3_locked = unlocked_min_row > map3_start_row
        room3_chase_active = (
            room3_entry_started_at is not None
            and (current_time - room3_entry_started_at) >= room3_chase_delay_ms
        )
        for zombie in zombies:
            if getattr(zombie, "patrol_mode", False):
                move_patrol_zombie(
                    zombie,
                    map2_start_row,
                    map2_start_col,
                    map2_room_rows_count,
                    map2_room_cols_count,
                )
            else:
                if room3_chase_active:
                    zombie.follow_player(player)
                    zombie.update_angle(player)

            if first_wave_started and not first_wave_completed and room3_locked and getattr(zombie, "wave_tag", "") == "wave1":
                keep_zombie_in_room(
                    zombie,
                    map3_start_row,
                    map3_start_col,
                    map3_room_rows_count,
                    map3_room_cols_count,
                )

            dx = player.x - zombie.x
            dy = player.y - zombie.y
            distance = math.hypot(dx, dy)

            if distance < (player.radius + zombie.radius):
                if current_time - player.last_hit_time > 1000:
                    player.hp -= 1
                    player.last_hit_time = current_time
                    healthbar.set_hp(player.hp)
                    hurt_sound.play()

            if player.hp <= 0:
                pygame.time.delay(1000)
                death_screen(screen)
                return main()

        # ---------------- BOSS MOVEMENT ---------------- #
        if boss_spawned and boss is not None:
            boss.follow_player(player)

            dx = player.x - boss.x
            dy = player.y - boss.y
            distance = math.hypot(dx, dy)

            if distance < (player.radius + boss.radius):
                if current_time - player.last_hit_time > 1000:
                    player.hp -= 1
                    player.last_hit_time = current_time
                    healthbar.set_hp(player.hp)
                    hurt_sound.play()

            if player.hp <= 0:
                pygame.time.delay(1000)
                death_screen(screen)
                return main()

        # ---------------- DRAWING ---------------- #
        screen.fill((255, 255, 255))
        
        draw_map(screen, view_offset_x, view_offset_y, unlocked_min_row, room5_unlocked, room7_unlocked, room8_unlocked)
        draw_map_items(screen, view_offset_x, view_offset_y)

        # ---------------- BULLET COLLISION ---------------- #
        for bullet in player.bullets[:]:
            bullet.move()

            bullet_w = bullet.peanut.get_width()
            bullet_h = bullet.peanut.get_height()
            hits_wall = is_wall_collision(bullet.bullet_x, bullet.bullet_y, bullet_w, bullet_h)
            out_of_bounds = is_out_of_screen(bullet.bullet_x, bullet.bullet_y, bullet_w, bullet_h)
            if hits_wall or out_of_bounds:
                player.bullets.remove(bullet)
                continue

            screen.blit(bullet.peanut, (bullet.bullet_x - view_offset_x * TILE_SIZE, bullet.bullet_y - view_offset_y * TILE_SIZE))

            # Bullet → Zombie
            for zombie in zombies[:]:
                dx = bullet.bullet_x - zombie.x
                dy = bullet.bullet_y - zombie.y
                distance = math.hypot(dx, dy)

                if distance < zombie.radius:
                    zombie.hp -= 1
                    player.bullets.remove(bullet)

                    if zombie.hp <= 0:
                        zombies.remove(zombie)
                        zombies_killed += 1

                    break

            # Bullet → Boss
            if boss_spawned and boss is not None:
                dx = bullet.bullet_x - boss.x
                dy = bullet.bullet_y - boss.y
                distance = math.hypot(dx, dy)

                if distance < boss.radius:
                    boss.hp -= 1
                    player.bullets.remove(bullet)

                    if boss.hp <= 0:
                        boss = None
                        boss_spawned = False
                        current_level += 1

                    continue

        # Draw player
        player.rect.center = (player.x - view_offset_x * TILE_SIZE, player.y - view_offset_y * TILE_SIZE)
        player.draw()

        # Draw zombies
        for zombie in zombies:
            old_x, old_y = zombie.rect.x, zombie.rect.y
            zombie.rect.center = (zombie.x - view_offset_x * TILE_SIZE, zombie.y - view_offset_y * TILE_SIZE)
            zombie.draw()
            zombie.rect.x, zombie.rect.y = old_x, old_y
            draw_zombie_health_bar(screen, zombie, view_offset_x, view_offset_y)

        # Draw boss
        if boss_spawned and boss is not None:
            old_x, old_y = boss.rect.x, boss.rect.y
            boss.rect.center = (boss.x - view_offset_x * TILE_SIZE, boss.y - view_offset_y * TILE_SIZE)
            boss.draw()
            boss.rect.x, boss.rect.y = old_x, old_y
            draw_boss_health_bar(screen, boss, boss_max_hp, view_offset_x, view_offset_y)

        # ---------------- LEVEL CLEAR CHECK ---------------- #
        wave1_alive = any(getattr(zombie, "wave_tag", "") == "wave1" for zombie in zombies)
        if first_wave_started and (not first_wave_completed) and (not wave1_alive):
            screen.blit(level_clear_img, (350, 250))
            pygame.display.update()

            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_e:
                            waiting = False

                pygame.time.delay(50)

            first_wave_completed = True
            current_level = max(current_level, 2)
            player.bullets.clear()
            zombies[:] = [z for z in zombies if getattr(z, "wave_tag", "") != "wave1"]

        healthbar.draw()
        draw_minimap(screen, player, zombies, unlocked_min_row, room5_unlocked, room7_unlocked, room8_unlocked, minimap_x, minimap_y)

        if show_popup:
            draw_unlock_prompt(screen, next_map_number)

        if show_level2_popup:
            draw_level2_popup(screen, stage2_summary_kills, stage2_summary_time_s)
        if show_level3_popup:
            draw_level3_popup(screen, stage3_summary_kills, stage3_summary_time_s)
        if show_stage1_popup:
            draw_stage1_popup(screen)

        if _player_in_final_room(player):
            draw_escape_prompt(screen)

        level_text = font.render(f"Level: {current_level}", True, (0, 0, 0))
        screen.blit(level_text, (20, 760))

        pygame.display.update()


main()